import datetime
import os
from sqlalchemy import create_engine, String, Integer, DateTime, ForeignKey
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped,mapped_column,sessionmaker
from typing import List


dotenv = load_dotenv()
database_url = f"{os.getenv('DB_CONNECTION')}://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_DATABASE')}"
engine = create_engine(database_url, echo=True)
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(unique=True)
    password:Mapped[str] = mapped_column(String(100))
    email:Mapped[str] = mapped_column(unique=True)
    phone:Mapped[str] = mapped_column(unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship(back_populates="users")
class Role(Base):
    __tablename__ = "roles"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(unique=True)
    users:Mapped[List["User"]] = relationship(back_populates="role", cascade="all, delete-orphan")

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))
    parts:Mapped[List["Parts"]] = relationship(back_populates="manufacturer", cascade="all, delete-orphan")
    engines:Mapped[List["Engine"]] = relationship(back_populates="manufacturer", cascade="all,delete-orphan")
    models:Mapped[List["Modell"]] = relationship(back_populates="manufacturer", cascade="all,delete-orphan")

class SellHeader(Base):
    __tablename__ = "sell_headers"
    id:Mapped[int] = mapped_column(primary_key=True)
    date:Mapped[datetime.datetime] = mapped_column(DateTime)
    number:Mapped[int] = mapped_column(Integer)
    sell_items:Mapped[List["SellItem"]] = relationship(back_populates="sell_header", cascade="all, delete-orphan")

class Parts(Base):
    __tablename__ = "parts"
    id:Mapped[int] = mapped_column(primary_key=True)
    part_number:Mapped[str] = mapped_column(String(150))
    manufacturer_id:Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))
    manufacturer:Mapped["Manufacturer"] = relationship(back_populates="parts")
    sell_items:Mapped[List["SellItem"]] = relationship(back_populates="part", cascade="all, delete-orphan")
    compatibilities:Mapped[List["Compatibility"]] = relationship(back_populates="part", cascade="all, delete-orphan")
    name:Mapped[str] = mapped_column(String(50))
    type:Mapped[str] = mapped_column(String(50))
    price:Mapped[int] = mapped_column(Integer)
    amount:Mapped[int] = mapped_column(Integer)
    min_amount:Mapped[int] = mapped_column(Integer)
    max_amount:Mapped[int] = mapped_column(Integer)

class Fuel(Base):
    __tablename__="fuels"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))
    engines:Mapped[List["Engine"]] = relationship(back_populates="fuel", cascade="all, delete-orphan")

class Engine(Base):
    __tablename__ = "engines"
    id:Mapped[int] = mapped_column(primary_key=True)
    engine_code:Mapped[str] = mapped_column(String(50))
    manufacturer_id:Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))
    manufacturer:Mapped["Manufacturer"] = relationship(back_populates="engines")
    horse_power:Mapped[int] = mapped_column(Integer)
    ccc:Mapped[int] = mapped_column(Integer)
    fuel_id:Mapped[int] = mapped_column(ForeignKey("fuels.id"))
    fuel:Mapped["Fuel"] = relationship(back_populates="engines")
    motor_comps:Mapped[List["MotorCompatibility"]] = relationship(back_populates="engine",cascade="all, delete-orphan")
    compatibilities:Mapped[List["Compatibility"]] = relationship(back_populates="engine", cascade="all, delete-orphan")

class Modell(Base):
    __tablename__ = "models"
    id:Mapped[int] = mapped_column(primary_key=True)
    manufacturer_id:Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))
    manufacturer:Mapped["Manufacturer"] = relationship(back_populates="models")
    name:Mapped[str] = mapped_column(String(50))
    generation:Mapped[int] = mapped_column(Integer)
    date:Mapped[datetime.datetime] = mapped_column(DateTime)
    vehicles:Mapped[List["Vehicle"]] = relationship(back_populates="modell", cascade="all, delete-orphan")
    types:Mapped[List["Type"]] = relationship(back_populates="modell", cascade="all, delete-orphan")
    compatibilities:Mapped[List["Compatibility"]] = relationship(back_populates="modell", cascade="all, delete-orphan")
    motor_comps:Mapped[List["MotorCompatibility"]] = relationship(back_populates="modell", cascade="all, delete-orphan")

class VehicleType(Base):
    __tablename__ = "vehicle_types"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))
    vehicles:Mapped[List["Vehicle"]] = relationship(back_populates="vehicle_type", cascade="all, delete-orphan")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id:Mapped[int] = mapped_column(primary_key=True)
    vehicle_type_id:Mapped[int] = mapped_column(ForeignKey("vehicle_types.id"))
    vehicle_type:Mapped["VehicleType"] = relationship(back_populates="vehicles")
    modell_id:Mapped[int] = mapped_column(ForeignKey("models.id"))
    modell:Mapped["Modell"] = relationship(back_populates="vehicles")

class SellItem(Base):
    __tablename__ = "sell_items"
    id:Mapped[int] = mapped_column(primary_key=True)
    sell_header_id:Mapped[int] = mapped_column(ForeignKey("sell_headers.id"))
    sell_header:Mapped["SellHeader"] = relationship(back_populates="sell_items")
    part_id:Mapped[int] = mapped_column(ForeignKey("parts.id"))
    part:Mapped["Parts"] = relationship(back_populates="sell_items")
    amount:Mapped[int] = mapped_column(Integer)
    price:Mapped[int] = mapped_column(Integer)

class Type(Base):
    __tablename__ = "types"
    id:Mapped[int] = mapped_column(primary_key=True)
    modell_id:Mapped[int] = mapped_column(ForeignKey("models.id"))
    modell:Mapped["Modell"] = relationship(back_populates="types")
    bodytype:Mapped[str] = mapped_column(String)

class Compatibility(Base):
    __tablename__ = "compatibilities"
    id:Mapped[int] = mapped_column(primary_key=True)
    part_id:Mapped[int] = mapped_column(ForeignKey("parts.id"))
    part:Mapped["Parts"] = relationship(back_populates="compatibilities")
    modell_id:Mapped[int] = mapped_column(ForeignKey("models.id"))
    modell:Mapped["Modell"] = relationship(back_populates="compatibilities")
    engine_id:Mapped[int] = mapped_column(ForeignKey("engines.id"))
    engine:Mapped["Engine"] = relationship(back_populates="compatibilities")

class MotorCompatibility(Base):
    __tablename__ = "motorcompatibilities"
    id:Mapped[int] = mapped_column(primary_key=True)
    modell_id:Mapped[int] = mapped_column(ForeignKey("models.id"))
    modell:Mapped["Modell"] = relationship(back_populates="motor_comps")
    engine_id:Mapped[int] = mapped_column(ForeignKey("engines.id"))
    engine:Mapped["Engine"] = relationship(back_populates="motor_comps")

Sessionlocal = sessionmaker(bind=engine)
def seed_roles():
    with Sessionlocal() as session:
        user_role = session.get(Role,1)
        if user_role is None:
            user_role = Role(id=1,name="User")
            session.add(user_role)
            session.commit()
            session.refresh(user_role)
        return user_role
def seed_examples():
    with Sessionlocal() as session:
        session.add(Manufacturer(id=1, name="Ford"))
        session.add(Modell(id=1, name="Mustang",manufacturer_id = 1))
        session.add(Fuel(id=1, name="Gasoline"))
        session.add(Engine(id=1,horse_power=500, ccc=5000, manufacturer_id=1,fuel_id=1))
        session.add(Manufacturer(id=2, name="Ferrari"))
        session.add(Modell(id=2, name="Tessa Rosa", manufacturer_id = 2))
        session.add(Fuel(id=2, name="Sport Fuel"))
        session.add(Engine(id=2,horse_power=690,ccc=6000, manufacturer_id=2, fuel_id=2))
        session.commit()


try:
    Base.metadata.create_all(engine)
    #Base.metadata.drop_all(engine)
    seed_roles()
    print("Successfully created all tables")
except Exception as e:
    print("Failed to create tables", e)