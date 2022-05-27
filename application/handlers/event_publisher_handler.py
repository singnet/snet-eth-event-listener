from common.logger import get_logger
from constant import Status

logger = get_logger(__name__)


def consume_event_from_publisher(event, context):
    logger.info(f"Event {event} from publisher.")
    return {"status": Status.SUCCESS}