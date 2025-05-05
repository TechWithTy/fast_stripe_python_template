Best practices for preventing fraud
Learn how to use best practices to protect against disputes and fraudulent payments.
Copy page

Creating an effective dispute and fraud prevention strategy that best suits your business can help prevent fraud from occurring. By employing some of these best practices as part of your overall strategy, you can avoid excessive chargebacks and reduce potential customer burden and losses.
Tools for everyone

These are tools that any Stripe user—whether or not they’re a developer, and whether or not they use any specialized Stripe tools like Radar—can leverage to reduce fraud and dispute incidents.
Be clear and transparent with your customers

Clear and frequent contact with your customers can help prevent many of the reasons for disputes. By responding to issues and processing refunds or replacement orders quickly, your customers are far less likely to take the time to dispute a payment. Make your customer service contact information easy to find, keep customers updated throughout their order process, and provide updates about deliveries.
Caution

Include a clear description of your refund and cancellation policies in your terms of service. You can require your users to agree to your terms of service to increase the likelihood that card issuers respect your policies in the event of a dispute.

    Require ToS Agreement

In general, make your terms of service and policies easy to find on your website, and require customers to agree to them. Rather than only linking to them during checkout, provide a full version of them on the checkout page or as a pop-up with a requirement to agree to them prior to submitting the order.
Show complete policy

Card issuers can be very specific about how you present your policies. If you have a checkbox your customer must accept that only contains a link, the issuer might reject it as unsatisfactory evidence that your customer was aware of your policies. There must be reasonable evidence that you presented your customer with a full copy of your policies prior to their purchase.
Track shipping

When shipping physical goods to customers, use carriers and services that provide online tracking and delivery confirmation whenever possible. Provide this information to your customers as soon as it’s available (if you need to submit tracking information as dispute evidence, be aware that card issuers don’t follow links so screenshots must be provided).
Use clear statement descriptors

Set a recognizable name for your statement descriptor through your account settings. We recommend using your website domain or business name to make sure customers can easily identify their purchase when they look at their statement.

Statement descriptors are limited to between 5 and 22 characters. They must contain at least 5 letters and can’t use the special characters <, >, \, ', or ".
Separate your business accounts

    Avoid using the same Stripe account for separate businesses. Each Stripe account should represent a single business, which allows for separate statement descriptors and contact information. If you need to process payments for multiple businesses, create additional accounts for each.

Consider proactively refunding suspicious payments

You should immediately refund any payment you’re sure is fraud (unless you’re covered by some form of liability shift, such as with 3D Secure). If you know you’re going to receive a fraud dispute on it, you can save yourself the dispute fee, the increase to your dispute rate, and the potential loss of product by fully refunding the fraudulent payment.
Caution

While customers can’t dispute fully refunded payments, they can still dispute partially refunded payments. Card network rules even allow for a payment that has been partially refunded to be disputed for the full payment amount.

However, sometimes you might suspect a payment is fraud, but your suspicions fall short of absolute certainty. Sometimes it makes sense to aggressively refund every charge that falls into this gray area and sometimes it doesn’t.

You might want to pursue an aggressive refund strategy if any of the following apply:

    Order not yet fulfilled. The loss of your product could be prevented by a refund. That is, if you haven’t already committed your product or service in some irreversible way by the time you suspect fraud, you might want to be more aggressive in refunding. Whereas if your product or service was irretrievable—for example, the product already shipped, or the service has already been used—it might make more sense not to refund, and to wait and see if it does turn out to be fraud.
    Excessive disputes. Your recent dispute activity has been excessive by card network definitions, which could put your account standing with Stripe at risk or put you at risk of being identified into a chargeback monitoring program.
    Chargeback monitoring program. You’re already in a chargeback monitoring program and need to exit the program.
    New or small business. Your business has small enough payment volume (say, fewer than 100 payments per month) that one or two fraud disputes can have a very outsized impact on your dispute rate, even if you otherwise have little dispute activity.

If none of the above apply, you might want to be more conservative with how frequently you proactively refund charges you suspect are fraudulent.
Refunding a payment as fraud

To refund a payment, in the Dashboard, select the payment and click Refund as fraud. This refunds the payment and reports it as fraudulent to Stripe so that we can further improve our fraud detection.
Delay shipping orders

If you ship physical goods, consider delaying the shipment by 24-48 hours. This time gives cardholders a chance to spot and report any fraud on their accounts. You would still receive a fraud dispute in this scenario, but at least you wouldn’t also lose the merchandise. Not all cardholders check their statements on a daily basis, however, and their card issuer might not proactively notify them about the transaction.

Customers that request overnight or expedited shipping should be considered higher risk, as the increased cost of such services is of no consequence to fraudsters. One tactic you can use to identify these types of payments is to offer same day or overnight shipping at a very high cost–many times more expensive than any other shipping option you provide.

It’s far less likely that any legitimate customer would pay such a high cost, but a fraudster would want the goods to be shipped as soon as possible and have no regard for the additional cost. You can then manually screen any customers that opt for the anomalously expensive shipping option and scrutinize the order to determine if it looks genuine. Using a separate auth and capture process together with Radar reviews is a good way to do so.
Ship to a verified address

Shipping to a verified billing address which has passed postal code and street address checks is the safest option. When using an address that hasn’t been verified, you can’t prove that the order was shipped to the legitimate cardholder if the payment is later disputed.

This doesn’t prevent you shipping to a different address, though you should do all you can to mitigate the risks involved. For instance, you may only want to ship orders to a different address for returning customers you already know to be legitimate, or who provide a fully verifiable billing address. In addition, any of the following could indicate the payment is suspicious:

    The order is much larger than normal, or is only for your most expensive products
    The customer changed the shipping address after placing the order
    The customer requested expedited shipping
    The products ordered have a high resale value
    The shipping destination is different from the billing address or the card’s country of origin (for example, the billing address is in Spain, but the shipping address is in France)

Reviewing the order and the shipping address information can help you determine whether or not the order presents an unacceptable risk to you.
Benchmarking your dispute rate

Your account’s dispute rate is an important metric to use when reviewing the efficacy of your disputes and fraud prevention methods. You can regularly review these metrics in your Stripe Dashboard to see the impact your dispute prevention strategies are having.
Tools for users of Radar for Fraud Teams

Radar is a suite of features and tools for fighting fraud that is built into Stripe and requires no additional integration work.
Manually review payments

Radar for Fraud Teams includes a review feature that allows you to place certain payments into review—though keep in mind that these payments are still processed and the credit card charged, unless you are using a separate auth and capture process. These payments are placed into the review queue for you to take a closer look at. If you suspect the payment is fraudulent, you can refund it.

You should review payments that Stripe has placed into your review queue as soon as possible. Payments with an elevated risk of fraud are automatically marked for review. You can also create additional rules to customize the types of payments that should be placed in your review queue.

Here are some considerations when reviewing a payment:

    Does the billing address match the shipping address?
    Has the billing address been verified by AVS? Does it also match the card’s country of origin?
    Does the customer’s email address match the cardholder’s name?
    Is this an order that the customer has asked to be expedited?
    Have multiple orders from different credit cards originated from this same IP address?
    Has this customer made many order attempts that have been declined?

If you’re unsure about a payment when you’re reviewing it, you should always contact the customer by phone or email. If a payment’s billing and shipping address don’t match, look into the shipping address using Google Maps & Street View to find out more. A common tactic that fraudsters use is to have orders shipped to a freight or mail forwarding service or storage facility that forwards the goods to their actual location.
Use Radar rules to automatically block payments or place them in review

Radar for Fraud Teams, is built directly into the payment flow and combines a customizable rules engine with powerful machine learning algorithms. It can detect patterns across payments from every business processing payments with Stripe, assessing the risk of each one.

Using rules, you can automatically evaluate payments based on your specific detection criteria and take the appropriate action on them. You can also create rules that use multiple criteria, allowing you to allow or block payments that meet multiple conditions. Each business has different risks.
Country and card type limiting

If you’re experiencing increased fraud coming from certain countries, you can set up rules to block payments from any country you do not want to accept payments from, using the :ip_country: and :card_country: rule attributes. For example, you can create the following rule to block all payments and cards originating from Canada: Block if :ip_country: = ca and :card_country: = 'ca'. Similarly, if your business only supports the country it operates in, you can create a rule that blocks any payments from all other countries. For example, a rule to block payments that don’t originate from Australia is: Block if :ip_country: != au and :card_country: != 'au'.

You can set limits on which type of cards to accept, either by brand, (for example, Mastercard), or by funding type (for example, pre-paid). This can be particularly helpful if you see excessive fraud from certain card types. To block payments from all Visa-issued debit cards, an example rule would be: Block if :card_brand: = visa and :card_funding: = 'debit'.
Tools for developers

These are tools that require some development work to implement. If you rely on a Stripe partner to provide your payments integration, you might not have the ability to directly implement these on your own.
Process your transactions on Stripe

The Visa Compelling Evidence 3.0 rules rely on transaction history to dispute friendly fraud by showing previous non-fraud transactions with the same cardholder within a specified period. When you get a Visa fraud dispute, Stripe can identify qualifying transactions in your history on our platform and pre-populate the dispute response with most of the required evidence you need. You can use this evidence to significantly increase your likelihood of overturning the dispute in your favor.

Stripe can’t determine eligibility or submit evidence for externally processed transactions, so we recommend:

    Using Stripe processing whenever possible
    Including the customer IP address, email address, shipping address, and product descriptions in your transactions with Stripe

Collect as much payment information as possible

Some disputes are lost because only the minimum information was required during checkout. This makes it difficult (sometimes impossible) for Stripe or the card issuer to verify that the customer is legitimate. For instance, while a billing postal code isn’t always necessary to process a card payment, including it allows the payment to be verified by the card issuer. If verification fails, consider rejecting the payment because this might indicate fraud.

Use Checkout or Advanced fraud detection to make sure your integration is best equipped to provide relevant payment information, such as:

Customer name
Customer email address
CVC number
Full billing address and postal code
Shipping address (if different from billing address)

    Tracking information

Implement a cardholder authentication method such as 3D Secure

3D Secure is a way to add a verification step between the customer and the card issuer to your checkout flow. Payments that have been authenticated with 3D Secure might be protected from most fraudulent disputes through a rule known as liability shift. You will, however, still receive Early Fraud Warnings that can count against card brand monitoring programs.

Learn more at Card Authentication and 3D Secure.
Programmatically verify your customer’s identity

For some, verifying the identity of customers can be beneficial. Consider using Stripe Identity to verify a government ID and match with a selfie of the document holder. Alternatively, you can ask customers to connect their Facebook or LinkedIn accounts as a further proof of identity. This is an extra step that a fraudulent actor might not take. Some legitimate customers might not want to go through this additional step either, and your conversion rate might suffer as a result.
Use auth and capture when creating payments

Credit card charge attempts are processed in two parts. The charge is first authorized by requesting authorization for the amount to charge from the card issuer. After a charge is approved, by default it’s then captured immediately afterwards and the amount deducted from the card.

A capture later payment flow (sometimes called “auth and capture”) is the process of performing these two steps at separate times. The authorization can be made first, which holds the amount on the card and appears on a customer’s statement as a pending transaction, but does not actually move money out of their account. The charge can then be captured any time up to 7 days after the authorization. Capturing a charge completes the payment and the funds are deducted from the customer’s card. If a charge isn’t captured within the time limit, the authorization is automatically released.

Similar to delayed shipping, this method can allow enough time for potential fraud to come to light, giving you the option to carefully review—and potentially refund—the transaction. Cardholders can’t dispute uncaptured authorizations, only fully captured payments. With Radar for Fraud Teams you can manually capture these payments in the review process.
Set a custom statement descriptor for each payment

The statement descriptor is the text that appears on customers’ card statements with information about the company that’s associated with a payment. One way to use a statement descriptor is to insert a short, random code that your customer then has to verify. When you suspect a transaction might be fraudulent, you can contact your customer and ask them to give you the code that is shown on their online statement, and if they do not, you would refund the payment.

You can either edit your default statement descriptor within the Dashboard or set a dynamic statement descriptor whenever a payment is created through the API.

While this method can’t help against a fraudster who may have access to a cardholder’s online card issuer or credit account, this is rare. Using the statement descriptor in this manner can provide reassurance that the customer is likely to be genuine. As with some other prevention methods, the added customer friction of this method could lead to some legitimate payments being refunded.
