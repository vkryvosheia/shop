import pytest

from app.core.slugs import make_unique_slug, slugify


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Глечик ручної роботи, 1 л", "hlechyk-ruchnoi-roboty-1-l"),
        ("Кухня", "kukhnia"),
        ("Свічка соєва «Липа»", "svichka-soieva-lypa"),
        ("Юлія", "yuliia"),
        ("Їжак", "yizhak"),
        ("Згорани", "zghorany"),
        ("М'ята", "miata"),
        ("Ґанок", "ganok"),
        ("Ваза «Дніпро», 30 см", "vaza-dnipro-30-sm"),
        ("Hello, World!", "hello-world"),
        ("★★★", ""),
        ("", ""),
    ],
)
def test_slugify(text, expected):
    assert slugify(text) == expected


def test_make_unique_slug():
    taken = {"kukhnia", "kukhnia-2", "kukhnia-3"}

    def is_taken(slug: str) -> bool:
        return slug in taken

    assert make_unique_slug("vaza", is_taken) == "vaza"

    assert make_unique_slug("kukhnia", is_taken) == "kukhnia-4"
