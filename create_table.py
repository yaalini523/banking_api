from db import Base, engine
from models import AccountHolder, Account, Transaction

Base.metadata.create_all(bind=engine)
