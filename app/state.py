import reflex as rx
from typing import TypedDict, Optional

class File(TypedDict):
    name: str
    size: str
    type: str
    status: str
    uploaded_at: str
    id: str


class AppState(rx.State):
    "State for managing App status"

    sidebar_open: bool = True
    uploading: bool = False
    upload_progress: int = 0
    uploaded_files: list[File] = []
    active_page: str = "Dashboard"
    selected_file: Optional[File] = None