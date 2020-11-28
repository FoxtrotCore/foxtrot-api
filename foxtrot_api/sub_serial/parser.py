from __future__ import annotations
import enum
import ass
from .episode import Episode
from .line import Line


class Format(enum.Enum):
    ASS = 0
    SMI = 1
    SRT = 2
    TXT = 3
    VTT = 4

    def __str__(self: Format) -> str:
        return self.name.lower()


class Parser:
    def __init__(self: Parser, format: Format):
        self.__format = format

    @property
    def format(self: Parser) -> Format:
        """Gets the subtitle format"""
        return self.__format

    def parse(self: Parser, file_path: str) -> Episode:
        if(self.__format.value > 0):
            raise NotImplementedError('Parsing not supported for this format'
                                      ' yet.')
        __dispatch__ = {
            Format.ASS: ASSParser().parse
        }[self.__format]
        return __dispatch__(file_path)

    def __str__(self: Parser) -> str:
        return f'<Parser: (format: {self.__format})>'


class ASSParser:
    @staticmethod
    def parse(file_path: str) -> Episode:
        with open(file_path, encoding='utf-8-sig') as file:
            serialized_ass = ass.parse(file)

        title = serialized_ass.fields.get('Title')
        production_code = int(serialized_ass.fields.get('Original Script'))

        episode = Episode(production_code, title=title)
        for event in serialized_ass.events:
            line = Line(production_code,
                        event.start,
                        event.end,
                        event.name,
                        event.text)
            episode.add_line(line)
        return episode
