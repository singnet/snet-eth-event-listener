import json
from web3 import Web3
from config import EthereumNetwork, HttpProvider
from common.logger import get_logger
from infrastructure.repositories.network_repository import NetworkRepository
# todo: get networks settings from database
# rpc
logger = get_logger(__name__)
network_repository = NetworkRepository()

class BlockChainUtil:
    def __init__(self, network_id: int):
        self.provider_class = eval(EthereumNetwork.default_provider)
        network = network_repository.get_network(network_id)
        self.provider_url = network.rpc_provider
        self.provider = getattr(Web3, getattr(self.provider_class, "web3_class"))(self.provider_url)
        self.web3_object = Web3(self.provider)

    def test_connection(self):
        try:
            connected = self.web3_object.is_connected()
            assert connected, "Failed connection in test_connection"
        except Exception as e:
            logger.info(f"Error while testing web3 connection {repr(e)}")

    def reset_connection(self):
        self.provider = getattr(Web3, getattr(self.provider_class, "web3_class"))(self.provider_url)
        self.web3_object = Web3(self.provider)

    def get_current_block_no(self):
        self.test_connection()
        return self.web3_object.eth.block_number

    def create_contract_instance(self, abi, address):
        self.test_connection()
        return self.web3_object.eth.contract(abi=json.dumps(abi), address=address)

    def get_transaction_receipt(self, transaction_hash):
        self.test_connection()
        return self.web3_object.eth.get_transaction_receipt(transaction_hash)
