from dataclasses import dataclass

from teambot import team_alloc, team_to_string


@dataclass
class FakeMember:
    display_name: str


def test_team_sizes_differ_by_at_most_one():
    teams = team_alloc(list(range(15)), 4)
    assert [len(team) for team in teams] == [3, 4, 4, 4]


def test_every_member_is_assigned_exactly_once():
    members = list(range(15))
    teams = team_alloc(members, 4)
    assert sorted(member for team in teams for member in team) == members


def test_members_argument_is_not_reordered():
    members = list(range(15))
    team_alloc(members, 4)
    assert members == list(range(15))


def test_all_teams_are_full_when_divisible():
    teams = team_alloc(list(range(12)), 4)
    assert [len(team) for team in teams] == [4, 4, 4]


def test_team_to_string_lists_members_per_team():
    teams = [
        [FakeMember("a"), FakeMember("b")],
        [FakeMember("c")],
    ]
    assert team_to_string(teams) == "[Team 1] a, b\n[Team 2] c"


def test_team_to_string_escapes_markdown_in_names():
    teams = [[FakeMember("a_b*c")]]
    assert team_to_string(teams) == r"[Team 1] a\_b\*c"


def test_team_to_string_escapes_mentions_in_names():
    teams = [[FakeMember("@everyone")]]
    assert team_to_string(teams) == "[Team 1] @\u200beveryone"
