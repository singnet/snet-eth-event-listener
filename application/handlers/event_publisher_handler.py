import sys

sys.path.append('/opt')

from common.logger import get_logger
from constant import Status
from application.services.event_publisher import EventPublisher

logger = get_logger(__name__)


def publish_events(event, context):
    logger.info("Publish event to topic.")
    EventPublisher().manage_publish_events()
    return {"status": Status.SUCCESS}
