import unittest

from sqlalchemy import create_engine, event
from Model.database import Base, Sessionlocal, User, Role, Fuel, Manufacturer, ROLE_ADMIN, ROLE_WORKER

TEST_ADMIN_ID = 99

class DummyUser:
    def __init__(self, user_id, role_id):
        self.id = user_id
        self.role_id = role_id


class DummyAppWithUser:
    def __init__(self, user_id, role_id):
        self.current_user = DummyUser(user_id, role_id)


class Test_base(unittest.TestCase):
    def setUp(self):
        self.test_engine = create_engine('sqlite:///:memory:')
        @event.listens_for(self.test_engine, "connect")
        def enable_foreign_keys(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        Base.metadata.create_all(self.test_engine)
        Sessionlocal.configure(bind=self.test_engine)

        with Sessionlocal() as session:
            session.add_all([
                Role(id=ROLE_ADMIN, name="Admin"),
                Role(id=ROLE_WORKER, name="Raktaros"),
                Fuel(id=1, name="Benzin"),
                Manufacturer(id=1, name="Bosch"),
                Manufacturer(id=2, name="Valeo"),
                Manufacturer(id=3, name="Lemförder"),
                User(id=TEST_ADMIN_ID, name="__teszt_admin__", password="-", email="__admin@teszt.hu",
                     phone="__000", role_id=ROLE_ADMIN, is_active=True),
            ])
            session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.test_engine)
        self.test_engine.dispose()