from __future__ import annotations
import datetime as dt
from .line import Line


_SEASONS = {
    0: 2,
    1: 26,
    2: 26,
    3: 13,
    4: 30
}


class Episode:
    def __init__(self: Episode, production_code: int, title: str = None):
        self.__production_code = production_code
        self.__title = title
        self.__lines = {}

        season, episode = Episode.production_to_episode(self.__production_code)
        if(season < 0 or season > 4):
            raise ValueError(f'Invalid production code ({production_code}):'
                             f' season is {season} must be in range 1..4.')
        max_ep = _SEASONS[season]
        if(episode < 1 or episode > max_ep):
            raise ValueError(f'Invalid production code ({production_code}):'
                             f' episode is {episode} but must be in range'
                             f' 1..{max_ep}.')

    @staticmethod
    def production_to_episode(production_code: int) -> tuple:
        """
        Turns a 3-digit production code into a tuple of season and episode
        number respectively.

        Arguments
        ---------
        production_code: `int` The production code

        Raises
        ------
        `Value Error`: Raises this if the production is not 3 digits

        Returns
        -------
        `tuple`: A tuple of (season number, episode)
        """
        if(production_code == 0):  # Special case for the prequel
            return (0, 1)
        elif(production_code >= 100 or production_code <= 999):
            return production_code // 100, production_code % 100
        raise ValueError('Production code must be a 3-digit integer.')

    @property
    def production_code(self: Episode) -> int:
        """Gets the production code"""
        return self.__production_code

    @property
    def title(self: Episode) -> str:
        """Gets the episode title"""
        return self.__title

    def add_line(self: Episode, line: Line):
        """
        Adds the given line to the list of episode lines

        Arguments
        ---------
        line: `Line` The line to add
        """
        self.__lines[line.start] = line

    def search(self: Episode,
               inclusive_search: bool = False,
               **kwargs) -> [Line]:
        """
        Searches the episode with the given search terms.

        Arguments
        ---------
        inclusive_search: `bool` Whether or not the combination of terms should
                          be treated as a logical AND or a logical OR
        kwargs: `dict` The user-defined search terms.
            * character: match by character
            * dialogue: match by substring

        Returns
        -------
        `[Line]`: A list of lines that matched the terms and the search
                  opeartion (inclusive_search)
        """
        results = []
        conditional = any if inclusive_search else all

        for line in self.__lines.values():
            # Search terms matching
            match = []
            for term, value in kwargs.items():
                if(term == 'character'):
                    match.append(line.character.lower()
                                 == kwargs.get('character').lower())
                elif(term == 'dialogue'):
                    match.append(line.has_dialogue(kwargs.get('dialogue')))

            if conditional(match):
                results.append(line)

        return results

    def __eq__(self: Episode, src: Episode) -> bool:
        """
        Returns whether or not the current episode and given episode are
        exactly the same in terms of all attributes.

        This is implemented in a fail-fast fashion, so if a title or
        production code does not match, it will fail and not go on to check
        the line matches.

        Arguments
        ---------
        src: `Episode` The episode to compare against

        Returns
        -------
        `bool`: Whether or not the episodes are the same
        """
        if((self.__production_code != src.__production_code)
           or (self.__title != src.__title)):
            return False

        # TODO: There are problems with using the datetime as the index, since
        #   the ASS start time is slightly more precise than the unit tests or
        #   any user input, figure out a way around this
        #
        # for timestamp in self.__lines.keys():
        #     if self.__lines.get(timestamp) != src.__lines.get(timestamp):
        #         return False
        return True

    def __getitem__(self: Episode, start: dt.time) -> Line:
        """
        Returns the line at the given start-time index if any line exists,
        otherwise returns None

        Arguments
        ---------
        start: `datetime.time` The start-time of the line

        Returns
        -------
        `Line`: The line at the given start-time
        `None`: If no line starts at that time
        """
        return self.__lines.get(start)

    def __str__(self: Episode):
        """
        Returns a string representation of the episode for debugging purposes.

        Returns
        -------
        `str`: The string representation
        """
        return f'<Episode {self.__production_code}: {self.__title}' \
               f' ({len(self.__lines)} episodes)>'

    def __dict__(self: Line) -> dict:
        """
        Returns a dicttionary representation of the episode.

        Returns
        -------
        `dict`: The dictionary representation
        """
        return {
            'production_code': self.__production_code,
            'title': self.__title,
            'lines': list(map(lambda x: x.__dict__(), self.__lines.values()))
        }
