from .register_user._handler import register_handler
from .update_password._handler import update_password_handler

ACCOUNT_HANDLERS = {
    "REGISTER": register_handler,
    "UPDATE_PASSWORD": update_password_handler,
}
