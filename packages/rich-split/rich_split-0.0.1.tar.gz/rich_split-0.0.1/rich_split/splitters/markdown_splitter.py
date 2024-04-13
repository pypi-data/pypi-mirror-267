from marko import Parser

from rich_split.cutters import MarkdownCutter
from rich_split.joiners import MarkdownJoiner, TextJoiner
from rich_split.splitters import BaseSplitter
from rich_split.splitters.text_splitter import TextSplitter
from rich_split.utils.markdown import (
    add_markdown_children_elements_additional_length,
    add_markdown_elements_length,
)


class MarkdownSplitter(BaseSplitter):
    cutter_config = {
        "class": MarkdownCutter,
        "cutter_config": TextSplitter.cutter_config | {"count_separators": True},
    }
    joiner_config = {
        "class": MarkdownJoiner,
        "joiner_config": {"class": TextJoiner, "add_separator_to_parts_end": True},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = Parser()

    def check_is_one_part(self, text):
        return len(text) <= self.max_part_length

    def __call__(self, text):
        if self.not_process_if_only_one_part and self.check_is_one_part(text):
            return [text]
        max_part_length = self.max_part_length - self.calculate_part_header_length(text)
        document = self.parser.parse(text)
        add_markdown_elements_length(document)
        add_markdown_children_elements_additional_length(document)
        self.cutter(document, max_part_length)
        parts_gen = self.joiner(document, max_part_length)
        return self.apply_parts_header(parts_gen)
