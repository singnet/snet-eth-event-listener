from sqlalchemy.exc import SQLAlchemyError
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.models import Contract


class ContractRepository(BaseRepository):
    def get_contracts(self, contract_name=None):
        try:
            query = self.session.query(Contract)
            if contract_name:
                query = query.filter(Contract.contract_name == contract_name)
            contracts_db = query.all()
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        return contracts_db
