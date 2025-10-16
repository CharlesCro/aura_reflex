import reflex as rx
from app.state import AppState


def nav_item(icon: str, text: str, is_active: bool) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(tag=icon, class_name="w-5 h-5"),
            rx.el.span(
                text,
                class_name=rx.cond(AppState.sidebar_open, "opacity-100", "opacity-0"),
            ),
            class_name=rx.cond(
                is_active,
                "flex items-center gap-3 px-4 py-2.5 rounded-lg bg-indigo-100 text-indigo-700 font-semibold",
                "flex items-center gap-3 px-4 py-2.5 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900",
            ),
        ),
        on_click=lambda: AppState.set_active_page(text),
        href="#",
        class_name="w-full transition-colors duration-200",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("brain-circuit", class_name="h-8 w-8 text-indigo-600"),
                rx.el.h1(
                    "AcademiAI",
                    class_name=rx.cond(
                        AppState.sidebar_open,
                        "text-2xl font-bold text-gray-800 opacity-100 transition-opacity duration-300",
                        "opacity-0 w-0",
                    ),
                ),
                class_name="flex items-center gap-3 p-4 border-b border-gray-200",
            ),
            rx.el.nav(
                nav_item(
                    "layout-dashboard", "Dashboard", AppState.active_page == "Dashboard"
                ),
                nav_item("file-text", "Summarize", AppState.active_page == "Summarize"),
                nav_item("mic", "Transcribe", AppState.active_page == "Transcribe"),
                nav_item("languages", "Translate", AppState.active_page == "Translate"),
                nav_item(
                    "sparkles", "Study Aids", AppState.active_page == "Study Aids"
                ),
                class_name="flex flex-col gap-2 p-4",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            nav_item("settings", "Settings", AppState.active_page == "Settings"),
            nav_item("log-out", "Logout", AppState.active_page == "Logout"),
            class_name="p-4 border-t border-gray-200",
        ),
        class_name=rx.cond(
            AppState.sidebar_open,
            "flex flex-col bg-white border-r border-gray-200 w-64 transition-width duration-300",
            "flex flex-col bg-white border-r border-gray-200 w-20 transition-width duration-300",
        ),
    )