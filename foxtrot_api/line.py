from __future__ import annotations
import datetime as dt


class Line:
    def __init__(self: Line,
                 production_code: int,
                 start: dt.time,
                 end: dt.time,
                 character: str = None,
                 dialogue: str = None):
        self.__production_code = production_code
        self.__start = start
        self.__end = end
        self.__character = character.upper()
        self.__dialogue = dialogue

    def has_dialogue(self: Line, dialogue: str) -> bool:
        return (self.__dialogue.lower().find(dialogue.lower()) != -1)

    def __eq__(self: Line, src: Line) -> bool:
        return (self.__character.upper() == src.__character.upper())

    def __str__(self: Line) -> str:
        return f'<Line: [{self.__start}-{self.__end}][{self.__character}]:' \
                ' {self.dialogue}>'

    def __dict__(self: Line):
        return {
            'production_code': self.__production_code,
            'timestamp': {
                'start': self.__start.strftime('%H:%M:%S'),
                'end': self.__end.strftime('%H:%M:%S')
            },
            'character': self.__character,
            'dialogue': self.__dialogue
        }


if __name__ == '__main__':
    l1 = Line(21, dt.time(1), dt.time(2), 'Yumi', 'Some text.')
    import ipdb; ipdb.set_trace()
