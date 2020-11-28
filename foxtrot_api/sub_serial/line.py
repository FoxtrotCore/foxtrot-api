from __future__ import annotations
import datetime as dt


class Line:
    def __init__(self: Line,
                 production_code: int,
                 start: dt.time,
                 end: dt.time,
                 character: str,
                 dialogue: str):
        self.__production_code = production_code
        self.__start = start
        self.__end = end
        self.__character = character.upper()
        self.__dialogue = dialogue

        if(self.__start >= self.__end):
            raise ValueError(f'Line in-time ({self.__start}) cannot be greater'
                             ' than or equal to Line out-time'
                             f' ({self.__end}).')

    @property
    def production_code(self: Line) -> int:
        """Gets the production code."""
        return self.__production_code

    @property
    def start(self: Line) -> dt.time:
        """Gets the timestamp start-time."""
        return self.__start

    @property
    def end(self: Line) -> dt.time:
        """Gets the timestamp end-time."""
        return self.__end

    @property
    def character(self: Line) -> str:
        """Gets the character."""
        return self.__character

    @property
    def dialogue(self: Line) -> str:
        """Gets the character."""
        return self.__dialogue

    def has_dialogue(self: Line, dialogue: str) -> bool:
        """
        Evaluates whether or not the Line has the substring.
        The search is case insensitive.

        Arguments
        ---------
        dialogue: `str` The substring to search for.

        Returns
        -------
        `bool`: Whether or not the substring was found.
        """
        return (self.__dialogue.lower().find(dialogue.lower()) != -1)

    def __eq__(self: Line, src: Line) -> bool:
        """
        Returns whether or not the current line and given line are exactly the
        same in terms of all attributes.

        Arguments
        ---------
        src: `Line` The line to compare against

        Returns
        -------
        `bool`: Whether or not the lines are the same
        """
        return (self.__production_code == src.__production_code) \
            and (self.__start == src.__start) \
            and (self.__end == src.__end) \
            and (self.__character.upper() == src.__character.upper()) \
            and (self.__dialogue == src.__dialogue)

    def __ne__(self: Line, src: Line) -> bool:
        """
        Returns whether or not the current line and given line are different
        in terms of any  of the attributes.

        Arguments
        ---------
        src: `Line` The line to compare against

        Returns
        -------
        `bool`: Whether or not the lines are different
        """
        return (self.__production_code != src.__production_code) \
            or (self.__start != src.__start) \
            or (self.__end != src.__end) \
            or (self.__character.upper() != src.__character.upper()) \
            or (self.__dialogue != src.__dialogue)

    def __str__(self: Line) -> str:
        """
        Returns a string representation of the line for debugging purposes.

        Returns
        -------
        `str`: The string representation
        """
        return f'<Line: [{self.__start}-{self.__end}][{self.__character}]:' \
               f' {self.__dialogue}>'

    def __dict__(self: Line) -> dict:
        """
        Returns a dicttionary representation of the line.

        Returns
        -------
        `dict`: The dictionary representation
        """
        return {
            'production_code': self.__production_code,
            'timestamp': {
                'start': self.__start.strftime('%H:%M:%S'),
                'end': self.__end.strftime('%H:%M:%S')
            },
            'character': self.__character,
            'dialogue': self.__dialogue
        }
