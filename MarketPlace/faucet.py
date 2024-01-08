#faucet.py
import requests
import logging
import json

class Faucet:
    def __init__(self, node):
        self.node = node
        self.logger = logging.getLogger(__name__)

    def request_funds(self, address, amount):
        faucet_url = f"{self.node}/faucet"
        try:
            response = requests.post(faucet_url, json={"address": address, "amount": amount})
            response.raise_for_status()

            if response.status_code == 200:
                return "Funds requested successfully"
            elif response.status_code == 400:
                try:
                    error_message = response.json().get('error')
                    return f"Bad request. Error: {error_message}"
                except json.JSONDecodeError:
                    return "Bad request. Check the address format."
            elif response.status_code == 404:
                return "Endpoint not found. Check the server configuration."
            elif response.status_code == 500:
                return "Internal server error. Try again later."
            else:
                return f"Unexpected response: {response.status_code}"
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error: {e}")
            return f"An unexpected error occurred. Check the logs for more information."

# Usage example
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # Set the logging level as needed

    node_url = "http://127.0.0.1:5000"  # Replace with your blockchain node URL
    faucet = Faucet(node_url)
    address = "0x2B69b4C80f4b4BFEae8A5fC04e9E70fE09DD7885"
    amount = 10  # Amount of funds to request
    result = faucet.request_funds(address, amount)
    print(result)
