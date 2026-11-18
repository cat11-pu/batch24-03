import os

import pytest

import path_guard as pg


@pytest.fixture(autouse=True)
def base(tmp_path, monkeypatch):
    monkeypatch.setattr(pg, "BASE", str(tmp_path))
    return tmp_path


def test_1_parent_traversal_is_rejected():
    with pytest.raises(ValueError):
        pg.resolve_path("../etc/passwd")


def test_2_absolute_path_is_rejected():
    with pytest.raises(ValueError):
        pg.resolve_path("/etc/passwd")


def test_3_encoded_traversal_is_rejected():
    with pytest.raises(ValueError):
        pg.resolve_path("%2e%2e%2fsecret")


def test_4_backslash_traversal_is_rejected():
    with pytest.raises(ValueError):
        pg.resolve_path("..\\secret")


def test_5_null_byte_is_rejected():
    with pytest.raises(ValueError):
        pg.resolve_path("a\x00b")


def test_6_sibling_prefix_is_not_allowed():
    assert pg.is_allowed("../data2/file") is False


def test_7_double_slash_is_normalized():
    path = pg.resolve_path("a//b")
    assert "//" not in path


def test_8_dot_segment_is_normalized():
    path = pg.resolve_path("a/./b")
    assert "/./" not in path and "\\.\\" not in path


def test_9_empty_path_is_rejected():
    with pytest.raises(ValueError):
        pg.resolve_path("")


def test_10_non_string_path_is_rejected():
    with pytest.raises(ValueError):
        pg.resolve_path(123)


def test_11_inner_dot_dot_is_normalized():
    assert pg.resolve_path("a/../b") == os.path.join(str(pg.BASE), "b")


def test_12_trailing_separator_is_removed():
    assert not pg.resolve_path("a/").endswith(("/", "\\"))


def test_13_windows_drive_is_rejected():
    with pytest.raises(ValueError):
        pg.resolve_path("C:\\Windows\\win.ini")


def test_14_encoded_null_is_rejected():
    with pytest.raises(ValueError):
        pg.resolve_path("a%00b")


def test_15_deep_escape_is_not_allowed():
    assert pg.is_allowed("a/../../etc/passwd") is False
