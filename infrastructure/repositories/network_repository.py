from sqlalchemy.exc import SQLAlchemyError
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.models import Blockchain


class NetworkRepository(BaseRepository):
    def get_network(self, network_id=None):
        try:
            query = self.session.query(Blockchain)
            if network_id:
                query = query.filter(Blockchain.chain_id == network_id)
            network_db = query.all()
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        return network_db
