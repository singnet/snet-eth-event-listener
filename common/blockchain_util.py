from web3 import Web3
from config import EthereumNetwork, HttpProvider
from common.logger import get_logger

logger = get_logger(__name__)


class BlockChainUtil:
    def __init__(self):
        self.provider_class = eval(EthereumNetwork.default_provider)
        self.provider_url = getattr(self.provider_class, "connection_url")
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

    def create_contract_instance(self, abi, network_address):
        self.test_connection()
        return self.web3_object.eth.contract(abi=abi, address=network_address)

    def get_transaction_receipt(self, transaction_hash):
        self.test_connection()
        return self.web3_object.eth.get_transaction_receipt(transaction_hash)
