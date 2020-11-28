import sys; sys.path.insert(0, '..')
import pytest
import datetime as dt
from foxtrot_api.sub_serial import Episode, Line


def test_episode_eq_true():
    """
    Given two equal episodes with equal lines
    When comparing them with the overloaded `==` operator
    Then they should resolve to a true boolean
    """
    lines = [
        Line(121, dt.time(0, 10, 12), dt.time(0, 10, 13), 'Yumi', 'Text 1'),
        Line(122, dt.time(0, 15, 12), dt.time(0, 16, 13), 'Ulrich', 'Text 2')
    ]
    episode_1 = Episode(121, "Zero Gravity Zone")
    episode_2 = Episode(121, "Zero Gravity Zone")
    for line in lines:
        episode_1.add_line(line)
        episode_2.add_line(line)
    assert episode_1 == episode_2


def test_episode_construction():
    """
    Given the valid data set: {
        production_code: 121,
        title: Zero Gravity Zone
    }
    When trying to construct the Episode and converting it to a string
    Then it should result in the string:
    "<Episode 121: Zero Gravity Zone (0 episodes)>"
    """
    episode = Episode(121, "Zero Gravity Zone")
    assert str(episode) == '<Episode 121: Zero Gravity Zone (0 episodes)>'


def test_episode_production_code_valid():
    """
    Given an episode with the production code: 121
    When constructiong the object
    Then it should result in a valid episode of season 1, episode 21
    """
    episode = Episode(121, "Zero Gravity Zone")
    assert Episode.production_to_episode(episode.production_code) == (1, 21)


def test_episode_season_invalid():
    """
    Given an episode with the production code: 510
    When constructiong the object
    Then it should raise a value error
    """
    with pytest.raises(ValueError):
        assert Episode(510, "Zero Gravity Zone")


def test_episode_episode_invalid():
    """
    Given an episode with the production code: 150
    When constructiong the object
    Then it should raise a value error
    """
    with pytest.raises(ValueError):
        assert Episode(150, "Zero Gravity Zone")


def test_episode_add_get():
    """
    Given a valid line: {
        production_code: 121,
        start: dt.time(0, 5, 37),
        end: dt.time(0, 5, 42),
        character: 'Ulrich',
        dialogue: 'No, I said count me out. I’ll go when the game’s over.'
    }
    When adding it to an episode and subindexing the episode by the same
    start-time
    Then it should give back the line just submitted
    """
    episode = Episode(121, "Zero Gravity Zone")
    line = Line(121,
                dt.time(0, 5, 37),
                dt.time(0, 5, 42),
                'Ulrich',
                'No, I said count me out. I’ll go when the game’s over.')
    episode.add_line(line)
    assert episode[dt.time(0, 5, 37)] == line


def test_episode_has_search_terms():
    """
    Given the search terms: {
        character: Yumi
        dialogue: more
    }
    When searching the episode with the given terms
    Then the results of the search should be: [
        <Line: [00:11:30-00:11:32][YUMI]: More text!>
    ]
    """
    lines = [
        Line(121, dt.time(0, 10, 12), dt.time(0, 10, 13), 'Yumi', 'A text 1.'),
        Line(121, dt.time(0, 11, 30), dt.time(0, 11, 32), 'Yumi', 'More text!'),
        Line(121, dt.time(0, 15, 12), dt.time(0, 16, 13), 'Ulrich', 'B, text 2.')
    ]
    episode = Episode(121, "Zero Gravity Zone")
    for line in lines:
        episode.add_line(line)
    assert episode.search(dialogue='more', character='yumi') == [lines[1]]


def test_episode_not_has_search_terms():
    """
    Given the search terms: {
        character: Odd
        dialogue: more
    }
    When searching the episode with the given terms
    Then the results of the search should be: []
    """
    lines = [
        Line(121, dt.time(0, 10, 12), dt.time(0, 10, 13), 'Yumi', 'A text 1.'),
        Line(121, dt.time(0, 11, 30), dt.time(0, 11, 32), 'Yumi', 'More text!'),
        Line(121, dt.time(0, 15, 12), dt.time(0, 16, 13), 'Ulrich', 'B, text 2.')
    ]
    episode = Episode(121, "Zero Gravity Zone")
    for line in lines:
        episode.add_line(line)
    assert episode.search(dialogue='more', character='odd') == []
