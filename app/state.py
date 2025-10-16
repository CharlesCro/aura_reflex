import reflex as rx
import asyncio
import os
from typing import TypedDict, Optional
import datetime


class File(TypedDict):
    name: str
    size: str
    type: str
    status: str
    uploaded_at: str
    id: str


class AppState(rx.State):
    """The main application state."""

    sidebar_open: bool = True
    uploading: bool = False
    upload_progress: int = 0
    uploaded_files: list[File] = []
    active_page: str = "Dashboard"
    selected_file: Optional[File] = None

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def set_active_page(self, page: str):
        self.active_page = page
        if page != "Study Aids":
            self.selected_file = None

    @rx.event
    def set_selected_file(self, file: File | None):
        self.selected_file = file

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        if not files:
            yield rx.toast.error("No files selected for upload.")
            return
        self.uploading = True
        total_files = len(files)
        for i, file in enumerate(files):
            upload_data = await file.read()
            unique_id = f"{datetime.datetime.now().timestamp()}-{file.name}"
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            file_path = upload_dir / unique_id
            with file_path.open("wb") as f:
                f.write(upload_data)
            self.upload_progress = int((i + 1) / total_files * 100)
            file_size_kb = round(len(upload_data) / 1024, 2)
            new_file: File = {
                "name": file.name,
                "size": f"{file_size_kb} KB",
                "type": file.content_type,
                "status": "Completed",
                "uploaded_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "id": unique_id,
            }
            self.uploaded_files.append(new_file)
            yield
        self.uploading = False
        self.upload_progress = 0
        yield rx.toast.success(f"Successfully uploaded {total_files} file(s).")