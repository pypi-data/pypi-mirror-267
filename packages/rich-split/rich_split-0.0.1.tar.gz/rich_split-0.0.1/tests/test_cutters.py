from pytest import raises

from rich_split.cutters import TextCutter
from rich_split.exceptions import CutError


class TestTextCutter:
    def test_one_level_nesting_cutting(self):
        text = "word1 word2 wo3 w4 wword5"
        expected_result = (
            ["word1", "word2", "wo3", "w4", "wword5"],
            [" ", " ", " ", " ", None],
        )
        cutter = TextCutter(separator=" ")
        assert cutter(text, 6) == expected_result

    def test_cut_error_exception(self):
        with raises(CutError):
            TextCutter(separator=" ")("test", 3)

    def test_two_level_nesting_cutting(self):
        text = "word1 word2 wo3 w4 wword5"
        expected_result = (
            ["word1", "word2", "wo3", "w4", "w", "w", "o", "r", "d", "5"],
            [" ", " ", " ", " ", "", "", "", "", "", None],
        )
        cutter = TextCutter(separator=" ", cutter_config={"separator": ""})
        assert cutter(text, 5) == expected_result
        text = "word1 word2"
        expected_result = (
            ["w", "o", "r", "d", "1", "w", "o", "r", "d", "2"],
            ["", "", "", "", " ", "", "", "", "", None],
        )
        assert cutter(text, 4) == expected_result

    def test_count_separators_param(self):
        text = "word1 word2"
        expected_result = (
            ["word1", "word2"],
            [" ", None],
        )
        cutter = TextCutter(separator=" ", count_separators=True)
        assert cutter(text, 6) == expected_result
        with raises(CutError):
            cutter(text, 5)
