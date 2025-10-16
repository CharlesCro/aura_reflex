import reflex as rx
from app.state import AppState
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.dashboard import dashboard_page
from app.components.study_aids import study_aids_dashboard


def study_aids_page() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AppState.selected_file,
            study_aids_dashboard(),
            rx.el.div(
                rx.icon("file-search", class_name="w-16 h-16 text-gray-300"),
                rx.el.p(
                    "Please select a document from the dashboard first.",
                    class_name="text-gray-500 mt-4",
                ),
                rx.el.button(
                    "Go to Dashboard",
                    on_click=lambda: AppState.set_active_page("Dashboard"),
                    class_name="mt-4 px-4 py-2 font-semibold text-white bg-indigo-600 rounded-lg",
                ),
                class_name="flex flex-col items-center justify-center h-full p-8 text-center",
            ),
        ),
        class_name="p-8 h-full",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.match(
                AppState.active_page,
                ("Dashboard", dashboard_page()),
                ("Study Aids", study_aids_page()),
                rx.el.div(f"Page: {AppState.active_page}", class_name="p-8"),
            ),
            class_name="flex-1 bg-gray-50 overflow-y-auto",
        ),
        class_name="flex h-screen bg-white font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)