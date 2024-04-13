from rich_split import MarkdownSplitter, TextSplitter


class TestTextSplitter:
    def test_text_splitter_without_part_header(self):
        fixtures = [
            ("word1", ["word1"]),
            ("word1 word2", ["word1", "word2"]),
            ("word1word2", ["word1word2"]),
            ("word1 longword2", ["word1", "longword2"]),
            ("word1 longlongword2", ["word1 long", "longword2"]),
        ]
        splitter = TextSplitter(10)
        for text, expected_result in fixtures:
            assert splitter(text) == expected_result

    def test_text_splitter_with_fixed_length_part_header(self):
        fixtures = [
            ("word1", ["word1"]),
            ("word1 word2", ["hword1", "hword2"]),
            ("word1word2", ["word1word2"]),
            ("word1word", ["word1word"]),
            ("word1 longword2", ["hword1", "hlongword2"]),
            ("word1 longlongword2", ["hword1 lon", "hglongword", "h2"]),
        ]
        splitter = TextSplitter(
            10, part_header_config={"use_fixed_length_header": True, "header": "h"}
        )
        for text, expected_result in fixtures:
            assert splitter(text) == expected_result

    def test_text_splitter_with_fixed_length_part_header_and_offset(self):
        fixtures = [
            ("word1", ["word1"]),
            ("word1 word2", ["hword1", "hword2"]),
            ("word1word2", ["word1word2"]),
            ("word1word", ["word1word"]),
            ("word1 longword2", ["hword1 l", "hongword", "h2"]),
            ("word1 longlongword2", ["hword1 l", "honglong", "hword2"]),
        ]
        splitter = TextSplitter(
            10,
            part_header_config={
                "use_fixed_length_header": True,
                "header": "h",
                "part_header_length_offset": 2,
            },
        )
        for text, expected_result in fixtures:
            assert splitter(text) == expected_result

    def test_text_splitter_with_fixed_length_part_header_and_header_for_single_part(
        self,
    ):
        fixtures = [
            ("word1", ["hword1"]),
            ("word1 word2", ["hword1", "hword2"]),
            ("word1word2", ["hword1word", "h2"]),
            ("word1word", ["hword1word"]),
            ("word1 longword2", ["hword1", "hlongword2"]),
            ("word1 longlongword2", ["hword1 lon", "hglongword", "h2"]),
        ]
        splitter = TextSplitter(
            10,
            part_header_config={"use_fixed_length_header": True, "header": "h"},
            not_process_if_only_one_part=False,
        )
        for text, expected_result in fixtures:
            assert splitter(text) == expected_result

    def test_text_splitter_with_part_header_with_numbers(self):
        fixtures = [
            ("word1", ["word1"]),
            ("word1 word2", ["1/2word1", "2/2word2"]),
            ("word1word2", ["word1word2"]),
            ("word1word", ["word1word"]),
            ("word1 longword2", ["1/3word1 l", "2/3ongword", "3/32"]),
            ("word1 longlongword2", ["1/3word1 l", "2/3onglong", "3/3word2"]),
        ]
        splitter = TextSplitter(
            10,
            part_header_config={
                "use_part_numbers": True,
                "template": "{current}/{total}",
            },
        )
        for text, expected_result in fixtures:
            assert splitter(text) == expected_result

    def test_text_splitter_with_part_header_with_numbers_and_separators(self):
        fixtures = [
            ("word1", ["word1"]),
            ("word1 word2", ["1/2word1 ", "2/2word2"]),
            ("word1word2", ["word1word2"]),
            ("word1word", ["word1word"]),
            ("word1 longword2", ["1/3word1 l", "2/3ongword", "3/32"]),
            ("word1 longlongword2", ["1/3word1 l", "2/3onglong", "3/3word2"]),
        ]
        splitter = TextSplitter(
            10,
            with_separators=True,
            part_header_config={
                "use_part_numbers": True,
                "template": "{current}/{total}",
            },
        )
        for text, expected_result in fixtures:
            assert splitter(text) == expected_result


class TestMarkdownSplitter:
    def test_with_default_parameters(self):
        splitter = MarkdownSplitter(20)
        fixtures = [
            ("test", ["test"]),
            ("test1test2 test3test4", ["test1test2 \n", "test3test4\n"]),
            (
                "test1\n```\ncode\n```\ntest2\n",
                ["test1\n```\ncode\n```\n", "test2\n"],
            ),
            (
                "testtest1\n```\ncode\n```\ntesttest2\n",
                ["testtest1\n", "```\ncode\n```\n", "testtest2\n"],
            ),
            (
                "head\n```\ncode1\n  code2\n    code3\n```\nfooter\n",
                [
                    "head\n",
                    "```\ncode1\n```\n",
                    "```\n  code2\n```\n",
                    "```\n    code3\n```\n",
                    "footer\n",
                ],
            ),
            (
                "head\n```python\ncode1\n  code2\n    code3\n```\nfooter\n",
                [
                    "head\n",
                    "```python\ncode1\n```\n",
                    "```python\n  \n```\n",
                    "```python\ncode2\n```\n",
                    "```python\n    \n```\n",
                    "```python\ncode3\n```\n",
                    "footer\n",
                ],
            ),
        ]
        for text, expected_result in fixtures:
            assert splitter(text) == expected_result

    def test_extreme_splitting(self):
        splitter = MarkdownSplitter(16)
        assert splitter(
            "head\n```python\ncode1\n  code2\n    code3\n```\nfooter\n"
        ) == [
            "head\n",
            "```python\nc\n```\n",
            "```python\no\n```\n",
            "```python\nd\n```\n",
            "```python\ne\n```\n",
            "```python\n1\n```\n",
            "```python\n \n```\n",
            "```python\n \n```\n",
            "```python\nc\n```\n",
            "```python\no\n```\n",
            "```python\nd\n```\n",
            "```python\ne\n```\n",
            "```python\n2\n```\n",
            "```python\n \n```\n",
            "```python\n \n```\n",
            "```python\n \n```\n",
            "```python\n \n```\n",
            "```python\nc\n```\n",
            "```python\no\n```\n",
            "```python\nd\n```\n",
            "```python\ne\n```\n",
            "```python\n3\n```\n",
            "footer\n",
        ]
