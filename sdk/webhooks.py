"""
Centralized Stripe webhook handling utilities.
Implements DRY principle for webhook processing and validation.
"""

import json
import logging
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
from dataclasses import dataclass

from opentelemetry import trace
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


@dataclass
class WebhookResult:
    """Result of webhook processing"""
    success: bool
    event_type: str
    event_id: str
    message: str
    data: Optional[Dict[str, Any]] = None


class StripeWebhookHandler:
    """
    Centralized Stripe webhook handler with event routing and validation.
    Implements production best practices for webhook processing.
    """
    
    def __init__(self, stripe_client=None):
        self.stripe_client = stripe_client
        self.event_handlers: Dict[str, Callable] = {}
        self.supported_events = [
            "checkout.session.completed",
            "payment_intent.succeeded",
            "payment_intent.payment_failed", 
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
            "invoice.paid",
            "invoice.payment_failed"
        ]
    
    def register_handler(self, event_type: str, handler: Callable) -> None:
        """Register a handler function for specific webhook event type"""
        self.event_handlers[event_type] = handler
        logger.info(f"Registered webhook handler for event: {event_type}")
    
    @tracer.start_as_current_span("verify_webhook_signature")
    def verify_webhook_signature(
        self, 
        payload: bytes, 
        signature: str, 
        webhook_secret: str
    ) -> bool:
        """
        Verify Stripe webhook signature using centralized validation.
        
        Args:
            payload: Raw webhook payload
            signature: Stripe signature header
            webhook_secret: Webhook endpoint secret
            
        Returns:
            bool: True if signature is valid
        """
        span = trace.get_current_span()
        span.set_attribute("operation", "verify_webhook_signature")
        
        try:
            if not self.stripe_client:
                logger.error("Stripe client not initialized for webhook verification")
                return False
                
            # Use centralized Stripe client for verification
            self.stripe_client.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            
            span.set_attribute("signature_valid", True)
            logger.debug("Webhook signature verified successfully")
            return True
            
        except ValueError as e:
            span.set_attribute("signature_valid", False)
            span.set_attribute("error", "Invalid payload")
            logger.error(f"Invalid webhook payload: {str(e)}")
            return False
            
        except Exception as e:
            span.set_attribute("signature_valid", False)
            span.set_attribute("error", "Invalid signature")
            logger.error(f"Webhook signature verification failed: {str(e)}")
            return False
    
    @tracer.start_as_current_span("parse_webhook_event")
    def parse_webhook_event(self, payload: bytes) -> Dict[str, Any]:
        """
        Parse Stripe webhook event payload with error handling.
        
        Args:
            payload: Raw webhook payload
            
        Returns:
            Dict: Parsed webhook event
            
        Raises:
            ValueError: If payload is invalid JSON
        """
        span = trace.get_current_span()
        span.set_attribute("operation", "parse_webhook_event")
        
        try:
            event = json.loads(payload)
            
            # Validate required event fields
            required_fields = ["id", "type", "data"]
            for field in required_fields:
                if field not in event:
                    raise ValueError(f"Missing required field: {field}")
            
            # Also validate that data.object exists
            if "object" not in event.get("data", {}):
                raise ValueError("Missing required field: data.object")
            
            span.set_attribute("event_type", event.get("type"))
            span.set_attribute("event_id", event.get("id"))
            
            logger.debug(f"Successfully parsed webhook event: {event.get('type')} ({event.get('id')})")
            
            return event
            
        except json.JSONDecodeError as e:
            span.record_exception(e)
            logger.error(f"Failed to parse webhook payload as JSON: {str(e)}")
            raise ValueError("Invalid JSON payload")
        
        except Exception as e:
            span.record_exception(e)
            logger.error(f"Error parsing webhook event: {str(e)}")
            raise ValueError(f"Failed to parse webhook event: {str(e)}")
    
    @tracer.start_as_current_span("process_webhook_event")
    async def process_webhook_event(self, event: Dict[str, Any]) -> WebhookResult:
        """
        Process webhook event by routing to appropriate handler.
        
        Args:
            event: Parsed webhook event
            
        Returns:
            WebhookResult: Processing result with success status and details
        """
        span = trace.get_current_span()
        event_type = event.get("type")
        event_id = event.get("id")
        
        span.set_attribute("event_type", event_type)
        span.set_attribute("event_id", event_id)
        
        try:
            # Check if event type is supported
            if event_type not in self.supported_events:
                logger.warning(f"Unsupported webhook event type: {event_type}")
                return WebhookResult(
                    success=True,  # Return success to prevent retries
                    event_type=event_type,
                    event_id=event_id,
                    message=f"Event type {event_type} not handled"
                )
            
            # Check if handler is registered
            if event_type not in self.event_handlers:
                logger.warning(f"No handler registered for event type: {event_type}")
                return WebhookResult(
                    success=True,  # Return success to prevent retries
                    event_type=event_type,
                    event_id=event_id,
                    message=f"No handler for event type {event_type}"
                )
            
            # Process event with registered handler
            handler = self.event_handlers[event_type]
            result = await handler(event)
            
            logger.info(f"Successfully processed webhook event {event_id} ({event_type})")
            
            return WebhookResult(
                success=True,
                event_type=event_type,
                event_id=event_id,
                message="Event processed successfully",
                data=result if isinstance(result, dict) else None
            )
            
        except Exception as e:
            span.record_exception(e)
            logger.error(f"Error processing webhook event {event_id}: {str(e)}")
            
            return WebhookResult(
                success=False,
                event_type=event_type,
                event_id=event_id,
                message=f"Processing failed: {str(e)}"
            )
    
    def get_supported_events(self) -> List[str]:
        """Get list of supported webhook event types"""
        return self.supported_events.copy()
    
    def get_registered_handlers(self) -> Dict[str, str]:
        """Get information about registered event handlers"""
        return {
            event_type: handler.__name__ 
            for event_type, handler in self.event_handlers.items()
        }


class PaymentEventProcessor:
    """
    Specialized processor for payment-related webhook events.
    Handles credit allocation and payment processing logic.
    """
    
    def __init__(self):
        pass
    
    @tracer.start_as_current_span("handle_checkout_completed")
    async def handle_checkout_completed(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle checkout.session.completed webhook event.
        
        Args:
            event: Checkout session completed event
            
        Returns:
            Dict: Processing result with session and credit details
        """
        span = trace.get_current_span()
        span.set_attribute("operation", "handle_checkout_completed")
        
        try:
            session_data = event["data"]["object"]
            session_id = session_data["id"]
            metadata = session_data.get("metadata", {})
            
            # Extract payment information
            user_id = metadata.get("user_id")
            credits_str = metadata.get("credits", "0")
            credits_purchased = int(credits_str) if credits_str.isdigit() else 0
            amount_total = session_data.get("amount_total", 0)
            
            span.set_attribute("session_id", session_id)
            span.set_attribute("user_id", user_id)
            span.set_attribute("credits_purchased", credits_purchased)
            span.set_attribute("amount_total", amount_total)
            
            logger.info(f"Processing checkout completion for session {session_id}: {credits_purchased} credits for user {user_id}")
            
            # Integration with credit processing service will be handled by the main application
            # This webhook handler focuses on parsing and validating the webhook event
            
            return {
                "session_id": session_id,
                "user_id": user_id,
                "credits_purchased": credits_purchased,
                "amount_paid": amount_total / 100,  # Convert from cents
                "status": "processed"
            }
            
        except Exception as e:
            span.record_exception(e)
            logger.error(f"Error handling checkout completed event: {str(e)}")
            raise
    
    @tracer.start_as_current_span("handle_payment_succeeded")
    async def handle_payment_succeeded(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle payment_intent.succeeded webhook event"""
        span = trace.get_current_span()
        span.set_attribute("operation", "handle_payment_succeeded")
        
        payment_intent = event["data"]["object"]
        payment_intent_id = payment_intent["id"]
        amount = payment_intent["amount"]
        
        span.set_attribute("payment_intent_id", payment_intent_id)
        span.set_attribute("amount", amount)
        
        logger.info(f"Payment succeeded: {payment_intent_id} for ${amount/100}")
        
        return {
            "payment_intent_id": payment_intent_id,
            "amount": amount / 100,
            "status": "succeeded"
        }
    
    @tracer.start_as_current_span("handle_payment_failed")
    async def handle_payment_failed(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Handle payment_intent.payment_failed webhook event"""
        span = trace.get_current_span()
        span.set_attribute("operation", "handle_payment_failed")
        
        payment_intent = event["data"]["object"]
        payment_intent_id = payment_intent["id"]
        failure_reason = payment_intent.get("last_payment_error", {}).get("message", "Unknown")
        
        span.set_attribute("payment_intent_id", payment_intent_id)
        span.set_attribute("failure_reason", failure_reason)
        
        logger.warning(f"Payment failed: {payment_intent_id} - {failure_reason}")
        
        return {
            "payment_intent_id": payment_intent_id,
            "failure_reason": failure_reason,
            "status": "failed"
        }


# * Global instances for application-wide use
default_webhook_handler = StripeWebhookHandler()
default_payment_processor = PaymentEventProcessor()

# * Register default payment event handlers
default_webhook_handler.register_handler(
    "checkout.session.completed", 
    default_payment_processor.handle_checkout_completed
)
default_webhook_handler.register_handler(
    "payment_intent.succeeded", 
    default_payment_processor.handle_payment_succeeded
)
default_webhook_handler.register_handler(
    "payment_intent.payment_failed", 
    default_payment_processor.handle_payment_failed
)


def get_webhook_handler(stripe_client=None) -> StripeWebhookHandler:
    """
    Get configured webhook handler instance.
    
    Args:
        stripe_client: Optional Stripe client instance
        
    Returns:
        StripeWebhookHandler: Configured webhook handler
    """
    if stripe_client:
        handler = StripeWebhookHandler(stripe_client)
        # Re-register default handlers
        handler.register_handler(
            "checkout.session.completed", 
            default_payment_processor.handle_checkout_completed
        )
        handler.register_handler(
            "payment_intent.succeeded", 
            default_payment_processor.handle_payment_succeeded
        )
        handler.register_handler(
            "payment_intent.payment_failed", 
            default_payment_processor.handle_payment_failed
        )
        return handler
    
    return default_webhook_handler
