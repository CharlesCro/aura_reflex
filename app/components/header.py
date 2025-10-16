import reflex as rx
from app.state import AppState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon(
                    tag=rx.cond(
                        AppState.sidebar_open, "panel-left-close", "panel-left-open"
                    ),
                    class_name="w-6 h-6 text-gray-600",
                ),
                on_click=AppState.toggle_sidebar,
                class_name="p-2 rounded-md hover:bg-gray-100",
            ),
            rx.el.h2(
                f"Welcome to {AppState.active_page}",
                class_name="text-xl font-semibold text-gray-800",
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.input(
                    placeholder="Search documents...",
                    class_name="bg-gray-100 border-none rounded-lg px-4 py-2 w-64 focus:ring-2 focus:ring-indigo-500",
                ),
                rx.icon(
                    "search",
                    class_name="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400",
                ),
                class_name="relative",
            ),
            rx.el.button(
                rx.icon("bell", class_name="w-6 h-6 text-gray-600"),
                class_name="p-2 rounded-full hover:bg-gray-100",
            ),
            rx.el.img(
                src="https://api.dicebear.com/9.x/initials/svg?seed=User",
                class_name="w-10 h-10 rounded-full border-2 border-indigo-200",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex items-center justify-between p-4 bg-white border-b border-gray-200",
    )