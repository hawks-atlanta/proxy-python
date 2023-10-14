from .login._handler import login_handler
from .refresh._handler import challenge_handler

AUTHENTICATION_HANDLERS = {"LOGIN": login_handler, "REFRESH": challenge_handler}
