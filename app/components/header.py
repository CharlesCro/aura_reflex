import reflex as rx

def title() -> rx.Component:
    return 

def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.image(
                'logo.png',
                class_name='header_logo'
            ),
            rx.el.h2(
                'Welcome to AuraWeb',
                class_name = 'header_title'
            ),
            class_name = 'header_left'
        ),
        rx.el.div(
                rx.el.div(
                    rx.el.input(
                        placeholder='Search documents...',
                        class_name = 'search_box'
                    ),
                    rx.icon(
                        'search',
                        class_name = 'search_icon'
                    ),
                    class_name = 'relative'
                ),
                class_name = 'header_right'
            ),
            class_name='header_wrapper' 
    )