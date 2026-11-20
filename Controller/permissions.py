from tkinter import messagebox

from Model.database import Sessionlocal, User, ROLE_ADMIN


def _fresh_user(main_app):
    current = getattr(main_app, "current_user", None)
    if current is None:
        return None
    with Sessionlocal() as session:
        return session.get(User, current.id)


def require_active_user(main_app, parent=None):
    user = _fresh_user(main_app)
    if user is None:
        messagebox.showerror("Hiba", "Nincs érvényes bejelentkezett felhasználó!", parent=parent)
        return False
    if not user.is_active:
        messagebox.showerror("Hiba", "A fiókod fel van függesztve, a művelet nem végezhető el!", parent=parent)
        return False
    return True


def require_admin(main_app, parent=None):
    if not require_active_user(main_app, parent):
        return False
    user = _fresh_user(main_app)
    if user.role_id != ROLE_ADMIN:
        messagebox.showerror("Hiba", "Ehhez a művelethez admin jogosultság szükséges!", parent=parent)
        return False
    return True