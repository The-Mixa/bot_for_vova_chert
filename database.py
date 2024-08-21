from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy import (
    String,
    BigInteger,
    Integer,
    Column,
    Text,
    DateTime,
    Boolean,
)
from sqlalchemy.sql import func
import datetime

user = "root"
password = "vukSTxKmPMF"
host = "213.226.127.94"
db_name = "buys_mp"
DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db_name}"

engine = create_engine(DATABASE_URL, pool_size=1000000, max_overflow=2000000)
Base = declarative_base()



class Order2(Base):
    __tablename__ = "order-2"
    id = Column("id", BigInteger(), primary_key=True)
    article = Column("article", BigInteger(), nullable=True)
    search_key = Column("search_key", String(300), nullable=True)
    size = Column("size", String(32), nullable=True)
    account = Column("account", Integer(), nullable=True)
    price = Column("price", Integer(), nullable=True)
    buyer_id = Column("buyer_id", Integer(), nullable=True)
    status = Column("status", Integer(), nullable=True)
    date_buy = Column("date_buy", DateTime())
    review_text = Column("review_text", Text())
    review_data = Column("review_data", DateTime())
    pvz = Column("pvz", Integer(), nullable=True)
    marketplace = Column("marketplace", Text())
    date_create = Column("date_create", DateTime())
    date_get = Column("date_get", DateTime())
    brand = Column("brand", Text())
    photo = Column("photo", String(255), nullable=True)
    sex = Column("sex", Text())

class Order(Base):
    __tablename__ = "order"
    id = Column("id", BigInteger(), primary_key=True)
    article = Column("article", BigInteger(), nullable=True)
    search_key = Column("search_key", String(300), nullable=True)
    size = Column("size", String(32), nullable=True)
    account = Column("account", Integer(), nullable=True)
    price = Column("price", Integer(), nullable=True)
    buyer_id = Column("buyer_id", Integer(), nullable=True)
    status = Column("status", Integer(), nullable=True)
    date_buy = Column("date_buy", DateTime())
    review_text = Column("review_text", Text())
    review_data = Column("review_data", DateTime())
    pvz = Column("pvz", Integer(), nullable=True)
    marketplace = Column("marketplace", Text())
    date_create = Column("date_create", DateTime())
    date_get = Column("date_get", DateTime())
    brand = Column("brand", Text())
    photo = Column("photo", String(255), nullable=True)
    sex = Column("sex", Text())
    qr_code = Column("qr_code", Text(), nullable = True)
    date_check = Column("date_check", DateTime(), nullable=True)


class WorkBd:
    def __init__(self, engine):
        self.engine = engine

    def create_session(self):
        Session = sessionmaker()
        session = Session(bind=engine)
        return session
    
    def get_pvz(self):
        session = self.create_session()
        pvzs = session.query(Pvz).all()
        session.close()
        return pvzs
    
    def get_qr(self, pvz_text):
        session = self.create_session()
        pvz = session.query(Pvz).filter(Pvz.Path == pvz_text).first()
        now = datetime.datetime.now()
        start_of_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        order = session.query(Order).filter(Order.status == 3).filter(Order.marketplace == 'WB').filter(Order.date_check>= start_of_day).order_by(func.random()).first()
        orders = session.query(Order).filter(Order.pvz == pvz.Id).filter(Order.marketplace == 'WB').filter(Order.account == order.account).filter(Order.status == 3).filter(Order.date_check>= start_of_day).all()
        for ord in orders:
            ord.status = 4
        qr = order.qr_code
        amo = len(orders)
        session.commit()
        session.close()
        return {"qr": qr, "amount": amo}
    
class new_sms_tink(Base):
    __tablename__ = "sms_tinkoff"

    Id = Column(Integer, primary_key=True)
    Sms = Column(String)
    Code = Column(String)
    is_used = Column(Boolean)
    Date = Column(DateTime)
    
class User(Base):
    __tablename__ = "user"
    username = Column("username", String(255))
    id = Column("id", BigInteger(), primary_key=True)
    username = Column("username", BigInteger(), nullable=True)
    password = Column("password", String(100), nullable=True)
    email = Column("email", String(100), nullable=True)
    first_name = Column("first_name", Text())
    last_name = Column("last_name", Text())
    is_active = Column("is_active", Boolean(), nullable=True)
    is_superuser = Column("is_superuser", Boolean(), nullable=True)
    date_joined = Column(
        "date_joined", DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    last_login = Column(
        "last_login", DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    phone = Column("phone", BigInteger(), nullable=True)
    money = Column("money", Integer(), nullable=True)
    who_added_last_money = Column("who_added_last_money", Integer(), nullable=True)
    is_registered = Column("is_registered", Boolean(), nullable=True)
    is_authenticated = Column("is_authenticated", Boolean(), nullable=True)


class Tg_user(Base):
    __tablename__ = "tg_user"

    id = Column("id", Integer(), primary_key=True)
    tg_id = Column("tg_id", BigInteger(), nullable=False)
    id_user = Column("user_id", BigInteger(), nullable=False)


class modems(Base):
    __tablename__ = "modems"

    Id = Column(Integer, primary_key=True)
    Ip = Column(String)
    Is_using = Column(Boolean)
    To_reboot = Column(Boolean)


class open_accs(Base):
    __tablename__ = "open_accounts_wb"

    Id = Column(Integer, primary_key=True)
    Id_account = Column(Integer)
    Date_open = Column(DateTime)
    Id_proxy = Column(Integer)
    Ip_address = Column(String)

class Cards(Base):
    __tablename__ = "cards"
    Id = Column("id", Integer, primary_key=True)
    Card = Column("card", String, nullable=True)
    In_work = Column("in_work", Integer)
    Ucid = Column("ucid", Integer)
    Date_get = Column('dateGet', DateTime)
    Update = Column("update", Integer)


class Accounts(Base):
    __tablename__ = "accounts_wb"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    Is_man = Column(Boolean)
    Path = Column(String)
    Path_id = Column(Integer)
    Date_active = Column(DateTime)
    Is_using = Column(Boolean)
    Date_reg = Column(DateTime)

class Pvz(Base):
    __tablename__ = "pvz_wb"
    Id = Column(Integer, primary_key=True)
    Tg_id = Column(String)
    Path = Column(String)
    Is_partner = Column(Boolean)

    def __str__(self):
        return self.Path



Base.metadata.create_all(engine)
