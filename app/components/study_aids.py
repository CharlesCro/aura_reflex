import reflex as rx
from app.states.study_state import StudyState, Flashcard, PracticeQuestion
from app.state import AppState


def flashcard_view(card: Flashcard) -> rx.Component:
    return rx.el.div(
        rx.cond(
            card["flipped"],
            rx.el.div(card["answer"], class_name="p-6"),
            rx.el.div(card["question"], class_name="p-6 font-semibold"),
        ),
        on_click=lambda: StudyState.flip_flashcard(card["id"]),
        class_name="relative w-full h-48 flex items-center justify-center text-center bg-white border border-gray-200 rounded-lg shadow-sm cursor-pointer transition-transform duration-500",
        style={
            "transformStyle": "preserve-3d",
            "transform": rx.cond(card["flipped"], "rotateY(180deg)", "rotateY(0deg)"),
        },
    )


def mcq_question_view(question: PracticeQuestion) -> rx.Component:
    return rx.el.fieldset(
        rx.el.legend(question["question"], class_name="font-semibold mb-2"),
        rx.foreach(
            question["options"],
            lambda option: rx.el.div(
                rx.el.input(
                    type="radio",
                    name=f"q_{question['id']}",
                    value=option,
                    on_change=lambda val: StudyState.set_user_answer(
                        question["id"], val
                    ),
                    class_name="mr-2",
                    disabled=~StudyState.quiz_in_progress,
                ),
                rx.el.label(option, class_name="text-gray-700"),
                class_name="flex items-center p-2 rounded-md",
            ),
        ),
        class_name="p-4 mb-4 border border-gray-200 rounded-lg",
    )


def short_answer_view(question: PracticeQuestion) -> rx.Component:
    return rx.el.div(
        rx.el.label(question["question"], class_name="font-semibold mb-2 block"),
        rx.el.input(
            placeholder="Your answer...",
            on_change=lambda val: StudyState.set_user_answer(question["id"], val),
            class_name="w-full p-2 border border-gray-300 rounded-md",
            disabled=~StudyState.quiz_in_progress,
        ),
        class_name="p-4 mb-4 border border-gray-200 rounded-lg",
    )


def quiz_results_view(question: PracticeQuestion) -> rx.Component:
    return rx.el.div(
        rx.el.p(question["question"], class_name="font-semibold text-gray-800"),
        rx.el.div(
            rx.icon(
                rx.cond(question["is_correct"], "check-circle-2", "x-circle"),
                class_name="mr-2",
            ),
            rx.el.p(f"Your answer: {question['user_answer']}"),
            class_name=rx.cond(
                question["is_correct"],
                "flex items-center text-green-600",
                "flex items-center text-red-600",
            ),
        ),
        rx.cond(
            ~question["is_correct"],
            rx.el.p(
                f"Correct answer: {question['correct_answer']}",
                class_name="mt-1 text-sm text-blue-600",
            ),
        ),
        class_name="p-4 border rounded-lg mb-4",
        style={"borderColor": rx.cond(question["is_correct"], "#22c55e", "#ef4444")},
    )


def study_aids_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Study Aids", class_name="text-2xl font-bold text-gray-800 mb-2"),
        rx.el.p(
            f"Tools for: {AppState.selected_file['name']}",
            class_name="text-gray-600 mb-6",
        ),
        rx.el.div(
            rx.el.button(
                "Flashcards",
                on_click=lambda: StudyState.set_active_study_tool("flashcards"),
                class_name=rx.cond(
                    StudyState.active_study_tool == "flashcards",
                    "px-4 py-2 font-semibold text-white bg-indigo-600 rounded-lg",
                    "px-4 py-2 font-semibold text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200",
                ),
            ),
            rx.el.button(
                "Practice Quiz",
                on_click=lambda: StudyState.set_active_study_tool("questions"),
                class_name=rx.cond(
                    StudyState.active_study_tool == "questions",
                    "px-4 py-2 font-semibold text-white bg-indigo-600 rounded-lg",
                    "px-4 py-2 font-semibold text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200",
                ),
            ),
            class_name="flex gap-4 mb-6",
        ),
        rx.el.button(
            f"Generate {StudyState.active_study_tool.capitalize()}",
            on_click=lambda: StudyState.generate_study_aids(
                AppState.selected_file["id"], StudyState.active_study_tool
            ),
            is_loading=StudyState.generating,
            class_name="w-full px-6 py-3 font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors shadow-sm mb-8",
        ),
        rx.match(
            StudyState.active_study_tool,
            (
                "flashcards",
                rx.cond(
                    StudyState.flashcards.length() > 0,
                    rx.el.div(
                        rx.foreach(StudyState.flashcards, flashcard_view),
                        class_name="grid md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                    rx.el.p("Generate flashcards to start studying."),
                ),
            ),
            (
                "questions",
                rx.cond(
                    StudyState.questions.length() > 0,
                    rx.el.div(
                        rx.cond(
                            StudyState.quiz_in_progress,
                            rx.foreach(
                                StudyState.questions,
                                lambda q: rx.match(
                                    q["question_type"],
                                    ("mcq", mcq_question_view(q)),
                                    ("short_answer", short_answer_view(q)),
                                    rx.el.p("Unknown question type"),
                                ),
                            ),
                            rx.foreach(StudyState.questions, quiz_results_view),
                        ),
                        rx.el.button(
                            rx.cond(
                                StudyState.quiz_in_progress, "Submit Quiz", "Start Quiz"
                            ),
                            on_click=rx.cond(
                                StudyState.quiz_in_progress,
                                StudyState.submit_quiz,
                                StudyState.start_quiz,
                            ),
                            class_name="mt-6 w-full px-6 py-3 font-semibold text-white bg-green-600 rounded-lg hover:bg-green-700",
                        ),
                    ),
                    rx.el.p("Generate a practice quiz to test your knowledge."),
                ),
            ),
        ),
        key=f"{AppState.selected_file['id']}-{StudyState.active_study_tool}",
        class_name="p-8 bg-white rounded-xl border border-gray-200 shadow-sm",
    )