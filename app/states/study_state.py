import reflex as rx
from typing import TypedDict, Literal
import json
import random
import logging


class Flashcard(TypedDict):
    id: int
    question: str
    answer: str
    flipped: bool


QuestionType = Literal["mcq", "short_answer"]


class PracticeQuestion(TypedDict):
    id: int
    question_type: QuestionType
    question: str
    options: list[str]
    correct_answer: str
    user_answer: str
    is_correct: bool | None


class StudyState(rx.State):
    generating: bool = False
    flashcards: list[Flashcard] = []
    questions: list[PracticeQuestion] = []
    active_study_tool: str = "flashcards"
    quiz_in_progress: bool = False

    def _parse_ai_response(self, text: str, tool: str) -> list:
        try:
            clean_text = text.strip()
            if "on" in clean_text:
                clean_text = clean_text.split("on")[1].split("")[0].strip()
            elif "" in clean_text:
                clean_text = clean_text.split("")[1].split("")[0].strip()
            return json.loads(clean_text)
        except (json.JSONDecodeError, IndexError) as e:
            logging.exception(
                f"Failed to parse AI response as JSON, trying fallback: {e}"
            )
            if tool == "flashcards":
                lines = text.strip().splitlines()
                parsed = []
                q = None
                for line in lines:
                    line = line.strip()
                    if line.lower().startswith("q:"):
                        q = line[2:].strip()
                    elif line.lower().startswith("a:") and q is not None:
                        a = line[2:].strip()
                        parsed.append({"question": q, "answer": a})
                        q = None
                if parsed:
                    logging.info(
                        f"Successfully parsed {len(parsed)} flashcards via fallback."
                    )
                    return parsed
        logging.error(
            f"AI response parsing failed completely for tool: {tool}. Response: {text[:200]}..."
        )
        return []

    @rx.event(background=True)
    async def generate_study_aids(self, file_id: str, tool: str):
        async with self:
            self.generating = True
            if tool == "flashcards":
                self.flashcards = []
            else:
                self.questions = []
        yield
        from app.states.ai_state import AIState

        async with self:
            ai_state = await self.get_state(AIState)
            content = await ai_state._get_file_content(file_id)
        if content is None:
            async with self:
                self.generating = False
            yield rx.toast.error("Could not retrieve file content.")
            return
        prompts = {
            "flashcards": f'Generate 5 flashcards from the text below. Format the output as a JSON array of objects, where each object has a "question" and "answer" key. Example: [{{"question": "What is...?", "answer": "It is..."}}].\n\nText: {content}',
            "questions": f'Generate 3 practice questions (mix of multiple choice and short answer) from the text below. Format as a JSON array of objects. For MCQs, include "question_type": "mcq", "question", "options" (an array of 4 strings), and "correct_answer". For short answer, include "question_type": "short_answer", "question", and "correct_answer".\n\nText: {content}',
        }
        prompt = prompts.get(tool)
        if not prompt:
            async with self:
                self.generating = False
            yield rx.toast.error(f"Unknown study tool: {tool}")
            return
        ai_response = await ai_state._process_with_gemini(prompt)
        if not ai_response:
            async with self:
                self.generating = False
            yield rx.toast.error("Failed to generate study aids from AI.")
            return
        parsed_items = self._parse_ai_response(ai_response, tool)
        if not parsed_items:
            async with self:
                self.generating = False
            yield rx.toast.error("Could not understand the AI response format.")
            return
        if tool == "flashcards":
            flashcards = [
                {
                    "id": i,
                    "question": item.get("question", "No question provided"),
                    "answer": item.get("answer", "No answer provided"),
                    "flipped": False,
                }
                for i, item in enumerate(parsed_items)
            ]
            async with self:
                self.flashcards = flashcards
        elif tool == "questions":
            questions = []
            for i, item in enumerate(parsed_items):
                q_type = item.get("question_type", "short_answer")
                if q_type == "mcq" and (not item.get("options")):
                    q_type = "short_answer"
                new_q: PracticeQuestion = {
                    "id": i,
                    "question_type": q_type,
                    "question": item.get("question", "No question provided"),
                    "options": item.get("options", []),
                    "correct_answer": item.get("correct_answer", ""),
                    "user_answer": "",
                    "is_correct": None,
                }
                if q_type == "mcq":
                    if not new_q["options"]:
                        new_q["question_type"] = "short_answer"
                    elif new_q["correct_answer"] not in new_q["options"]:
                        new_q["options"].append(new_q["correct_answer"])
                    random.shuffle(new_q["options"])
                questions.append(new_q)
            async with self:
                self.questions = questions
                self.quiz_in_progress = True if questions else False
        async with self:
            self.generating = False

    @rx.event
    def set_active_study_tool(self, tool: str):
        self.active_study_tool = tool

    @rx.event
    def flip_flashcard(self, card_id: int):
        for card in self.flashcards:
            if card["id"] == card_id:
                card["flipped"] = not card["flipped"]
                break

    @rx.event
    def start_quiz(self):
        self.quiz_in_progress = True
        for q in self.questions:
            q["user_answer"] = ""
            q["is_correct"] = None

    @rx.event
    def submit_quiz(self):
        for q in self.questions:
            q["is_correct"] = (
                q["user_answer"].strip().lower() == q["correct_answer"].strip().lower()
            )
        self.quiz_in_progress = False

    @rx.event
    def set_user_answer(self, question_id: int, answer: str):
        for q in self.questions:
            if q["id"] == question_id:
                q["user_answer"] = answer
                break