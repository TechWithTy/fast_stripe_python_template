Best practices for integrating Stripe Billing with your SaaS
Ben Sears
Ben Sears
5 min read
·
Sep 19, 2018

Stripe has quickly become one of the leading billing solutions on the market, especially preferred by businesses selling Software-as-a-Service. By reading this guide you will understand how to ensure PCI compliance and the best way to build front-end and back-end integration with Stripe.
Security — Ensure PCI Compliance
The Stripe PCI Compliance Dashboard

Any company that stores, transfers, or processes credit card data must adhere to the Payment Card Industry (PCI) Data Security Standards. If you integrate with Stripe using their security standards, you will automatically qualify as PCI compliant and they will automatically generate the required Self Assessment Questionaire (SAQ) and Attestation of Compliance which you can download from your compliance dashboard. Stripe recommends adhering to the following items to remain PCI compliant:

    Use Checkout, Stripe.js and Elements, or our mobile SDK libraries to collect payment information, which is securely transmitted directly to Stripe without it passing through your servers

    Serve your payment pages securely using Transport Layer Security (TLS) so that they make use of HTTPS

    Review and validate your account’s PCI compliance annually

When integrating with the Stripe API, the secret keys you use must be stored in a safe place. Avoid storing keys in version control; this could lead to a security breach of customer data and could cause massive problems for your business.
Front-end — Use Stripe Elements
An Example Site Using Stripe Elements

For a SaaS, Stripe Elements is a great tool to create a great checkout page customized to fit your specific use-case. They have pre-built UI components such as credit card input and payment buttons. These handle credit card data while maintaining PCI compliance by sending the data directly to Stripe — without it having to pass through your own servers. They are responsive to screen size, customizable to fit your business’s style, and can be localized to your customers’ preferred language.

Stripe Elements is only a tool to give customers a way to enter payment information. As a SaaS company you still need to develop a front-end solution to handle other functions, such as when a customer upgrades or downgrades to a different subscription plan, cancels their service, or resubscribes.
Back-end — Use a Stripe API Library and Webhooks

A Stripe integration on the back-end consists of two parts: an active integration and a reactive integration. Active being direct calls to the Stripe API to perform actions like cancelling a subscription and Indirect being event handlers that respond to events in Stripe such as a credit card payment failing.

The best way to make API calls is to use an official Stripe API library. With this you can start building logic needed to handle all the use-cases you want to cover for your particular SaaS.

Webhooks are API calls that Stripe can send to an endpoint of your choice to alert you when events happen in Stripe. This is most useful for allowing you to respond to payment failures and automatically restricting access to your app when a customer’s credit card is failing.

When building your integration, be mindful of the following:

    Keep your Stripe secret key out of version control to prevent your Stripe account from being hacked
    Do all development using Stripe test keys, ensuring you do not break your production customer data
    When using webhooks, check the Stripe signature to ensure the requests are valid
    Make sure your integration keeps a 1 to 1 mapping of user in your database to customer in Stripe. Some businesses mistakenly create multiple customers using the same email and this can cause issues when trying to make more complex integration code later on.
    Lock the API version to what you developed and tested with; Stripe can change their API and break your code if you are not locked on a specific version; here’s how you do it.

Using a Stripe Partner to avoid development
Servicebot Generates PCI Compliant UI Components connected to Stripe

Stripe does a lot out of the box, but most SaaS companies will need more than just the bare bones. Features such as pricing pages and billing settings pages where customers can manage their own subscriptions.

If you don’t want to spend a lot of resources developing and maintaining your own integration with Stripe, there are Stripe verified partners which can provide a ready-made integration you can drop-into your app. Servicebot makes it easy to connect your SaaS to Stripe without spending time developing by generating embeddable components such as pricing pages, billing management, and check-out pages.
Conclusion

When building a Stripe integration for a SaaS, there are a lot of moving parts that need to be built. Developing a front-end using Stripe Elements and a back-end with one of Stripe’s libraries, and handling events sent by Stripe webhooks are the building blocks of a solid Stripe integration.

If you are looking to minimize development on your SaaS billing solution, you should look at Stripe partners such as Servicebot
This story is published in The Startup, Medium’s largest entrepreneurship publication followed by + 370,107 people.
Subscribe to receive our top stories here.
Payments
Stripe
SaaS
Entrepreneurship
Startup

The Startup
Published in The Startup
844K Followers
·
Last published 2 days ago

Get smarter at building your thing. Follow to join The Startup’s +8 million monthly readers & +772K followers.
Ben Sears
Written by Ben Sears
684 Followers
·
3 Following

Founder of https://servicebot.io and Consultant for VMware
Responses (2)
CodingOni
CodingOni

﻿
Radhika Tekumalla

Radhika Tekumalla

Apr 10, 2020

Good read on integrating a 3rd party library to reduce dev time. I’m curious what your thoughts are on Stripe overall — using as-is vs Servicebot. Having built an e-commerce marketplace using Stripe, here’s mine- https://medium.com/@tradhikarao/confessions-of-a-stripe-aholic-4dc2d5b44a6e