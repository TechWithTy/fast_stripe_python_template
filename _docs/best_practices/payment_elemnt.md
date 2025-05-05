Payment Element integration best practices
Build your Payment Element integration using best practices.
Copy page

Use the checklist on this page to make sure you build your Payment Element integration for optimal performance. The following features enable you to access additional integration options. For example, if you use Dynamic payment methods, you can use payment method rules to present payment methods with custom criteria.
Integration checklist

    Choose a layout

Choose the Payment Element’s layout to match the style of your site, then run an A/B test to confirm the best choice. If you have over 4 payment methods, we recommend the accordion layout.
Add styling

Style the Payment Element to match the visual design of your website using the Appearance API. You can apply this style to any element you add to your integration.
Choose how to collect a payment

Consider if you want to collect a payment before you create the PaymentIntent API call. To accept a payment, you must create a PaymentIntent that contains an amount and currency, and confirm that payment to trigger Stripe to make a charge. However, you can alternate the order that you collect the payment and create the PaymentIntent. We recommend that you collect the payment first.
Send metadata

Send metadata in your PaymentIntent to allow metadata to show up in your reports. This indexes your metadata to make sure that it’s searchable in the Stripe Dashboard. You can use this metadata to find and reference transactions.
Make sure to use the latest API

Check to make sure your PaymentIntent uses the latest API version.
Select the payment methods you want to display

Use Dynamic payment methods as part of the default Stripe integration to dynamically display eligible payment methods to each customer. Stripe orders the payment methods by conversion probability based on factors such as the amount, currency, and location. Dynamic payment methods allow you to:

    Choose the payment methods that your customers can use from the Dashboard.
    Use additional features, such as payment method rules, which allows you to present payment methods using custom criteria.

Test payment methods

When your integration is complete, test and view how payment methods appear to customers. From the Review displayed payment methods form, enter a PaymentIntent ID to learn which payment methods were and weren’t available for that specific transaction. You can also simulate which payment methods display in a given scenario by changing factors such as the amount, currency, capture method, and future usage.
Avoid iframes

    The Payment Element contains an iframe that securely sends payment information to Stripe over an HTTPS connection. Avoid placing the Payment Element within another iframe because some payment methods require a redirect to another page for payment confirmation. For more information on iframe considerations, see Collect payment details.

Additional features checklist

    Enable Link

After you integrate your UI and dynamic payment methods, enable Link in the Payment Method settings page. Link securely saves and fills in customer payment and shipping details. It supports various payment methods, including credit cards, debit cards, and US bank accounts. For logged-in customers that already use Link, this feature prefills their information, regardless of whether they initially saved it on the checkout page of another business.
Add the Link Authentication Element

To collect and prefill shipping addresses and sell physical goods, we recommend using the Link Authentication Element to create a single email input field for both email collection and Link authentication.
Add the Address Element

The Address Element streamlines collection of shipping and billing information during checkout. It integrates with other elements and prefills addresses with Link. It supports auto-suggestions for new address entry using free Google Autocomplete support.

    In shipping mode, customers have the option to use their shipping address as their billing address.
    In billing mode, Stripe hides billing fields within the Payment Element to make sure that customers only need to enter their details once.

Add the Payment Method Messaging Element

If you choose to offer BNPLs, we recommend that you promote them ahead of checkout to help drive awareness, increase order value, and positively impact conversion using the Payment Method Messaging Element.

    You can display this unified embeddable component on product detail, cart, and payment pages.
    This element includes support for Affirm, Afterpay, and Klarna.

Add the Express Checkout Element
Use the Express Checkout Element to show customers multiple one-click payment buttons in a single UI component, including Apple Pay, Google Pay, PayPal, and Lin