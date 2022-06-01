from datetime import datetime as dt
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.models import Event


class EventRepository(BaseRepository):
    def add_events(self, contract_id, contract_name, raw_events):
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
                    processed=0,
                    error_code=0,
                    error_msg="",
                    created_at=dt.utcnow(),
                    updated_at=dt.utcnow()
                )
            )
        self.add_all_items(events_db)

    def get_events(self):
        try:
            events_db = self.session.query(Event).all()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        return events_db

    def get_unprocessed_events(self, contract_id, limit):
        try:
            events_db = self.session.query(Event).\
                filter(Event.contract_id == contract_id).\
                filter(Event.processed == 0).\
                order_by(Event.block_no).limit(limit).all()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        return events_db

    def mark_event_as_processed(self, event_id):
        try:
            event_db = self.session.query(Event).filter(Event.id == event_id).first()
            if event_db:
                event_db.processed = 1
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        return event_db
