from constant import Status
from application.services.event_listener import EventListener
from application.services.trigger_listener import TriggerListener


def listen_to_ethereum_events(event, context):
    contract_name = event["contract_name"]
    status = Status.SUCCESS
    try:
        event_listener = EventListener(contract_name=contract_name)
        event_listener.fetch_events()
    except Exception as e:
        status = Status.FAILED
    return {"status": status}


def monitor_events(event, context):
    try:
        status = TriggerListener().trigger_listener_for_all_the_contracts()
    except Exception as e:
        status = Status.FAILED
        # slack alert
    return {"status": status}
