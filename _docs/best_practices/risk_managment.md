Best practices for risk management
Protect your integration by implementing best practices for preventing, mitigating, and responding to payments risk.
Copy page

These best practices for protecting your Connect integration are based on what we’ve learned from thousands of platforms, extensions, and plug-ins.
Decide your approach to negative balance liability

Because your choice of negative balance liability can significantly impact your platform and connected accounts, consider it carefully before onboarding any accounts. We advise that new platforms have Stripe take responsibility for negative balances on connected accounts. Only consider taking responsibility as the platform if you’re confident in your ability to manage merchant risk.
Best practices for both approaches
Prevent fraudulent transactions by enabling Radar

When you enable Radar, payment risk scoring is on by default at the user level, preventing transactions with high fraud risk. For information on using Radar with connected accounts, see Using Radar with Connect.
Manage notifications and communications with Stripe
Webhook notifications

Stripe uses webhooks to notify you of your connected accounts’ activities. Set up Connect webhooks so you can avoid delays in fund transfers by promptly responding to connected account updates and Stripe requests.

Stripe requests additional information if the provided user information fails verification. An incorrect date of birth or last name might be the result of a data entry error. You can help your connected accounts respond to failed verifications by directing them to Stripe-hosted onboarding or Embedded onboarding, or request the data yourself if you use API onboarding.

When a user updates their account information (for example, bank account), Stripe sends you a notification of the change.
Accounts to review

The Connected accounts page in your Dashboard helps you monitor the risk and onboarding status of all of your connected accounts. It flags the connected accounts that have restrictions due to risk and onboarding issues, as well as the accounts that Stripe expects to have restrictions in the near future.
Support transparency

A connected account’s details page includes a list of support cases that the account has opened with Stripe. Select a case to review the conversation between the account and Stripe. If you have any additional context or information, you can also help resolve the case by sending private messages to Stripe Support.
Concerns about sanctions

As a US company, Stripe complies with all sanctions programs administered by the US Office of Foreign Assets Control (OFAC), along with a number of other national and international sanctions regimes. That includes prohibitions against interactions with certain individuals and entities, as well as comprehensive bans on business dealings involving certain countries or regions targeted by sanctions regimes.

Stripe screens all accounts, including connected accounts, in compliance with our own obligations under sanctions regimes. If a connected account is flagged as a possible sanctions concern, Stripe pauses payouts from that account and emails the platform to request additional information. If you have a preferred email address for receiving sanctions-related requests, contact Stripe Support.

Payouts from the connected account remain paused until the review has been cleared. Disregarding or violating sanctions can lead to fines, regulatory action, and loss of licensing for both Stripe and our users.
Best practices for platform negative balance liability connected accounts
Core considerations

Platforms can bring merchant risk management in-house and further tailor their connected accounts’ experiences using risk tooling that Stripe provides. For additional details on strategy and approach to risk management, see our guide on risk management for software platforms. Starting a risk management solution involves several investments. Some of the core considerations include:

    Screening and detection: Risk screening infrastructure to understand the risk profile of connected accounts and prevent or reduce fraud and credit risk. This includes building detection mechanisms to identify risky connected accounts.
    Monitoring and mitigation: Systems to monitor risk signals and take action (such as pausing payouts, pay-ins, and so on) to mitigate exposure in response to changes in risk signals over time. Building workflows in your product to make sure that users have resolution paths in response to actions, such as uploading identity documents, verifying legal entity information or providing additional risk related information.
    Risk specialists: Risk operations teams can monitor risk exposure and intervene in response to signals. Make sure that your operations teams can support connected account owners with questions about risk actions taken on their account.

Reduce the risk of fraudulent merchants using your platform

Before going live, establish best practices for preventing fraud and managing risk. There’s no foolproof method to detect bad actors. Mitigate fraud risk by following risk management best practices to assess an account’s holistic risk profile. The more you understand your connected account and their business, the better the risk assessment. Stripe recommends that you:

    Verify your connected accounts before they can do business through your platform.
    Examine an account’s online presence through social or professional profiles such as Facebook, X (formerly Twitter), or LinkedIn.
    Closely review the account’s website, including considering whether it’s appropriate for them to have one.
    Collect any appropriate licenses for their business.
    Confirm their email address if it’s linked to their business domain. For example, send an email to an address at that domain and require a response from it.
    Collect and verify platform-appropriate information such as a physical address, inventory list, or selling history.
    Monitor activity on your platform to get a sense of typical behavior, which you can use to identify future suspicious behavior.
    Pause payments or payouts when suspicious behavior is detected.
    Use the built-in fraud tools to identify and prevent fraud on individual charge attempts. For information on how Radar works with Connect, see Using Radar with Connect.
    Add additional verifications to Connect onboarding and disable payouts or payments until the checks pass.

If you suspect that a connected account is committing fraud, Stripe recommends rejecting that account. That reduces losses by preventing the account from receiving more funds and helps improve Stripe’s fraud detection systems.
Prevent account take-overs

Bad actors can target your connected accounts and compromise them, an attack known as account takeover (ATO). Attackers commonly obtain account credentials using methods like phishing, data breaches, and guessable passwords. They use the credentials to create unauthorized transactions and other fraudulent activities on the account. To help prevent account takeovers, it’s good practice to:

    Require two-factor authentication when your connected account users log in
    Educate your connected accounts about phishing and other vulnerabilities
    Enforce unique password policies
    Monitor anomalous login activity, especially when it involves new device identifiers or IP addresses
    Monitor changes to sensitive account data such as passwords, email addresses, and bank account information that originates from new devices
    Use identity checks to assist in two-factor authentication recovery or in response to suspicious activity

Mitigate credit risks

Managing disputes and chargebacks are a normal part of doing business when accepting card payments. To build an effective strategy for preventing disputes, employ a number of different methods. The following subsections contain some recommendations to help you manage your exposure, protect your business, and support your accounts.
Account monitoring

Monitor your accounts. The more you understand your connected account and their business, the better you can assess their risk.

    Examine connected account balances through the API or the Dashboard. In the Dashboard’s accounts overview, use filters to investigate accounts that might require you to take action, such as accounts with negative balances.
    Review financial activity on an account. When viewing the account in the Dashboard, click View financial reports in the Activity card.
    Create alerts to monitor riskier accounts so you can quickly adjust your strategies. Riskier accounts have higher dispute rates (dispute activity above 0.75% is generally considered excessive), sharply reduced volume, or negative balances.

Riskier accounts

For newer sellers or service providers that might be riskier, consider delaying or holding payouts until goods or services are delivered. Learn more about account balances and payout scheduling.

For platforms with users on manual payouts, you can update your payout creation logic to defer or slow down payouts for riskier accounts.

For connected accounts that receive automatic payouts, you can slow them by extending the payout schedule on a per-account basis in the Dashboard or by setting settings.payouts.schedule in the API. When viewing the account in the Dashboard, click Edit payout schedule in the Balance card’s overflow menu

:
Edit the payout schedule in the Stripe Dashboard
Impact from chargebacks and negative balances

Consider product or service refunds instead of having to manage chargebacks and negative balances. It might be better for the customer and also less expensive for you. Your options include:

    Issue refunds. You can check whether the connected account’s balance can cover the refund using the Dashboard or by retrieving it using the API. If their balance can’t cover the refund, you can reverse the transfer without issuing the refund, which results in a negative balance on the account.
    Issue refunds based on certain parameters. For example, you can wait until the account’s balance is no longer negative to issue refunds or immediately issue the refund knowing that future payments can cover the amount.
    Proactively cancel and refund charges that are likely to be disputed. The loss on the transaction might be better for the account than getting a chargeback. In addition, there are costs that come with chargebacks and the potential scrutiny from card networks.
    Permit your team to handle refunds by adding them to your platform account.
    Pause collection of recurring payments for subscriptions that are at high risk for chargebacks. That gives you more control over when to resume the subscription. For example, if your platform offers classes that have been canceled for the next few months, you can pause collection of payments for those classes.
    Protect your platform from negative balances by adding funds to your platform balance.
    If you have access to Stripe Sigma, use it to generate a report of each account’s negative balance over time.

Negative balances on accounts Australia Canada Europe (SEPA, UK) New Zealand US

If your connected accounts are in Australia, Canada, Europe (SEPA countries, including the UK), New Zealand, or the US, you can allow Stripe to cover negative balances by automatically debiting their external accounts. In New Zealand, automatic debiting is only supported for connected accounts where Stripe is responsible for collecting updated information when requirements are due or change (including Standard and Express accounts). Otherwise, connected accounts can cover negative balances with future payment volume.

By default, automatic debiting is set to false for connected accounts where the platform is responsible for collecting updated information when requirements are due or change (including Custom accounts). You can toggle the automatic debits setting on an account using the Dashboard or by setting debit_negative_balances using the API.

From the Dashboard, select an account and open the Balance card’s overflow menu (

). You can view all connected accounts that have the automatic debits setting turned off by using the Debit negative balances filter:
Stripe Dashboard using the Debit negative balances filter
Use Stripe’s tools to manage merchant risks

Stripe provides platforms with several tools to monitor and manage risk.

Loss prevention tools

    Debit Negative Balances: For connected accounts in certain countries, you can allow Stripe to automatically debit their external accounts to cover negative balances. Otherwise, negative balances can be covered by future payment volume. You can toggle the automatic debits setting on an account using the Dashboard or by setting debit_negative_balances using the Accounts API.

    Set payout timing: You can set default delay_days for payouts to connected accounts that are considered risky or are located in countries with higher fraud rates.

Additional risk signals

    Identity: Streamline risk processes by providing ID verification during onboarding or prior to enabling payouts.
    Financial Connections: Minimize fraud by matching bank account ownership with the identity of a connected account user before accepting payments or payouts. Fully underwrite accounts with a deep understanding of balance and transaction data.

Actioning

    Pause payouts: In the Dashboard, you can pause payouts as a first line of defense after you identify suspicious activity. Pausing payouts stops a connected account from completing payouts to their bank account.
    Pause payments: In the Dashboard, you can pause payments as a second line of defense. Pausing payments on a suspicious connected account limits your exposure by stopping it from collecting payments through your platform.
    Reject account: You can use the API or Dashboard to remove fraudulent or risky connected accounts from your platform. Rejecting an account is permanent and should only be used as the last line of defense.