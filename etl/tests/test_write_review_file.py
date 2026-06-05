from scrape.scrape_reviews import write_review_file
from copy import deepcopy
from pathlib import Path

broken = {"broken" : True}
empty = {"reviews": {}}
empty_2 = {"reviews": [{"review": ""}]}
correct = {"reviews": [{
    "author": {"steamid" : 123, "playtime_at_review": 612},
    "review": "foo",
    "voted_up": 1,
    "votes_funny": 0,
    "votes_up": 0,
    "weighted_vote_score": 0.59
    }]}
wrong_types = {"reviews": [{
    "author": {"steamid" : "haha", "playtime_at_review": "asnk"},
    "review": 123,
    "voted_up": "efa",
    "votes_funny": "ajk",
    "votes_up": "hbsjk",
    "weighted_vote_score": "aebks"
    }]}

no_user_id = deepcopy(correct)
no_user_id["reviews"][0]["author"] = None

no_does_recommend = deepcopy(correct)
no_does_recommend["reviews"][0]["votes_up"] = None

wrong_casts = {"reviews": [{
    "author": {"steamid" : 123, "playtime_at_review": 612.0},
    "review": "foo",
    "voted_up": 1.0,
    "votes_funny": 1.0,
    "votes_up": 1.0,
    "weighted_vote_score": 1
    }]}


def test_broken():
    write_review_file("test_broken", broken)
    path = Path("mydata") / "test_broken_reviews.csv"

    # should not have been written
    assert not path.exists()


def test_empty():
    write_review_file("test_empty", empty)
    write_review_file("test_empty", empty_2)
    path = Path("mydata") / "test_empty_reviews.csv"

    # should not have been written
    assert not path.exists()


def test_no_user_id():
    write_review_file("test_nui", no_user_id)
    path = Path("mydata") / "test_nui_reviews.csv"

    # should not have been written
    assert not path.exists()


def test_no_does_recommed():
    write_review_file("test_ndr", no_does_recommend)
    path = Path("mydata") / "test_ndr_reviews.csv"

    # should not have been written
    assert not path.exists()


def test_wrong_types():
    write_review_file("test_wrong_types", wrong_types)
    path = Path("mydata") / "test_wrong_types_reviews.csv"

    # should not have been written
    assert not path.exists()


def test_wrong_casts():
    write_review_file("test_wrong_casts", wrong_casts)
    path = Path("mydata") / "test_wrong_casts_reviews.csv"

    # should have been written
    assert path.exists()
    path.unlink()


def test_correct():
    write_review_file("test_correct", correct, "mydata")
    path = Path("mydata") / "test_correct_reviews.csv"

    # should have been written
    assert path.exists()
    path.unlink()
