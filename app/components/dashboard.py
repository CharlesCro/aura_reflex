import reflex as rx



def main_content() -> rx.Component:
    return rx.el.div(
        rx.text('Hello World', class_name='text_primary'),
        class_name = 'main')