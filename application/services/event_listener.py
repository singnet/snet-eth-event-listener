from config import EVENT_FETCH_LIMIT
from common.blockchain_util import BlockChainUtil
from infrastructure.repositories.contract_repository import ContractRepository
from infrastructure.repositories.event_marker_repository import EventMarkerRepository
from infrastructure.repositories.event_repository import EventRepository

blockchain_util = BlockChainUtil()

contract_repo = ContractRepository()
event_marker_repo = EventMarkerRepository()
event_repo = EventRepository()


class EventListener:
    def __init__(self, contract_name):
        blockchain_util.test_connection()
        contracts = contract_repo.get_contracts(contract_name)
        self.contract = contracts[0] if contracts else None
        if not self.contract:
            raise Exception(f"Unable to find contract for given contract name {contract_name}.")
        self.contract_instance = blockchain_util.create_contract_instance(abi=self.contract.abi,
                                                                          network_address=self.contract.network_address)

    def fetch_events(self):
        contract_id = self.contract.id

        # get last processed block no from EventMarkerTable
        last_processed_block_no = event_marker_repo.get_last_block_no(contract_id)

        # compute start_block_no and end_block_no
        start_block_no = last_processed_block_no
        end_block_no = self.calculate_end_block_no(last_processed_block_no)

        # fetch events from blockchain
        raw_events = self.get_events(start_block_no, end_block_no)

        # update events table
        event_marker_repo.update_last_block_no(contract_id, end_block_no)
        event_repo.update_events(contract_id, self.contract.contract_name, raw_events)

    def calculate_end_block_no(self, last_processed_block_no):
        blocks_adjustment = self.contract.blocks_adjustment
        current_block_no = blockchain_util.get_current_block_no()
        end_block_no = last_processed_block_no + EVENT_FETCH_LIMIT - 1
        if end_block_no > (current_block_no - blocks_adjustment):
            end_block_no = current_block_no - blocks_adjustment
        return end_block_no

    def get_events(self, start_block_no, end_block_no):
        events = []
        for attributes in self.contract_instance.events.abi:
            if attributes['type'] == 'event':
                event_name = attributes['name']
                event_object = getattr(self.contract_instance.events, event_name)
                blockchain_events = event_object.createFilter(fromBlock=start_block_no,
                                                              toBlock=end_block_no).get_all_entries()
                events.extend(blockchain_events)
        return events
