import reflex as rx
from app.state import AppState

def nav_item(icon: str, text: str, is_active: bool) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(tag=icon, class_name="w-5 h-5"),
            rx.el.span(
                text,
                class_name='opacity-100',
            ),
            class_name=rx.cond(
                is_active,
                "nav_item_active",
                "nav_item_inactive",
            ),
        ),
        on_click=lambda: AppState.set_active_page(text),
        href="#"
    )

def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                        
                ),
                rx.el.nav(
                    nav_item("house", "Home", AppState.active_page == "Home"),
                    nav_item("file-text", "Summarize", AppState.active_page == "Summarize"),
                    nav_item("languages", "Translate", AppState.active_page == "Translate"),
                    nav_item("mic", "Transcribe", AppState.active_page == "Transcribe"),
                    nav_item("sparkles", "Study Aids", AppState.active_page == "Study Aids"),
                    class_name="sidebar_items",
                ),
            ),
            rx.el.div(
                nav_item("settings", "Settings", AppState.active_page == "Settings"),
                nav_item("log-out", "Logout", AppState.active_page == "Logout"),
                class_name="sidebar_bottom",
            ),
            class_name = 'sidebar'
        )
    )

