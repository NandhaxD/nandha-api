import requests
from dataclasses import dataclass
from json import dumps

class ApiException(Exception):
    pass

class Base:
    @staticmethod
    def default(obj: "Base"):
        return {
            attr: getattr(obj, attr)
            for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
            if getattr(obj, attr) is not None
        }

    def __str__(self) -> str:
        return dumps(self, default=Base.default, ensure_ascii=False)

@dataclass
class HozoryTranslateResult(Base):
    translated_text: str
    translation_language: str
    voice_link: str

    @staticmethod
    def parse(d: dict, dest: str) -> "HozoryTranslateResult":
        return HozoryTranslateResult(
            translated_text=d["translate"],
            translation_language=dest,
            voice_link=d["Voice_link"],
        )

class HozoryTranslator:
    def __init__(self) -> None:
        pass

    def translate(self, text: str, dest: str = "en") -> "HozoryTranslateResult":
        response = requests.get(
            f"https://hozory.com/translate/?target={dest}&text={text}"
        )
        try:
            result = response.json()
        except Exception as e:
            raise ApiException(str(e))

        if not result["status"] == "ok":
            raise ApiException(dumps(result["result"], indent=2, ensure_ascii=False))

        return HozoryTranslateResult.parse(result["result"], dest)

    def enter(self):
        return self

    def exit(self, *args):
        return self

def hozory_translate(text, code):
    hozory_engine = HozoryTranslator()
    result = hozory_engine.translate(text, code)
    return result.__str__()
