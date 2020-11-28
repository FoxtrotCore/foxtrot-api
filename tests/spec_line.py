import sys; sys.path.insert(0, '..')
import pytest
import datetime as dt
from foxtrot_api.sub_serial import Line


def test_line_construction():
    """
    Given a set of valid line info
    When constructing a line with the data set: {
        production_code: 121,
        start: dt.time(1),
        end: dt.time(2),
        character: 'Yumi',
        dialogue: 'Some text.'
    }
    and converting it to a string
    Then it should produce the string ""
    """
    line = Line(121, dt.time(1), dt.time(2), 'Yumi', 'Some text.')
    assert str(line) == '<Line: [01:00:00-02:00:00][YUMI]: Some text.>'


def test_line_to_dict():
    """
    Given a set of valid line info
    When constructing a line with the data set: {
        production_code: 121,
        start: dt.time(1),
        end: dt.time(2),
        character: 'Yumi',
        dialogue: 'Some text.'
    }
    and converting it to a string
    Then it should produce a matching dict representation
    """
    line = Line(121, dt.time(1), dt.time(2), 'Yumi', 'Some text.')
    assert line.__dict__() == {
        'production_code': 121,
        'timestamp': {
            'start': dt.time(1).strftime('%H:%M:%S'),
            'end': dt.time(2).strftime('%H:%M:%S')
        },
        'character': 'YUMI',
        'dialogue': 'Some text.'
    }


def test_line_eq_true():
    """
    Given two equal lines
    When comparing them with the overloaded `==` operator
    Then they should resolve to a true boolean
    """
    line_1 = Line(121, dt.time(1), dt.time(2), 'Yumi', 'Some text.')
    line_2 = Line(121, dt.time(1), dt.time(2), 'Yumi', 'Some text.')
    assert line_1 == line_2


def test_line_eq_false():
    """
    Given two equal lines
    When comparing them with the overloaded `==` operator
    Then they should resolve to a true boolean
    """
    line_1 = Line(121, dt.time(1), dt.time(2), 'Yumi', 'Some text.')
    line_2 = Line(122, dt.time(3), dt.time(4), 'Odd', 'Other text.')
    assert line_1 != line_2


def test_line_start_before_end():
    """
    Given a line with a start-time greater than its end-time
    When constructing the object
    Then a ValueError should be raised
    """
    with pytest.raises(ValueError):
        assert Line(121, dt.time(2), dt.time(1), 'Yumi', 'Some text.')


def test_line_has_dialogue():
    """
    Given a line that has the dialogue "Some text."
    When searching the line for the substring "Text"
    Then the line should affirm that it has the substring in its dialogue
    """
    text = 'Text'
    line = Line(121, dt.time(1), dt.time(2), 'Yumi', 'Some text.')
    assert line.has_dialogue(text)


def test_line_not_has_dialogue():
    """
    Given a line that has the dialogue "Some text."
    When searching the line for the substring "Dog"
    Then the line should affirm that it does not have the substring in its
    dialogue
    """
    text = 'Dog'
    line = Line(121, dt.time(1), dt.time(2), 'Yumi', 'Some text.')
    assert not line.has_dialogue(text)
