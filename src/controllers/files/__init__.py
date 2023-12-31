from .check_file_status._handler import check_state_handler
from .rename_file._handler import rename_handler
from .create_directory._handler import create_new_dir_handler
from .upload_file._handler import upload_file_handler
from .get_file_by_uuid._handler import get_file_handler
from .list_files._handler import list_files_handler
from .download_file._handler import download_file_handler
from .share_file._handler import share_handler
from .move_a_file._handler import file_move_handler
from .shared_with_who._handler import shared_with_who_handler
from .shared_file._handler import shared_files_handler
from .remove_file._handler import remove_file_handler
from .unshare_file._handler import unshare_handler

FILES_HANDLERS = {
    "CHECK_STATE": check_state_handler,
    "RENAME": rename_handler,
    "CREATE_DIRECTORY": create_new_dir_handler,
    "UPLOAD": upload_file_handler,
    "GET_BY_UUID": get_file_handler,
    "FILE_LIST": list_files_handler,
    "DOWNLOAD_FILE": download_file_handler,
    "SHARE": share_handler,
    "MOVE_FILE": file_move_handler,
    "SHARED_WITH_WHO": shared_with_who_handler,
    "SHARED_FILES": shared_files_handler,
    "REMOVE": remove_file_handler,
    "UNSHARE": unshare_handler,
}
