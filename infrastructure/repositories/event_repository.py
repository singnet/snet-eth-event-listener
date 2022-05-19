from datetime import datetime as dt
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.models import Event


class EventRepository(BaseRepository):
    def update_events(self, contract_id, contract_name, raw_events):
        events_db = []
        for event in raw_events:
            events_db.append(
                Event(
                    contract_id=contract_id,
                    contract_name=contract_name,
                    event_name=event["event"],
                    block_no=event["blockNumber"],
                    data=str(dict(event["args"])),
                    transaction_hash=event["transactionHash"].hex(),
                    log_index=event["logIndex"],
                    created_at=dt.utcnow(),
                    updated_at=dt.utcnow()
                )
            )
        self.add_all_items(events_db)
