import re
from collections.abc import Callable

UKR_TO_LATIN = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "h",
    "ґ": "g",
    "д": "d",
    "е": "e",
    "ж": "zh",
    "з": "z",
    "и": "y",
    "і": "i",
    "й": "i",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ю": "iu",
    "я": "ia",
    "є": "ie",
    "ї": "i",
}

START_MAP = {
    "є": "ye",
    "ї": "yi",
    "й": "y",
    "ю": "yu",
    "я": "ya",
}


def _transliterate_word(word: str) -> str:
    word = word.lower()
    result = []
    i = 0
    length = len(word)

    while i < length:
        if i + 1 < length and word[i] == "з" and word[i + 1] == "г":
            result.append("zgh")
            i += 2
            continue

        char = word[i]

        if char in "ь'’ʼ":
            i += 1
            continue

        if char in START_MAP:
            is_at_start = i == 0
            if is_at_start:
                result.append(START_MAP[char])
            else:
                result.append(UKR_TO_LATIN[char])
            i += 1
            continue

        if char in UKR_TO_LATIN:
            result.append(UKR_TO_LATIN[char])
        elif char.isascii() and (char.isalnum() or char in "-_"):
            result.append(char)
        i += 1

    return "".join(result)


def slugify(text: str) -> str:
    if not text:
        return ""

    cleaned_chars = []
    for char in text.lower():
        if char.isalnum() or char in "а-яґєіїьюя'’ʼ " or (char.isascii() and char.isalnum()):
            cleaned_chars.append(char)
        else:
            cleaned_chars.append(" ")

    cleaned_text = "".join(cleaned_chars)
    words = cleaned_text.split()

    transliterated_words = [_transliterate_word(w) for w in words]

    slug = "-".join(filter(None, transliterated_words))
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")

    if len(slug) > 80:
        slug = slug[:80]
        if "-" in slug:
            slug = slug.rsplit("-", 1)[0]

    return slug


def make_unique_slug(base: str, is_taken: Callable[[str], bool]) -> str:
    if not is_taken(base):
        return base

    counter = 2
    while True:
        candidate = f"{base}-{counter}"
        if not is_taken(candidate):
            return candidate
        counter += 1
