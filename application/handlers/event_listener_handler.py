from constant import Status
from common.logger import get_logger
from application.services.event_listener import EventListener
from application.services.trigger_listener import TriggerListener

logger = get_logger(__name__)


def listen_to_ethereum_events(event, context):
    contract_name = event["contract_name"]
    status = Status.SUCCESS
    try:
        event_listener = EventListener(contract_name=contract_name)
        event_listener.fetch_events()
    except Exception as e:
        status = Status.FAILED
        logger.info(f"Exception from service listen_to_ethereum_events:: {repr(e)}")
    return {"status": status}


def monitor_events(event, context):
    try:
        status = TriggerListener().trigger_listener_for_all_the_contracts()
    except Exception as e:
        status = Status.FAILED
        logger.info(f"Exception from service monitor_events:: {repr(e)}")
    return {"status": status}
