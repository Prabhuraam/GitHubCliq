from dataclasses import dataclass
from typing import List
from .response_types import (
    Context,
    SuggestionList,
    Slide,
    ButtonObject,
    CardDetails,
    Form,
    Message
)
from .request_types import BotDetails


@dataclass
class HandlerResponse:
    text: str = None
    context: Context = None
    bot: BotDetails = None
    suggestions: SuggestionList = None
    slides: List[Slide] = None
    buttons: List[ButtonObject] = None
    card: CardDetails = None
    message: Message = None

    @staticmethod
    def new_context():
        return Context()

    @staticmethod
    def new_bot_details(name: str, img: str) -> BotDetails:
        return {
            'name': name,
            'image': img
        }

    @staticmethod
    def new_suggestion_list():
        return SuggestionList()

    @staticmethod
    def new_slide():
        return Slide()

    def add_slides(self, *slides: Slide):
        if not self.slides:
            self.slides = list(slides)
            return len(self.slides)
        self.slides.extend(slides)
        return len(self.slides)

    @staticmethod
    def new_button():
        return ButtonObject()

    def add_button(self, *buttons: ButtonObject):
        if not self.buttons:
            self.buttons = list(buttons)
            return len(self.buttons)
        self.buttons.extend(buttons)
        return len(self.buttons)

    @staticmethod
    def new_card():
        return CardDetails()

    @staticmethod
    def new_form():
        return Form()

    @staticmethod
    def new_message():
        return Message()

    def set_text(self, text: str):
        self.text = text

    def set_message(self, mes):
        self.message = mes
