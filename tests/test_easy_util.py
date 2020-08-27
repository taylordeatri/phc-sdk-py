from phc.easy.util import (
    concat_dicts,
    join_underscore,
    prefix_dict_keys,
    without_keys,
    defaultprop,
    add_prefixes,
)


def test_concat_dicts():
    assert concat_dicts([{"a": 1}, {"b": 2}, {"c": 3}]) == {
        "a": 1,
        "b": 2,
        "c": 3,
    }


def test_concat_dicts_with_duplicates():
    assert concat_dicts([{"a": 1}, {"a": 2}, {"a": 3, "b": 0}]) == {
        "a": 1,
        "a_1": 2,
        "a_2": 3,
        "b": 0,
    }


def test_concat_dicts_with_prefix():
    assert concat_dicts([{"a": 1}, {"b": 2}, {"c": 3}], prefix="tag") == {
        "tag_a": 1,
        "tag_b": 2,
        "tag_c": 3,
    }


def test_join_underscore():
    assert join_underscore(["", "tag", "", 0, "column"]) == "tag_0_column"


def test_prefix_dict_keys():
    assert prefix_dict_keys({"hi": 1, "yo": 2}, "column") == {
        "column_hi": 1,
        "column_yo": 2,
    }

    assert prefix_dict_keys({"a": 2, "b": 3}, "") == {"a": 2, "b": 3}


def test_without_keys():
    assert without_keys({"a": "z", "b": "y", "c": "x"}, ["b", "c"]) == {
        "a": "z"
    }


def test_add_prefixes():
    assert add_prefixes(["a", "b", "Patient/c"], ["Patient/"]) == [
        "Patient/a",
        "Patient/b",
        "Patient/c",
    ]


# defaultprop


class TestObject:
    @defaultprop
    def name(self):
        return "Di Lorenzo"

    def update_attrs(self, details):
        self._name = details.get("name")


def test_defaultprop():
    obj = TestObject()
    assert obj.name == "Di Lorenzo"

    obj.update_attrs({"name": "LifeOmic"})
    assert obj.name == "LifeOmic"
