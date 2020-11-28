import sys; sys.path.insert(0, '..')
import datetime as dt
from foxtrot_api.sub_serial import Parser, Format, Episode, Line


def test_parser_construction():
    """
    Given a valid format: ass
    When constructing a parser with it and converting to a string
    Then the parser should result in the string "<Parser: (format: ass)>"
    """
    parser = Parser(Format.ASS)
    assert str(parser) == '<Parser: (format: ass)>'


def test_parse_ass_format():
    """
    Given a valid format: ass and a path to a valid file
    When trying to parse the file at the given file path
    Then the parser should return a fully populated Episode object
    """
    parser = Parser(Format.ASS)
    lines = [
        Line(0, dt.time(0, 0, 54), dt.time(0, 0, 58), 'Jeremie',
             'Diary of Jeremie Belpois, Kadic Academy 8th grade student,'
             ' October 9th.'),
        Line(0, dt.time(0, 0, 59), dt.time(0, 1, 3), 'Jeremie',
             'A few weeks ago, I was hunting for parts to finish building my'
             ' miniature robots.'),
        Line(0, dt.time(0, 1, 3), dt.time(0, 1, 10), 'Jeremie',
             'I couldnt find anything around here I could use, so I decided'
             ' to rummage for scrap in the abandoned factory, not far from the'
             ' Academy.'),
    ]
    valid_episode = Episode(0, "X.A.N.A. Awakens")
    for line in lines:
        valid_episode.add_line(line)
    assert parser.parse('tests/subtitles/test.ass') == valid_episode
