import datetime
import os

import bcrypt
from sqlalchemy import create_engine, String, Integer, DateTime, ForeignKey, func, Column, text
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
    transaction_logs:Mapped[List["TransactionLog"]] = relationship(back_populates="users", cascade="all, delete-orphan")

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

class VehicleBrand(Base):
    __tablename__ = "vehiclebrands"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(unique=True)
    country:Mapped[str] = mapped_column(String(100))
    models:Mapped[List["Modell"]] = relationship(back_populates="vehicleBrand", cascade="all,delete-orphan")
    engines:Mapped[List["Engine"]] = relationship(back_populates="vehicleBrand", cascade="all,delete-orphan")

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
    transaction_logs:Mapped[List["TransactionLog"]] = relationship(back_populates="part", cascade="all, delete-orphan")
    name:Mapped[str] = mapped_column(String(50))
    type:Mapped[str] = mapped_column(String(50))
    price:Mapped[int] = mapped_column(Integer)
    amount:Mapped[int] = mapped_column(Integer)
    min_amount:Mapped[int] = mapped_column(Integer)
    max_amount:Mapped[int] = mapped_column(Integer)
    image_path = Column(String, nullable = True)

class Fuel(Base):
    __tablename__="fuels"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(50))
    engines:Mapped[List["Engine"]] = relationship(back_populates="fuel", cascade="all, delete-orphan")

class Engine(Base):
    __tablename__ = "engines"
    id:Mapped[int] = mapped_column(primary_key=True)
    engine_code:Mapped[str] = mapped_column(String(50))
    vehicleBrand_id:Mapped[int] = mapped_column(ForeignKey("vehiclebrands.id"))
    vehicleBrand:Mapped["VehicleBrand"] = relationship(back_populates="engines")
    horse_power:Mapped[int] = mapped_column(Integer)
    ccc:Mapped[int] = mapped_column(Integer)
    fuel_id:Mapped[int] = mapped_column(ForeignKey("fuels.id"))
    fuel:Mapped["Fuel"] = relationship(back_populates="engines")
    motor_comps:Mapped[List["MotorCompatibility"]] = relationship(back_populates="engine",cascade="all, delete-orphan")
    compatibilities:Mapped[List["Compatibility"]] = relationship(back_populates="engine", cascade="all, delete-orphan")

class Modell(Base):
    __tablename__ = "models"
    id:Mapped[int] = mapped_column(primary_key=True)
    vehicleBrand_id:Mapped[int] = mapped_column(ForeignKey("vehiclebrands.id"))
    vehicleBrand:Mapped["VehicleBrand"] = relationship(back_populates="models")
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

class TransactionLog(Base):
    __tablename__ = "transaction_logs"
    id:Mapped[int] = mapped_column(primary_key=True)
    transaction_type:Mapped[str] = mapped_column(String)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"))
    users:Mapped["User"] = relationship(back_populates="transaction_logs")
    part_id:Mapped[int] = mapped_column(ForeignKey("parts.id"))
    part:Mapped["Parts"] = relationship(back_populates="transaction_logs")
    quantity:Mapped[int] = mapped_column(Integer)
    date:Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

Sessionlocal = sessionmaker(bind=engine)
def seed_roles():
    with Sessionlocal() as session:
        admin_role = session.get(Role,1)
        if admin_role is None:
            admin_role = Role(id=1,name="Admin")
            session.add(admin_role)

        raktaros_role = session.get(Role,2)
        if raktaros_role is None:
            raktaros_role = Role(id=2,name="Raktaros")
            session.add(raktaros_role)

        session.commit()
def seed_examples():
    with Sessionlocal() as session:
        if session.query(VehicleBrand).count() > 0:
            print("Examples already seeded, skipping...")
            return

        admin_pw=os.getenv("DEFAULT_ADMIN_PW")
        if not admin_pw:
            raise ValueError("ERROR: DEFAULT_ADMIN_PW not set!")
        hashed_password = bcrypt.hashpw(admin_pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        worker_pw = os.getenv("DEFAULT_WORKER_PW")
        if not worker_pw:
            raise ValueError("ERROR: DEFAULT_WORKER_PW not set!")
        hashed_password2 = bcrypt.hashpw(worker_pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        session.add(User(id=1,name="asd3", password=hashed_password, email="asd@gmail.com",phone="+214586453",role_id=1))
        session.add(User(id=2, name="raktaros", password=hashed_password2, email="raktaros@gmail.com", phone="+36309876543",role_id=2))

        session.add_all([
            VehicleBrand(id=1, name="Ford",country="USA"),
            VehicleBrand(id=2, name="Ferrari",country="Italia"),
            VehicleBrand(id=3, name="Opel", country="Germany"),
            VehicleBrand(id=4, name="Renault", country="France"),
            VehicleBrand(id=5, name="MZ", country="NDK"),
            VehicleBrand(id=6, name="Volkswagen", country="Germany"),
            VehicleBrand(id=7, name="Suzuki", country="Japan"),
            VehicleBrand(id=8, name="Toyota", country="Japan"),
            VehicleBrand(id=9, name="BMW", country="Germany"),
            VehicleBrand(id=10, name="Yamaha", country="Japan"),

            Manufacturer(id=1, name="Lemförder"),
            Manufacturer(id=2, name="Continental"),
            Manufacturer(id=3, name="MANN-FILTER"),
            Manufacturer(id=4, name="Valeo"),
            Manufacturer(id=5, name="Bosch"),
            Manufacturer(id=6, name="ZF"),
            Manufacturer(id=7, name="Brembo"),
            Manufacturer(id=8, name="NGK"),
            Manufacturer(id=9, name="Castrol"),
            Manufacturer(id=10, name="SKF"),
            Manufacturer(id=11, name="Motul"),
            Manufacturer(id=12, name="D.I.D"),

            Fuel(id=1, name="Benzin"),
            Fuel(id=2, name="Sport Benzin"),
            Fuel(id=3, name="Diesel"),
            Fuel(id=4, name="Hybrid"),

            VehicleType(id=1, name="Személyautó"),
            VehicleType(id=2, name="Motorkerékpár")
        ])
        session.flush()

        session.add_all([
            Modell(id=1, name="Mustang", vehicleBrand_id=1, generation=6, date=datetime.datetime(2015, 1, 1)),
            Modell(id=2, name="Testarossa", vehicleBrand_id=2, generation=1, date=datetime.datetime(1984, 1, 1)),
            Modell(id=3, name="Corsa", vehicleBrand_id=3, generation=5, date=datetime.datetime(2019, 1, 1)),
            Modell(id=4, name="Clio", vehicleBrand_id=4, generation=5, date=datetime.datetime(2019, 1, 1)),
            Modell(id=5, name="TS-125", vehicleBrand_id=5, generation=1, date=datetime.datetime(1973, 1, 1)),
            Modell(id=6, name="Golf", vehicleBrand_id=6, generation=7, date=datetime.datetime(2012, 1, 1)),
            Modell(id=7, name="Passat", vehicleBrand_id=6, generation=8, date=datetime.datetime(2014, 1, 1)),
            Modell(id=8, name="Swift", vehicleBrand_id=7, generation=4, date=datetime.datetime(2017, 1, 1)),
            Modell(id=9, name="Vitara", vehicleBrand_id=7, generation=4, date=datetime.datetime(2015, 1, 1)),
            Modell(id=10, name="Corolla", vehicleBrand_id=8, generation=12, date=datetime.datetime(2018, 1, 1)),
            Modell(id=11, name="3-as sorozat", vehicleBrand_id=9, generation=6, date=datetime.datetime(2011, 1, 1)),
            Modell(id=12, name="MT-07", vehicleBrand_id=10, generation=1, date=datetime.datetime(2014, 1, 1)),
            Engine(id=1, engine_code="coyote v8", horse_power=500, ccc=5000, vehicleBrand_id=1, fuel_id=1),
            Engine(id=2, engine_code="italian v12", horse_power=390, ccc=4900, vehicleBrand_id=2, fuel_id=2),
            Engine(id=3, engine_code="TS125", horse_power=12, ccc=125, vehicleBrand_id=5, fuel_id=1),
            Engine(id=4, engine_code="1.2 Ecotec", horse_power=60, ccc=1200, vehicleBrand_id=3, fuel_id=1),
            Engine(id=5, engine_code="1.4 TCe", horse_power=88, ccc=1400, vehicleBrand_id=4, fuel_id=1),
            Engine(id=6, engine_code="1.9 TDI", horse_power=105, ccc=1896, vehicleBrand_id=6, fuel_id=3),
            Engine(id=7, engine_code="2.0 TDI", horse_power=150, ccc=1968, vehicleBrand_id=6, fuel_id=3),
            Engine(id=8, engine_code="1.2 Dualjet", horse_power=90, ccc=1242, vehicleBrand_id=7, fuel_id=1),
            Engine(id=9, engine_code="1.8 HSD", horse_power=122, ccc=1798, vehicleBrand_id=8, fuel_id=4),
            Engine(id=10, engine_code="2.0d", horse_power=184, ccc=1995, vehicleBrand_id=9, fuel_id=3),
            Engine(id=11, engine_code="CP2", horse_power=75, ccc=689, vehicleBrand_id=10, fuel_id=1),
            Parts(id=1, part_number="MNF-001", manufacturer_id=3, name="Levegőszűrő", type="Szűrő", price=4500,
                  amount=50, min_amount=10, max_amount=100),
            Parts(id=2, part_number="BSC-002", manufacturer_id=5, name="Olajszűrő", type="Szűrő", price=3200, amount=85,
                  min_amount=20, max_amount=150),
            Parts(id=3, part_number="VLO-003", manufacturer_id=4, name="Kuplung szett", type="Hajtáslánc", price=85000,
                  amount=5, min_amount=2, max_amount=15),
            Parts(id=4, part_number="BRM-004", manufacturer_id=7, name="Első fékbetét szett", type="Fékrendszer",
                  price=18500, amount=30, min_amount=5, max_amount=50),
            Parts(id=5, part_number="BRM-005", manufacturer_id=7, name="Féktárcsa", type="Fékrendszer", price=25000,
                  amount=24, min_amount=4, max_amount=40),
            Parts(id=6, part_number="NGK-006", manufacturer_id=8, name="Gyújtógyertya", type="Gyújtás", price=4800,
                  amount=120, min_amount=16, max_amount=200),
            Parts(id=7, part_number="CST-007", manufacturer_id=9, name="Motorolaj 5W30 (5L)", type="Kenőanyag",
                  price=16500, amount=45, min_amount=10, max_amount=100),
            Parts(id=8, part_number="SKF-008", manufacturer_id=10, name="Vízpumpa", type="Hűtés", price=21000,
                  amount=12, min_amount=3, max_amount=25),
            Parts(id=9, part_number="CNT-009", manufacturer_id=2, name="Vezérműszíj készlet", type="Motor alkatrész",
                  price=45000, amount=8, min_amount=2, max_amount=15),
            Parts(id=10, part_number="VAL-010", manufacturer_id=4, name="H7 Izzó", type="Világítás", price=2500,
                  amount=200, min_amount=20, max_amount=500),
            Parts(id=11, part_number="ZFF-011", manufacturer_id=6, name="Kettőstömegű lendkerék", type="Hajtáslánc",
                  price=165000, amount=2, min_amount=1, max_amount=5),
            Parts(id=12, part_number="LMF-012", manufacturer_id=1, name="Lengőkar", type="Futómű", price=32000,
                  amount=16, min_amount=4, max_amount=30),
            Parts(id=13, part_number="MOT-013", manufacturer_id=11, name="Motul 7100 10W-40 (4L)", type="Kenőanyag",
                  price=19500, amount=30, min_amount=5, max_amount=50),
            Parts(id=14, part_number="DID-014", manufacturer_id=12, name="D.I.D Láncszett", type="Hajtáslánc",
                  price=45000, amount=8, min_amount=2, max_amount=20),
            Parts(id=15, part_number="HLL-015", manufacturer_id=5, name="Xenon vezérlő elektronika", type="Világítás",
                  price=125000, amount=2, min_amount=1, max_amount=5),
            Parts(id=16, part_number="SKF-016", manufacturer_id=10, name="Kardántengely csapágy", type="Hajtáslánc",
                  price=18000, amount=3, min_amount=2, max_amount=10),
            Parts(id=17, part_number="KLK-017", manufacturer_id=1, name="Kipufogó tartó bak", type="Kipufogó rendszer",
                  price=3500, amount=1, min_amount=5, max_amount=20)
        ])

        session.flush()

        session.add_all([
            Vehicle(id=1, vehicle_type_id=1, modell_id=1),
            Vehicle(id=2, vehicle_type_id=1, modell_id=6),
            Vehicle(id=3, vehicle_type_id=1, modell_id=8),
            Vehicle(id=4, vehicle_type_id=1, modell_id=10),
            Vehicle(id=5, vehicle_type_id=1, modell_id=11),
            Vehicle(id=6, vehicle_type_id=2, modell_id=5),
            Vehicle(id=7, vehicle_type_id=2, modell_id=12),
            MotorCompatibility(id=1, modell_id=1, engine_id=1),
            MotorCompatibility(id=2, modell_id=2, engine_id=2),
            MotorCompatibility(id=3, modell_id=6, engine_id=6),
            MotorCompatibility(id=4, modell_id=7, engine_id=7),
            MotorCompatibility(id=5, modell_id=8, engine_id=8),
            MotorCompatibility(id=6, modell_id=10, engine_id=9),
            MotorCompatibility(id=7, modell_id=11, engine_id=10),
            MotorCompatibility(id=8, modell_id=5, engine_id=3),
            MotorCompatibility(id=9, modell_id=12, engine_id=11),

            Compatibility(id=1, part_id=4, modell_id=6, engine_id=6),
            Compatibility(id=2, part_id=7, modell_id=6, engine_id=6),
            Compatibility(id=3, part_id=7, modell_id=8, engine_id=8),
            Compatibility(id=4, part_id=6, modell_id=8, engine_id=8),
            Compatibility(id=5, part_id=11, modell_id=7, engine_id=7),
            Compatibility(id=6, part_id=6, modell_id=5, engine_id=3),
            Compatibility(id=7, part_id=13, modell_id=12, engine_id=11),
            Compatibility(id=8, part_id=14, modell_id=12, engine_id=11)
        ])
        session.flush()

        now = datetime.datetime.now()

        session.add_all([
            SellHeader(id=1, date=now - datetime.timedelta(days=25), number=10001),
            SellHeader(id=2, date=now - datetime.timedelta(days=20), number=10002),
            SellHeader(id=3, date=now - datetime.timedelta(days=15), number=10003),
            SellHeader(id=4, date=now - datetime.timedelta(days=10), number=10004),
            SellHeader(id=5, date=now - datetime.timedelta(days=5), number=10005),
            SellHeader(id=6, date=now - datetime.timedelta(days=2), number=10006),
            SellHeader(id=7, date=now - datetime.timedelta(days=1), number=10007),
            SellHeader(id=8, date=now - datetime.timedelta(days=0), number=10008)
        ])
        session.flush()

        session.add_all([
            SellItem(id=1, sell_header_id=1, part_id=7, amount=1, price=16500),
            SellItem(id=2, sell_header_id=1, part_id=2, amount=1, price=3200),
            SellItem(id=3, sell_header_id=1, part_id=1, amount=1, price=4500),
            TransactionLog(id=1, transaction_type="Eladás", user_id=1, part_id=7, quantity=-1, date=now - datetime.timedelta(days=25)),
            TransactionLog(id=2, transaction_type="Eladás", user_id=1, part_id=2, quantity=-1, date=now - datetime.timedelta(days=25)),
            SellItem(id=4, sell_header_id=2, part_id=4, amount=1, price=18500),
            SellItem(id=5, sell_header_id=2, part_id=5, amount=2, price=25000),
            TransactionLog(id=3, transaction_type="Eladás", user_id=2, part_id=4, quantity=-1, date=now - datetime.timedelta(days=20)),
            SellItem(id=6, sell_header_id=3, part_id=10, amount=4, price=2500),
            TransactionLog(id=4, transaction_type="Eladás", user_id=1, part_id=10, quantity=-4, date=now - datetime.timedelta(days=15)),
            SellItem(id=7, sell_header_id=4, part_id=11, amount=1, price=165000),
            SellItem(id=8, sell_header_id=4, part_id=3, amount=1, price=85000),
            TransactionLog(id=5, transaction_type="Eladás", user_id=2, part_id=11, quantity=-1, date=now - datetime.timedelta(days=10)),
            SellItem(id=9, sell_header_id=8, part_id=14, amount=1, price=45000),
            SellItem(id=10, sell_header_id=8, part_id=13, amount=1, price=19500),
            SellItem(id=11, sell_header_id=8, part_id=6, amount=2, price=4800),
            TransactionLog(id=8, transaction_type="Eladás", user_id=1, part_id=14, quantity=-1, date=now),
            TransactionLog(id=9, transaction_type="Eladás", user_id=1, part_id=13, quantity=-1, date=now),
            TransactionLog(id=6, transaction_type="Bevételezés", user_id=1, part_id=7, quantity=50, date=now - datetime.timedelta(days=3)),
            TransactionLog(id=7, transaction_type="Bevételezés", user_id=1, part_id=10, quantity=100, date=now - datetime.timedelta(days=3)),
            TransactionLog(id=12, transaction_type="Bevételezés", user_id=1, part_id=14, quantity=9,
                           date=now - datetime.timedelta(days=10)),
            TransactionLog(id=13, transaction_type="Bevételezés", user_id=1, part_id=15, quantity=3,
                           date=now - datetime.timedelta(days=10)),
            TransactionLog(id=14, transaction_type="Bevételezés", user_id=1, part_id=16, quantity=5,
                           date=now - datetime.timedelta(days=10)),
            TransactionLog(id=15, transaction_type="Bevételezés", user_id=1, part_id=17, quantity=1,
                           date=now - datetime.timedelta(days=10))
        ])

        session.commit()

        session.execute(text("SELECT setval('parts_id_seq', (SELECT max(id) FROM parts))"))
        session.execute(text("SELECT setval('sell_headers_id_seq', (SELECT max(id) FROM sell_headers))"))
        session.execute(text("SELECT setval('sell_items_id_seq', (SELECT max(id) FROM sell_items))"))
        session.execute(text("SELECT setval('transaction_logs_id_seq', (SELECT max(id) FROM transaction_logs))"))
        session.commit()

if __name__ == '__main__':
    try:
        #Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        seed_roles()
        seed_examples()
        print("Successfully created all tables")
    except Exception as e:
        print("Failed to create tables", e)
