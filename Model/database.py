import datetime
import os
from sqlalchemy import create_engine, String,Integer,DateTime
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

dotenv = load_dotenv()
database_url = f"{os.getenv('DB_CONNECTION')}://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_DATABASE')}"
engine = create_engine(database_url, echo=True)

class Base(DeclarativeBase):
    pass

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))

class SellHeader(Base):
    __tablename__ = "sell_headers"
    id:Mapped[int] = mapped_column(primary_key=True)
    date:Mapped[datetime.datetime] = mapped_column(DateTime)
    number:Mapped[int] = mapped_column(Integer)

class Parts(Base):
    __tablename__ = "parts"
    id:Mapped[int] = mapped_column(primary_key=True)
    part_number:Mapped[str] = mapped_column(String(150))
    manufacturer_id:Mapped[int] = mapped_column(Integer)
    name:Mapped[str] = mapped_column(String(50))
    type:Mapped[str] = mapped_column(String(50))
    price:Mapped[int] = mapped_column(Integer)
    amount:Mapped[int] = mapped_column(Integer)
    min_amount:Mapped[int] = mapped_column(Integer)
    max_amount:Mapped[int] = mapped_column(Integer)

class Engine(Base):
    __tablename__ = "engines"
    id:Mapped[int] = mapped_column(primary_key=True)
    manufacturer_id:Mapped[int] = mapped_column(Integer)
    horse_power:Mapped[int] = mapped_column(Integer)
    ccc:Mapped[int] = mapped_column(Integer)
    fuel_id:Mapped[int] = mapped_column(Integer)

class Fuel(Base):
    __tablename__="fuels"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))

class Modell(Base):
    __tablename__ = "models"
    id:Mapped[int] = mapped_column(primary_key=True)
    manufacturer_id:Mapped[int] = mapped_column(Integer)
    name:Mapped[str] = mapped_column(String(50))
    generation:Mapped[int] = mapped_column(Integer)
    date:Mapped[datetime.datetime] = mapped_column(DateTime)

class Vehicle(Base):
    __tablename__ = "vehicles"
    id:Mapped[int] = mapped_column(primary_key=True)
    vehicle_type_id:Mapped[int] = mapped_column(Integer)
    modell_id:Mapped[int] = mapped_column(Integer)

class VehicleType(Base):
    __tablename__ = "vehicle_types"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))

class SellItem(Base):
    __tablename__ = "sell_items"
    id:Mapped[int] = mapped_column(primary_key=True)
    sell_header_id:Mapped[int] = mapped_column(Integer)
    part_id:Mapped[int] = mapped_column(Integer)
    amount:Mapped[int] = mapped_column(Integer)
    price:Mapped[int] = mapped_column(Integer)

class Type(Base):
    __tablename__ = "types"
    id:Mapped[int] = mapped_column(primary_key=True)
    modell_id:Mapped[int] = mapped_column(Integer)
    bodytype:Mapped[str] = mapped_column(String)

class Compatibility(Base):
    __tablename__ = "compatibilities"
    id:Mapped[int] = mapped_column(primary_key=True)
    part_id:Mapped[int] = mapped_column(Integer)
    engine_id:Mapped[int] = mapped_column(Integer)

class MotorCompatibility(Base):
    __tablename__ = "motorcompatibilities"
    id:Mapped[int] = mapped_column(primary_key=True)
    modell_id:Mapped[int] = mapped_column(Integer)
    engine_id:Mapped[int] = mapped_column(Integer)

#TODO: A kapcsolatok létrehozása relationshippel



