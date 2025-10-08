"""
Centralized pricing utilities for credit packages and bulk discounts.
Implements DRY principle for pricing calculations across the application.
"""

import logging
from typing import Dict, Tuple
from dataclasses import dataclass
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


@dataclass
class PricingResult:
    """Result of pricing calculation"""
    credits: int
    base_price: float
    final_price: float
    discount_percentage: int
    savings_amount: float
    price_per_credit: float
    currency: str = "usd"


class CreditPricingCalculator:
    """
    Centralized credit pricing calculator with configurable discount tiers.
    Follows SaaS best practices for bulk discounts and transparent pricing.
    """
    
    def __init__(self, base_price_per_credit: float = 0.10):
        self.base_price_per_credit = base_price_per_credit
        self.discount_tiers = self._get_default_discount_tiers()
    
    def _get_default_discount_tiers(self) -> Dict[int, float]:
        """
        Default bulk discount tiers for credit purchases.
        Can be overridden for custom pricing strategies.
        """
        return {
            1000: 0.25,    # 25% off for 1000+ credits
            500: 0.20,     # 20% off for 500+ credits  
            100: 0.10,     # 10% off for 100+ credits
            0: 0.0         # No discount for < 100 credits
        }
    
    def update_discount_tiers(self, tiers: Dict[int, float]) -> None:
        """Update discount tiers configuration"""
        self.discount_tiers = tiers
        logger.info(f"Updated pricing tiers: {tiers}")
    
    @tracer.start_as_current_span("calculate_credit_pricing")
    def calculate_pricing(self, credits: int) -> PricingResult:
        """
        Calculate comprehensive pricing information for credit purchase.
        
        Args:
            credits: Number of credits to purchase
            
        Returns:
            PricingResult with all pricing details
        """
        span = trace.get_current_span()
        span.set_attribute("credits_requested", credits)
        
        if credits < 1:
            raise ValueError("Credits must be at least 1")
        
        # Calculate base price
        base_price = credits * self.base_price_per_credit
        
        # Find applicable discount tier
        discount = self._get_applicable_discount(credits)
        
        # Calculate final pricing
        final_price = base_price * (1 - discount)
        savings_amount = base_price - final_price
        discount_percentage = int((discount * 100)) if discount > 0 else 0
        price_per_credit = final_price / credits
        
        result = PricingResult(
            credits=credits,
            base_price=round(base_price, 2),
            final_price=round(final_price, 2),
            discount_percentage=discount_percentage,
            savings_amount=round(savings_amount, 2),
            price_per_credit=round(price_per_credit, 4),
            currency="usd"
        )
        
        span.set_attribute("base_price", result.base_price)
        span.set_attribute("final_price", result.final_price)
        span.set_attribute("discount_percentage", discount_percentage)
        span.set_attribute("savings_amount", result.savings_amount)
        
        logger.debug(f"Calculated pricing for {credits} credits: ${result.final_price} ({discount_percentage}% off)")
        
        return result
    
    def _get_applicable_discount(self, credits: int) -> float:
        """Get the applicable discount percentage for the credit amount"""
        for tier_credits, tier_discount in sorted(self.discount_tiers.items(), reverse=True):
            if credits >= tier_credits:
                return tier_discount
        return 0.0
    
    def get_pricing_tiers_info(self) -> Dict[str, Dict[str, any]]:
        """
        Get information about all pricing tiers for display purposes.
        Useful for creating pricing tables and promotional materials.
        """
        tiers_info = {}
        
        for tier_credits, discount in sorted(self.discount_tiers.items()):
            if tier_credits == 0:
                continue
                
            tier_name = f"{tier_credits}+ Credits"
            sample_pricing = self.calculate_pricing(tier_credits)
            
            tiers_info[tier_name] = {
                "min_credits": tier_credits,
                "discount_percentage": int(discount * 100),
                "sample_pricing": {
                    "credits": sample_pricing.credits,
                    "price": sample_pricing.final_price,
                    "savings": sample_pricing.savings_amount,
                    "price_per_credit": sample_pricing.price_per_credit
                }
            }
        
        return tiers_info


# * Global instance for application-wide use
default_pricing_calculator = CreditPricingCalculator()


def calculate_credit_cost(credits: int) -> float:
    """
    Convenience function for backward compatibility.
    Returns only the final price for simple use cases.
    """
    result = default_pricing_calculator.calculate_pricing(credits)
    return result.final_price


def get_credit_pricing_info(credits: int) -> Dict[str, any]:
    """
    Get comprehensive pricing information as a dictionary.
    Useful for API responses and frontend integration.
    """
    result = default_pricing_calculator.calculate_pricing(credits)
    return {
        "credits": result.credits,
        "total_price": result.final_price,
        "base_price": result.base_price,
        "savings_amount": result.savings_amount,
        "savings_percentage": result.discount_percentage,
        "price_per_credit": result.price_per_credit,
        "currency": result.currency
    }


def get_all_pricing_tiers() -> Dict[str, Dict[str, any]]:
    """Get information about all available pricing tiers"""
    return default_pricing_calculator.get_pricing_tiers_info()


# * Example usage for testing and documentation
if __name__ == "__main__":
    # Test pricing calculations
    test_amounts = [1, 50, 100, 250, 500, 750, 1000, 2500]
    
    print("Credit Pricing Calculator Test")
    print("=" * 50)
    
    for amount in test_amounts:
        result = default_pricing_calculator.calculate_pricing(amount)
        print(f"{amount:,} credits: ${result.final_price} ({result.discount_percentage}% off, save ${result.savings_amount})")
    
    print("\nPricing Tiers Information:")
    print("=" * 50)
    
    tiers = get_all_pricing_tiers()
    for tier_name, tier_info in tiers.items():
        print(f"{tier_name}: {tier_info['discount_percentage']}% off")
        sample = tier_info['sample_pricing']
        print(f"  Example: {sample['credits']} credits = ${sample['price']} (${sample['price_per_credit']}/credit)")
