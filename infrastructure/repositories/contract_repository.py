from sqlalchemy.exc import SQLAlchemyError
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.models import Contract


class ContractRepository(BaseRepository):
    def get_contract(self, contract_name):
        try:
            contract = self.session.query(Contract).filter(Contract.contract_name == contract_name).first()
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
        return contract
