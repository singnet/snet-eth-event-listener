from datetime import datetime as dt
from unittest import TestCase
from unittest.mock import patch
from application.handlers.event_listener_handler import listen_to_ethereum_events, monitor_events
from infrastructure.repositories.contract_repository import ContractRepository
from infrastructure.repositories.event_marker_repository import EventMarkerRepository
from infrastructure.repositories.event_repository import EventRepository
from infrastructure.models import Contract, EventMarker, Event
from config import ETHEREUM_ENVIRONMENT
from constant import Status
from testcases.functional_testcases.test_data import RegistryContractData

contract_repo = ContractRepository()
event_marker_repo = EventMarkerRepository()
event_repo = EventRepository()


class TestEthereumListener(TestCase):
    def setUp(self):
        self.tearDown()
        contract_repo.add_item(
            Contract(
                environment=ETHEREUM_ENVIRONMENT,
                contract_name=RegistryContractData.name,
                abi=RegistryContractData.abi,
                contract_address=RegistryContractData.contract_address,
                contract_creation_block_no=RegistryContractData.contract_creation_block_no,
                blocks_adjustment=RegistryContractData.blocks_adjustment,
                created_at=dt.utcnow(),
                updated_at=dt.utcnow()
            )
        )
        contracts = contract_repo.get_contracts()
        event_marker_repo.add_item(
            EventMarker(
                contract_id=contracts[0].id,
                last_block_no=RegistryContractData.last_block_no,
                created_at=dt.utcnow(),
                updated_at=dt.utcnow()
            )
        )

    @patch("common.blockchain_util.BlockChainUtil.get_current_block_no")
    @patch("common.blockchain_util.BlockChainUtil.create_contract_instance")
    @patch("application.services.event_listener.EventListener.get_events")
    def test_listen_to_ethereum_events(self, mock_events, mock_contract_instance, mock_current_block_no):
        event = {"contract_name": RegistryContractData.name}
        mock_current_block_no.return_value = RegistryContractData.last_block_no + 100
        mock_contract_instance.return_value = None
        mock_events.return_value = [dict({'args': dict({'orgId': b'test-org\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}), 'event': 'OrganizationCreated', 'logIndex': 34, 'transactionIndex': 21, 'transactionHash': bytes.fromhex('c5faf4d06da986f4e83d46b5c6e06d37f83694359c7600b1ea9d9299ebdf34f8'), 'address': '0xB12089BD3F20A2C546FAad4167A08C57584f89C8', 'blockHash': bytes.fromhex('becbb196787436c1917fe33404ca3974a27ead05847168ea30cbfac5b4f94166'), 'blockNumber': 10908547})]
        self.tearDown()
        self.setUp()
        response = listen_to_ethereum_events(event, None)
        assert(response["status"] == Status.SUCCESS)
        events = event_repo.get_events()
        assert(len(events) == 1)

    @patch("common.boto_utils.BotoUtils.invoke_lambda")
    def test_monitor_events(self, mock_event_listener_response):
        mock_event_listener_response.return_value = {"StatusCode": 202}
        response = monitor_events(None, None)
        assert(response == [{RegistryContractData.name: {"status": Status.SUCCESS}}])

    def tearDown(self):
        contract_repo.session.query(Contract).delete()
        event_marker_repo.session.query(EventMarker).delete()
        event_repo.session.query(Event).delete()
        contract_repo.session.commit()
        event_marker_repo.session.commit()
        event_repo.session.commit()
