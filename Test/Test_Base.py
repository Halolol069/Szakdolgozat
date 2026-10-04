import unittest

from sqlalchemy import create_engine

from Model.database import Base, Sessionlocal


class Test_base(unittest.TestCase):
    def setUp(self):
        self.test_engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.test_engine)
        Sessionlocal.configure(bind=self.test_engine)

    def tearDown(self):
        Base.metadata.drop_all(self.test_engine)
        self.test_engine.dispose()