from infrastructure.repositories.event_repository import EventRepository
from infrastructure.repositories.contract_repository import ContractRepository
from infrastructure.repositories.registered_topics_repo import RegisteredTopicsRepository
from common.boto_utils import BotoUtils
from common.logger import get_logger
from config import EVENT_PUBLISH_LIMIT, AWS_REGION

boto_util = BotoUtils(region_name=AWS_REGION)
logger = get_logger(__name__)


class EventPublisher:
    def __init__(self):
        pass

    def manage_publish_events(self):
        contracts = ContractRepository().get_contracts()
        for contract in contracts:
            events = EventRepository().get_unprocessed_events(contract.id, limit=EVENT_PUBLISH_LIMIT)
            topic = RegisteredTopicsRepository().get_topic(contract.id)
            self.publish_event(topic.arn, events)

    def publish_event(self, arn, events):
        for event in events:
            logger.info(f"Processing block_no {event.block_no} | contract {event.contract_name} | transaction_hash {event.transaction_hash} | log_index {event.log_index}")
            payload = {
                "blockchain_name": "Binance",
                "blockchain_event": {
                    "data": {
                        "row_id": event.id,
                        "block_no": event.block_no,
                        "uncle_block_no": event.block_no,
                        "json_str": event.data,
                        "processed": event.processed,
                        "transactionHash": event.transaction_hash,
                        "logIndex": event.log_index,
                        "error_code": event.error_code,
                        "error_msg": event.error_msg,
                        "row_updated": str(event.updated_at),
                        "row_created": str(event.created_at),
                    },
                    "name": event.event_name
                }
            }
            message_group_id = event.event_name
            message_deduplication_id = str(event.id)
            response = boto_util.publish_to_sns_topic(arn, payload, message_group_id, message_deduplication_id)
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                EventRepository().mark_event_as_processed(event_id=event.id)
            else:
                # report slack
                break
