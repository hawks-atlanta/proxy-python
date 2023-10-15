from .check_file_status._handler import check_state_handler
from .rename_file._handler import rename_handler
from .create_directory._handler import create_new_dir_handler
from .upload_file._handler import upload_file_handler
from .list_files._handler import get_list_handler

FILES_HANDLERS = {
    "CHECK_STATE": check_state_handler,
    "RENAME": rename_handler,
    "CREATE_DIRECTORY": create_new_dir_handler,
    "UPLOAD": upload_file_handler,
    "FILE_LIST": get_list_handler,
}
