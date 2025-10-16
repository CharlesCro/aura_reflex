import reflex as rx
import os
import logging
from typing import cast


class AIState(rx.State):
    """Manages AI interactions and results."""

    processing: bool = False
    result: str = ""
    error_message: str = ""
    target_language: str = "Spanish"
    languages: list[str] = [
        "Spanish",
        "French",
        "German",
        "Chinese",
        "Japanese",
        "Italian",
    ]

    async def _get_file_content(self, file_id: str) -> str | None:
        from app.state import AppState

        app_state = await self.get_state(AppState)
        file_info = next(
            (f for f in app_state.uploaded_files if f["id"] == file_id), None
        )
        if not file_info:
            self.error_message = "File not found."
            return None
        upload_dir = rx.get_upload_dir()
        file_path = upload_dir / file_id
        if not file_path.exists():
            self.error_message = (
                f"File content not found on server for {file_info['name']}."
            )
            return None
        try:
            file_type = cast(str, file_info["type"])
            if file_type.startswith("text/"):
                return file_path.read_text()
            elif file_type == "application/pdf":
                return f"[Content of PDF: {file_info['name']}]"
            elif file_type.startswith("audio/") or file_type.startswith("video/"):
                return f"[Audio/Video content: {file_info['name']}]"
            else:
                self.error_message = (
                    f"Unsupported file type for processing: {file_info['type']}"
                )
                return None
        except Exception as e:
            logging.exception(f"Error reading file: {e}")
            self.error_message = f"Error reading file: {e}"
            return None

    def _get_gemini_client(self):
        try:
            from google import genai

            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                self.error_message = "GOOGLE_API_KEY is not set."
                return None
            return genai.Client(api_key=api_key)
        except ImportError as e:
            logging.exception(f"Error importing google.genai: {e}")
            self.error_message = (
                "Google GenAI package is not installed. Please install 'google-genai'."
            )
            return None

    async def _process_with_gemini(self, prompt: str):
        client = self._get_gemini_client()
        if client is None:
            async with self:
                self.processing = False
            yield rx.toast.error(self.error_message)
            return
        try:
            response = client.generate_content(
                model="models/gemini-1.5-flash", contents=prompt
            )
            yield response.text
            return
        except Exception as e:
            logging.exception(f"An error occurred with the AI service: {e}")
            async with self:
                self.error_message = f"An error occurred with the AI service: {e}"
            yield rx.toast.error(self.error_message)
            return

    @rx.event(background=True)
    async def process_file(self, file_id: str, task: str):
        """Processes a file with the specified AI task."""
        async with self:
            self.processing = True
            self.result = ""
            self.error_message = ""
        yield
        content = await self._get_file_content(file_id)
        if content is None:
            async with self:
                self.processing = False
            yield rx.toast.error(self.error_message)
            return
        prompts = {
            "summarize": f"Summarize the following content in a concise and academic manner:\n\n{content}",
            "transcribe": f"This is a placeholder for transcription. Content: {content}",
            "translate": f"Translate the following content to {self.target_language}:\n\n{content}",
        }
        prompt = prompts.get(task)
        if not prompt:
            async with self:
                self.error_message = f"Unknown task: {task}"
                self.processing = False
            yield rx.toast.error(self.error_message)
            return
        ai_result = await self._process_with_gemini(prompt)
        async with self:
            if ai_result:
                self.result = ai_result
            self.processing = False

    @rx.event
    def set_target_language(self, language: str):
        self.target_language = language