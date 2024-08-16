from fasthtml.common import *
import json
from rich import print

with open("data.json") as file:
    data = json.loads(file.read())


def find(id):
    for lesson in data["lessons"]:
        if lesson["id"] == id:
            return lesson
    return None


app, rt = fast_app()


@rt("/")
def get():
    cards = []
    for lesson in data["lessons"]:
        cards.append(
            Article(
                Header(A(lesson["title"], href=f"/course/{lesson['id']}")),
                P(lesson["description"]) if "description" in lesson else None,
                P(lesson["level"], lesson["topic"]),
                Img(src=lesson["image"]),
            )
        )

    return Main(*cards, cls="container")


@rt("/course/{id}")
def get(id: int):
    course = find(id)
    cards = set()
    for step in course["steps"]:
        for quiz in step["quizzes"]:
            if "card" in quiz and quiz["card"] and "image" in quiz["card"]:
                cards.add(quiz["card"]["image"])
            elif "cards" in quiz:
                for card in quiz["cards"]:
                    if "image" in card:
                        cards.add(card["image"])

    return Main(
        A("go back", href="/"),
        H1(course["title"]),
        P(course["description"]),
        *[Img(src=source) for source in cards],
        cls="container",
    )


serve()
