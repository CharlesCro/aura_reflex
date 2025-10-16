import reflex as rx


def ai_task_card(
    icon: str, title: str, description: str, task_name: str, file_id: str
) -> rx.Component:
    from app.states.ai_state import AIState

    return rx.el.div(
        rx.icon(icon, class_name="w-8 h-8 text-indigo-500"),
        rx.el.h3(title, class_name="mt-2 text-lg font-semibold text-gray-800"),
        rx.el.p(description, class_name="mt-1 text-sm text-gray-600"),
        rx.el.button(
            f"Run {title}",
            on_click=lambda: AIState.process_file(file_id, task_name),
            class_name="mt-4 w-full px-4 py-2 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-lg transition-shadow",
    )


def translation_options() -> rx.Component:
    from app.states.ai_state import AIState

    return rx.el.div(
        rx.el.h4("Translate Options", class_name="font-semibold text-gray-700"),
        rx.el.select(
            rx.foreach(AIState.languages, lambda lang: rx.el.option(lang, value=lang)),
            value=AIState.target_language,
            on_change=AIState.set_target_language,
            class_name="mt-2 w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500",
        ),
        class_name="mt-4",
    )


def ai_results_display() -> rx.Component:
    from app.state import AppState
    from app.states.ai_state import AIState

    return rx.el.div(
        rx.el.button(
            rx.icon("arrow-left", class_name="w-4 h-4 mr-2"),
            "Back to Dashboard",
            on_click=lambda: AppState.set_selected_file(None),
            class_name="flex items-center mb-6 px-4 py-2 text-sm font-semibold text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Process Document", class_name="text-2xl font-bold text-gray-800"
                ),
                rx.el.p(
                    f"Processing: {AppState.selected_file['name']}",
                    class_name="text-gray-600 mt-1",
                ),
                rx.el.div(
                    ai_task_card(
                        "file-text",
                        "Summarize",
                        "Generate a concise summary of the document.",
                        "summarize",
                        AppState.selected_file["id"],
                    ),
                    ai_task_card(
                        "mic",
                        "Transcribe",
                        "Convert audio or video content to text.",
                        "transcribe",
                        AppState.selected_file["id"],
                    ),
                    rx.el.div(
                        ai_task_card(
                            "languages",
                            "Translate",
                            "Translate the document into another language.",
                            "translate",
                            AppState.selected_file["id"],
                        ),
                        translation_options(),
                        class_name="flex flex-col gap-4",
                    ),
                    class_name="grid md:grid-cols-3 gap-6 mt-6",
                ),
                class_name="w-full",
            ),
            rx.el.div(
                rx.el.h3("Result", class_name="text-xl font-semibold text-gray-800"),
                rx.cond(
                    AIState.processing,
                    rx.el.div(
                        rx.spinner(class_name="w-8 h-8 text-indigo-600"),
                        rx.el.p(
                            "AI is processing your request...",
                            class_name="text-gray-600",
                        ),
                        class_name="flex flex-col items-center justify-center p-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200 mt-4",
                    ),
                    rx.el.div(
                        rx.cond(
                            AIState.result,
                            rx.el.div(
                                rx.el.p(
                                    AIState.result, class_name="whitespace-pre-wrap"
                                ),
                                class_name="p-6 bg-gray-50 rounded-xl border border-gray-200 mt-4 max-h-96 overflow-y-auto",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "brain-circuit",
                                    class_name="w-12 h-12 text-gray-300",
                                ),
                                rx.el.p(
                                    "Your AI-generated content will appear here.",
                                    class_name="text-gray-500",
                                ),
                                class_name="flex flex-col items-center justify-center p-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200 mt-4",
                            ),
                        )
                    ),
                ),
                class_name="mt-8",
            ),
            class_name="flex flex-col gap-6",
        ),
        key=AppState.selected_file["id"],
        class_name="w-full",
    )