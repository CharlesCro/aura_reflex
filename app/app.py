import reflex as rx

from app.state import AppState
from rxconfig import config
from app.components.sidebar import sidebar
from app.components.dashboard import main_content
from app.components.header import header



def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            main_content(),
            class_name = 'content_wrapper'
            ),
    )
    


app = rx.App(stylesheets = ['/style.css'])
app.add_page(index)