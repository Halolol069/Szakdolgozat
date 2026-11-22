MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_BYTES = 72


def is_password_too_long(password):
    return len(password.encode("utf-8")) > MAX_PASSWORD_BYTES


def password_error(password):
    if len(password) < MIN_PASSWORD_LENGTH:
        return f"A jelszó túl rövid, minimum {MIN_PASSWORD_LENGTH} karakter kötelező!"
    if is_password_too_long(password):
        return (f"A jelszó túl hosszú! Legfeljebb {MAX_PASSWORD_BYTES} bájt lehet "
                f"(az ékezetes betűk 2 bájtnak számítanak).")
    return None