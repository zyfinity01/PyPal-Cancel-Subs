import requests
import logging
import json
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# PayPal API credentials
CLIENT_ID = 'replace this with the client id from developer.paypal.com - create one if you do not have one'
CLIENT_SECRET = 'replace this with the client secret from developer.paypal.com - create one if you do not have one'
# Base URL for token and subscription management
API_BASE = 'https://api.paypal.com'
# Base URL for transaction reporting
TRANSACTION_API_BASE = 'https://api-m.paypal.com'


def get_access_token():
    """ Get access token using client credentials """
    logging.debug("Attempting to get access token")
    url = f"{API_BASE}/v1/oauth2/token"
    headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    response = requests.post(url, headers=headers, auth=(
        CLIENT_ID, CLIENT_SECRET), data={'grant_type': 'client_credentials'})
    if response.ok:
        logging.debug("Access token retrieved successfully")
        return response.json()['access_token']
    else:
        logging.error(f"Failed to get access token: {response.text}")
        return None


def fetch_transactions(access_token, start_date, end_date):
    """ Fetch transactions within a specific date range using the transaction API """
    logging.debug(f"Fetching transactions from {start_date} to {end_date}")
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    params = (
        ('start_date', start_date),
        ('end_date', end_date),
        ('fields', 'all'),
        ('page_size', '500'),
    )
    response = requests.get(
        f"{TRANSACTION_API_BASE}/v1/reporting/transactions", headers=headers, params=params)
    if response.ok:
        data = response.json()
        # Print the entire JSON response to help with debugging
        print("Full JSON response:")
        print(json.dumps(data, indent=4))  

        transactions = [detail['transaction_info']['paypal_reference_id']
                        for detail in data.get('transaction_details', [])
                        if 'paypal_reference_id_type' in detail['transaction_info'] and detail['transaction_info']['paypal_reference_id_type'] == "SUB"]
        logging.debug(f"Transactions fetched: {transactions}")
        return transactions
    else:
        logging.error(f"Failed to fetch transactions: {response.text}")
        return []


def cancel_subscription(access_token, subscription_id):
    """ Cancel a subscription using the regular API """
    logging.debug(f"Cancelling subscription ID: {subscription_id}")
    headers = {'Authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json'}
    url = f"{API_BASE}/v1/billing/subscriptions/{subscription_id}/cancel"
    response = requests.post(url, headers=headers)
    if response.ok:
        logging.info(f"Subscription {subscription_id} cancelled successfully")
    else:
        logging.error(f"Failed to cancel subscription {
                      subscription_id}: {response.text}")


def main():
    access_token = get_access_token()
    if access_token:
        today = datetime.now()
        # Modify the days if you want to use longer data, its possible paypal doesn't store this data however this depends on paypals API when you are using this script
        last_month_start = (today - timedelta(days=30)
                            ).strftime('%Y-%m-%dT00:00:00-0700')

        # Subtract 1.5 days from today for the end_date for timezone considerations with paypal and system time, feel free to modify tolerance
        last_month_end = (today - timedelta(days=1.5)
                          ).strftime('%Y-%m-%dT23:59:59-0700')

        subscription_ids = fetch_transactions(
            access_token, last_month_start, last_month_end)
        for subscription_id in subscription_ids:
            cancel_subscription(access_token, subscription_id)


if __name__ == "__main__":
    main()
