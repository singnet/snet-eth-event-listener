from datetime import datetime as dt
from unittest import TestCase
from unittest.mock import patch

from application.handlers.event_publisher_handler import publish_events
from config import ETHEREUM_ENVIRONMENT
from constant import Status
from infrastructure.models import Contract, EventMarker, Event, RegisteredTopics
from infrastructure.repositories.contract_repository import ContractRepository
from infrastructure.repositories.event_marker_repository import EventMarkerRepository
from infrastructure.repositories.event_repository import EventRepository
from infrastructure.repositories.registered_topics_repo import RegisteredTopicsRepository
from testcases.functional_testcases.test_data import RegistryContractData, EventData

contract_repo = ContractRepository()
event_marker_repo = EventMarkerRepository()
event_repo = EventRepository()
topics_repo = RegisteredTopicsRepository()


class TestEthereumPublisher(TestCase):
    def setUp(self):
        self.tearDown()
        contract_repo.add_item(
            Contract(
                environment=ETHEREUM_ENVIRONMENT,
                contract_name=RegistryContractData.name,
                abi=RegistryContractData.abi,
                network_address=RegistryContractData.contract_address,
                start_block_no=RegistryContractData.contract_creation_block_no,
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
        event_repo.add_item(
            Event(
                contract_id=contracts[0].id,
                contract_name=RegistryContractData.name,
                event_name=EventData.event_name,
                block_no=EventData.block_no,
                data=EventData.data,
                transaction_hash=EventData.transaction_hash,
                log_index=EventData.log_index,
                processed=0,
                error_code=0,
                error_msg="",
                created_at=dt.utcnow(),
                updated_at=dt.utcnow()
            )
        )
        topics_repo.add_item(
            RegisteredTopics(
                contract_id=contracts[0].id,
                topic_name="RegistryPublisherTopic.fifo",
                arn="arn",
                created_at=dt.utcnow(),
                updated_at=dt.utcnow()

            )
        )

    @patch("common.boto_utils.BotoUtils.publish_to_sns_topic")
    def test_publish_events(self, mock_publish_to_sns_topic):
        mock_publish_to_sns_topic.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
        events = event_repo.get_events()
        assert (events[0].processed == 0)
        response = publish_events(None, None)
        assert (response["status"] == Status.SUCCESS)
        events = event_repo.get_events()
        assert (events[0].processed == 1)

    def tearDown(self):
        contract_repo.session.query(Contract).delete()
        event_marker_repo.session.query(EventMarker).delete()
        event_repo.session.query(Event).delete()
        contract_repo.session.commit()
        event_marker_repo.session.commit()
        event_repo.session.commit()
