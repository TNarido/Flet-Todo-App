from flet import *
from components.TodoContainer import TodoContainer

def main(page : Page):
    page.title = "Todo App"
    page.bgcolor = colors.WHITE
    page.window_height = 600
    page.window_width = 500
    page.spacing = 52
    page.window_center()

    page.add(
        TodoContainer()
    )
    page.update

app(target = main)