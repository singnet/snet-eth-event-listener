from datetime import datetime as dt
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.models import RegisteredTopics


class RegisteredTopicsRepository(BaseRepository):
    def get_topic(self, contract_id):
        try:
            topic_db = self.session.query(RegisteredTopics).filter(RegisteredTopics.contract_id == contract_id).first()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        return topic_db