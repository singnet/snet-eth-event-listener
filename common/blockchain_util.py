import web3
import io
import json
from web3 import Web3
from config import EthereumNetwork, HttpProvider, WebSocketProvider


class BlockChainUtil:
    def __init__(self):
        provider_class = eval(EthereumNetwork.default_provider)
        self.provider_url = getattr(provider_class, "connection_url")
        self.provider = getattr(Web3, getattr(provider_class, "web3_class"))(self.provider_url)
        self.web3_object = Web3(self.provider)

    def test_connection(self):
        connected = True
        try:
            connected = self.web3_object.isConnected()
        except Exception as e:
            connected = False
        if not connected:
            self.reset_connection()

    def reset_connection(self):
        self.provider = getattr(Web3, getattr(EthereumNetwork.default_provider, "web3_class"))(self.provider_url)
        self.web3_object = Web3(self.provider)

    def get_current_block_no(self):
        return self.web3_object.eth.blockNumber

    def create_contract_instance(self, abi, network_address):
        return self.web3_object.eth.contract(abi=json.dumps(abi), address=network_address)

    def get_transaction_receipt(self, transaction_hash):
        return self.web3_object.eth.getTransactionReceipt(transaction_hash)
