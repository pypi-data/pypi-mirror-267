from rich_split.joiners import TextJoiner


class TestTextJoiner:
    def test_with_add_separator_to_parts_end(self):
        fixtures = [
            ((["word1"], [None]), ["word1"]),
            ((["word1", "word"], [" ", None]), ["word1 word"]),
            ((["word1", "word2"], [" ", None]), ["word1 ", "word2"]),
            ((["w1", "w2"], [" ", None]), ["w1 w2"]),
            ((["w1", "w2", "w3"], [" ", "", None]), ["w1 w2w3"]),
            (
                (["w1", "w2", "w3", "w4", "w5"], [" ", "", " ", "  ", None]),
                ["w1 w2w3 ", "w4  w5"],
            ),
            (
                (
                    ["cat1", "cat2", "cat3", "cat4", "cat5", "cat6", "cat7"],
                    [" ", " ", " ", " ", " ", " ", None],
                ),
                ["cat1 cat2 ", "cat3 cat4 ", "cat5 cat6 ", "cat7"],
            ),
        ]
        joiner = TextJoiner(True)
        for (chunks, separators), expected_result in fixtures:
            assert joiner(chunks, separators, 10) == expected_result

    def test_without_add_separator_to_parts_end(self):
        fixtures = [
            ((["word1"], [None]), ["word1"]),
            ((["word1", "word"], [" ", None]), ["word1 word"]),
            ((["word1", "word2"], [" ", None]), ["word1", "word2"]),
            ((["w1", "w2"], [" ", None]), ["w1 w2"]),
            ((["w1", "w2", "w3"], [" ", "", None]), ["w1 w2w3"]),
            (
                (["w1", "w2", "w3", "w4", "w5"], [" ", "", " ", "  ", None]),
                ["w1 w2w3 w4", "w5"],
            ),
            (
                (
                    ["cat1", "cat2", "cat3", "cat4", "cat5", "cat6", "cat7"],
                    [" ", " ", " ", " ", " ", " ", None],
                ),
                ["cat1 cat2", "cat3 cat4", "cat5 cat6", "cat7"],
            ),
        ]
        joiner = TextJoiner(False)
        for (chunks, separators), expected_result in fixtures:
            assert joiner(chunks, separators, 10) == expected_result
