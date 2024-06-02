_This tool has no afiliation, authorisation or collaboration with PayPal __WHATSOEVER__ use this tool at your __OWN__ risk and ensure you read the code. You agree by using this tool that you are __FULLY__ liable for anything and everything that is modified on your paypal account and that this tool is __NOT__ liable for any issues caused._

# PyPal-Cancel-Subs
PyPal-Cancel-Subs is a tool to cancel all automatic payment profiles on a PayPal account. This is for use for business PayPal accounts where the subscriptions are clients that are subbed.

The terms Subscriptions, Recurring Profiles, Automatic Profiles, Automatic Payments, Subs, Automatic Payment Profiles, are all used interchangeably 

# How does this tool work?

This tool uses the paypal transactions api endpoint to fetch all the subscription ID's used from all the transactions in the past 30 days (this can be changed but depends on the max transaction data that can be fetched from the PayPal transactions API), it then for each paypal automatic payment profile, (JSON response  key: ``paypal_reference_id``) cancels the profile under the PayPal developer api.


# How to use:

1. To use this tool you will need python installed

2. You will need to install requests:

   ```pip install requests```

3. Create a paypal API key and secret if you haven't already
4. Modify the ``CLIENT_ID`` and ``CLIENT_SECRET`` variables based on the details from the previous step
5. Run the program!
