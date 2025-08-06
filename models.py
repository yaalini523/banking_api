from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class AccountHolder(Base):
    __tablename__ = 'AccountHolder' 

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    aadhaar_number = Column(String, unique=True, nullable=False)
    status = Column(String, default='Active')

    accounts = relationship("Account", back_populates="holder")


class Account(Base):
    __tablename__ = 'Account'  

    id = Column(Integer, primary_key=True)
    account_number = Column(String, unique=True, nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    status = Column(String, default='Active')
    holder_id = Column(Integer, ForeignKey('AccountHolder.id')) 

    holder = relationship("AccountHolder", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = 'Transaction'  

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('Account.id'))  
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    source_account_id = Column(Integer)
    destination_account_id = Column(Integer)

    account = relationship("Account", back_populates="transactions")
