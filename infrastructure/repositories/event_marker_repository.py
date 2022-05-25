from datetime import datetime as dt
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.models import EventMarker


class EventMarkerRepository(BaseRepository):
    def get_last_block_no(self, contract_id):
        try:
            event_marker = self.session.query(EventMarker).filter(EventMarker.contract_id == contract_id).first()
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        if not event_marker:
            raise Exception(f"Unable to find event marker for contract {contract_id}.")
        return event_marker.last_block_no

    def update_last_block_no(self, contract_id, last_block_no):
        try:
            event_marker = self.session.query(EventMarker).filter(EventMarker.contract_id == contract_id).first()
            if event_marker:
                event_marker.last_block_no = last_block_no
                event_marker.updated_at = dt.utcnow()
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        if not event_marker:
            raise Exception(
                f"Unable to update event marker with last block_no {last_block_no} for contract {contract_id}.")
        return event_marker.last_block_no
