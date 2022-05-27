from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, func, text, DECIMAL
from sqlalchemy.dialects.mysql import JSON, TIMESTAMP, VARCHAR, BIT, TEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import null

Base = declarative_base()
created_at_default = func.current_timestamp()
updated_at_default = func.current_timestamp()


class Contract(Base):
    __tablename__ = "contract"
    id = Column("row_id", Integer, primary_key=True, autoincrement=True)
    environment = Column("environment", VARCHAR(64), nullable=False)
    contract_name = Column("contract_name", VARCHAR(64), nullable=False)
    abi = Column("abi", JSON, nullable=False)
    network_address = Column("network_address", VARCHAR(128), nullable=False)
    start_block_no = Column("start_block_no", Integer, nullable=False)
    blocks_adjustment = Column("blocks_adjustment", Integer, nullable=False)
    created_at = Column("created_at", TIMESTAMP, server_default=created_at_default, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, server_default=updated_at_default, nullable=False)
    event = relationship("Event", backref='contract', lazy='joined')
    event_marker = relationship("EventMarker", backref='contract', lazy='joined')
    registered_topics = relationship("RegisteredTopics", backref='contract', lazy='joined')
    UniqueConstraint(network_address, name="uq_ct")


class EventMarker(Base):
    __tablename__ = "event_marker"
    id = Column("row_id", Integer, primary_key=True, autoincrement=True)
    contract_id = Column("contract_id", Integer, ForeignKey("contract.row_id", ondelete="CASCADE", onupdate="CASCADE"),
                         nullable=False)
    last_block_no = Column("last_block_no", Integer, nullable=False)
    created_at = Column("created_at", TIMESTAMP, server_default=created_at_default, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, server_default=updated_at_default, nullable=False)
    UniqueConstraint(contract_id, name="uq_evtm")


class Event(Base):
    __tablename__ = "event"
    id = Column("row_id", Integer, primary_key=True, autoincrement=True)
    contract_id = Column("contract_id", Integer, ForeignKey("contract.row_id", ondelete="CASCADE", onupdate="CASCADE"),
                         nullable=False)
    contract_name = Column("contract_name", VARCHAR(64), nullable=False)
    event_name = Column("event_name", VARCHAR(64), nullable=False)
    block_no = Column("block_no", Integer, nullable=False)
    data = Column("data", JSON, nullable=False)
    transaction_hash = Column("transaction_hash", VARCHAR(128), nullable=False)
    log_index = Column("log_index", Integer, nullable=False)
    processed = Column("processed", BIT, nullable=True, default=b"0")
    error_code = Column("error_code", Integer, nullable=True, default=null())
    error_msg = Column("error_msg", VARCHAR(256), nullable=True, default="")
    created_at = Column("created_at", TIMESTAMP, server_default=created_at_default, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, server_default=updated_at_default, nullable=False)
    UniqueConstraint(transaction_hash, log_index, name="uq_evt")


class RegisteredTopics(Base):
    __tablename__ = "registered_topics"
    id = Column("row_id", Integer, primary_key=True, autoincrement=True)
    contract_id = Column("contract_id", Integer, ForeignKey("contract.row_id", ondelete="CASCADE", onupdate="CASCADE"),
                         nullable=False)
    topic_name = Column("topic_name", VARCHAR(64), nullable=False)
    arn = Column("arn", VARCHAR(128), nullable=False)
    created_at = Column("created_at", TIMESTAMP, server_default=created_at_default, nullable=False)
    updated_at = Column("updated_at", TIMESTAMP, server_default=updated_at_default, nullable=False)
    UniqueConstraint(contract_id, arn, name="uq_rt")
