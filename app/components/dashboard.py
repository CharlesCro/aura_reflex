import reflex as rx


def file_upload_component() -> rx.Component:
    from app.state import AppState

    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud-upload", class_name="w-12 h-12 text-indigo-500"),
                rx.el.p(
                    "Drag & drop files here, or click to select files",
                    class_name="text-gray-600 font-medium",
                ),
                rx.el.p(
                    "Supports: Audio, Video, PDF, DOCX, TXT (Max 50MB)",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-indigo-200 rounded-xl bg-indigo-50 cursor-pointer hover:bg-indigo-100 transition-colors",
            ),
            id="file_upload_area",
            multiple=True,
            accept={
                "audio/*": [],
                "video/*": [],
                "application/pdf": [".pdf"],
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
                    ".docx"
                ],
                "text/plain": [".txt"],
            },
            max_size=52428800,
            class_name="w-full",
        ),
        rx.el.div(
            rx.foreach(
                rx.selected_files("file_upload_area"),
                lambda file: rx.el.div(
                    rx.icon("file", class_name="w-4 h-4 text-gray-500"),
                    rx.el.span(file, class_name="text-sm text-gray-700 truncate"),
                    class_name="flex items-center gap-2 p-2 bg-gray-100 border border-gray-200 rounded-md",
                ),
            ),
            class_name="mt-4 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2",
        ),
        rx.cond(
            rx.selected_files("file_upload_area").length() > 0,
            rx.el.div(
                rx.el.button(
                    "Clear Selection",
                    on_click=rx.clear_selected_files("file_upload_area"),
                    class_name="px-4 py-2 text-sm font-semibold text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors",
                ),
                rx.el.button(
                    "Upload Files",
                    on_click=AppState.handle_upload(
                        rx.upload_files(upload_id="file_upload_area")
                    ),
                    class_name="px-6 py-2 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm",
                ),
                class_name="flex justify-end gap-4 mt-4",
            ),
        ),
        rx.cond(
            AppState.uploading,
            rx.el.div(
                rx.el.p(
                    f"Uploading... {AppState.upload_progress}%",
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="h-2 bg-indigo-600 rounded-full transition-all duration-300",
                        style={"width": AppState.upload_progress.to_string() + "%"},
                    ),
                    class_name="w-full h-2 bg-gray-200 rounded-full overflow-hidden",
                ),
                class_name="mt-4",
            ),
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
    )


def file_management_dashboard() -> rx.Component:
    from app.state import AppState

    return rx.el.div(
        rx.el.h3("My Documents", class_name="text-lg font-semibold text-gray-800 mb-4"),
        rx.cond(
            AppState.uploaded_files.length() > 0,
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Name",
                                class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                            ),
                            rx.el.th(
                                "Size",
                                class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                            ),
                            rx.el.th(
                                "Type",
                                class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                            ),
                            rx.el.th(
                                "Uploaded",
                                class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                            ),
                            rx.el.th(
                                "Actions",
                                class_name="px-4 py-2 text-left text-sm font-semibold text-gray-600",
                            ),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            AppState.uploaded_files,
                            lambda file: rx.el.tr(
                                rx.el.td(
                                    file["name"],
                                    class_name="px-4 py-3 text-sm text-gray-800 border-t",
                                ),
                                rx.el.td(
                                    file["size"],
                                    class_name="px-4 py-3 text-sm text-gray-600 border-t",
                                ),
                                rx.el.td(
                                    file["type"],
                                    class_name="px-4 py-3 text-sm text-gray-600 border-t truncate max-w-xs",
                                ),
                                rx.el.td(
                                    file["uploaded_at"],
                                    class_name="px-4 py-3 text-sm text-gray-600 border-t",
                                ),
                                rx.el.td(
                                    rx.el.span(
                                        file["status"],
                                        class_name="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800",
                                    ),
                                    class_name="px-4 py-3 border-t",
                                ),
                                rx.el.td(
                                    rx.el.div(
                                        rx.el.button(
                                            rx.icon("play", class_name="w-4 h-4"),
                                            on_click=lambda: AppState.set_selected_file(
                                                file
                                            ),
                                            class_name="p-1 text-gray-500 hover:bg-gray-100 hover:text-indigo-600 rounded-md",
                                        ),
                                        rx.el.button(
                                            rx.icon(
                                                "trash-2",
                                                class_name="w-4 h-4 text-red-500",
                                            ),
                                            class_name="p-1 hover:bg-gray-100 rounded-md",
                                        ),
                                        class_name="flex gap-2",
                                    ),
                                    class_name="px-4 py-3 border-t",
                                ),
                                class_name="hover:bg-gray-50",
                            ),
                        )
                    ),
                    class_name="w-full",
                ),
                class_name="overflow-x-auto",
            ),
            rx.el.div(
                rx.icon("folder-open", class_name="w-16 h-16 text-gray-300"),
                rx.el.p("No documents uploaded yet.", class_name="text-gray-500 mt-4"),
                rx.el.p(
                    "Start by uploading your academic files above.",
                    class_name="text-sm text-gray-400",
                ),
                class_name="flex flex-col items-center justify-center p-12 border-2 border-dashed border-gray-200 rounded-xl mt-4",
            ),
        ),
        class_name="mt-8 p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
    )


def dashboard_page() -> rx.Component:
    from app.state import AppState
    from app.components.ai_results import ai_results_display

    return rx.el.div(
        rx.cond(
            AppState.selected_file,
            ai_results_display(),
            rx.el.div(file_upload_component(), file_management_dashboard()),
        ),
        class_name="p-8",
    )