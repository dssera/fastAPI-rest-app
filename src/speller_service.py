from __future__ import annotations

import requests


def spell_text(text: str):
    words_obj = __make_request(text)
    for speller_word_dict in words_obj:
        suggestions: list[None | str] = speller_word_dict["s"]
        old_word: str = speller_word_dict["word"]

        text = text.replace(old_word, suggestions[0])
    return text


def __make_request(text: str):
    speller_api_str = "https://speller.yandex.net/services/spellservice.json/checkText"
    return requests.post(url=speller_api_str, data={'text': text}).json()


if __name__ == "__main__":
    print(check_text("Привет, сможеш ли ты исправть это собщение? ваатпаоаврпиарицуориккалыв"))
