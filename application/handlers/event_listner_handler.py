from constant import Status
from application.services.event_listner import EventListener


def listen_to_ethereum_events(event, context):
    contract_name = event["contract_name"]
    status = Status.SUCCESS
    try:
        event_listener = EventListener(contract_name=contract_name)
        event_listener.fetch_events()
    except Exception as e:
        status = Status.FAILED
    return {"status": status}
