import bcrypt
from unittest.mock import MagicMock

from Controller.LoginController import LoginController
from Model.database import Sessionlocal, User, Role, ROLE_ADMIN, ROLE_WORKER
from Test.Test_Base import Test_base


class DummyEntry:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def delete(self, start, end):
        self.value = ""


class DummyLabel:
    def __init__(self):
        self.text = ""

    def configure(self, text=None, **kwargs):
        if text is not None:
            self.text = text


class DummyButton:
    def configure(self, command=None, **kwargs):
        pass


class DummyLoginView:
    def __init__(self, username="", password=""):
        self.username = DummyEntry(username)
        self.password = DummyEntry(password)
        self.error_label = DummyLabel()
        self.login_button = DummyButton()


class DummyApp:
    def __init__(self):
        self.current_user = None
        self.dashboard_shown = False
        self.dashboard_controller = MagicMock()

    def show_dashboard(self):
        self.dashboard_shown = True


class Test_Login_Logic(Test_base):
    def setUp(self):
        super().setUp()
        hashed = bcrypt.hashpw(b"titok123", bcrypt.gensalt(rounds=4)).decode("utf-8")
        with Sessionlocal() as session:
            session.add_all([
                Role(id=ROLE_ADMIN, name="Admin"),
                Role(id=ROLE_WORKER, name="Raktaros"),
                User(id=1, name="anna", email="anna@mail.hu", phone="111",
                     password=hashed, role_id=ROLE_WORKER, is_active=True),
                User(id=2, name="bela", email="bela@mail.hu", phone="222",
                     password=hashed, role_id=ROLE_WORKER, is_active=False),
            ])
            session.commit()

    def _login(self, username, password):
        app = DummyApp()
        view = DummyLoginView(username, password)
        LoginController(app, view).login()
        return app, view

    def test_login_with_username(self):
        app, view = self._login("anna", "titok123")
        self.assertEqual("anna", app.current_user.name)
        self.assertTrue(app.dashboard_shown)

    def test_login_with_email(self):
        app, view = self._login("anna@mail.hu", "titok123")
        self.assertIsNotNone(app.current_user)

    def test_wrong_password(self):
        app, view = self._login("anna", "rossz")
        self.assertIsNone(app.current_user)
        self.assertFalse(app.dashboard_shown)
        self.assertIn("Hibás", view.error_label.text)

    def test_unknown_user_gets_same_message(self):
        app, view = self._login("nincsilyen", "titok123")
        self.assertIsNone(app.current_user)
        self.assertIn("Hibás", view.error_label.text)

    def test_suspended_account(self):
        app, view = self._login("bela", "titok123")
        self.assertIsNone(app.current_user)
        self.assertIn("függesztve", view.error_label.text)

    def test_empty_fields(self):
        app, view = self._login("", "")
        self.assertIsNone(app.current_user)
        self.assertIn("Add meg", view.error_label.text)