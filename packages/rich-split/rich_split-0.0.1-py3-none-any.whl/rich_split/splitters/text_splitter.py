from rich_split.cutters import TextCutter
from rich_split.joiners import TextJoiner
from rich_split.splitters import BaseSplitter


class TextSplitter(BaseSplitter):
    cutter_config = {
        "class": TextCutter,
        "separator": "\n",
        "cutter_config": {
            "separator": " ",
            "cutter_config": {
                "separator": "",
            },
        },
    }
    joiner_config = {"class": TextJoiner}

    def __init__(
        self,
        *args,
        cutter_config=None,
        joiner_config=None,
        with_separators=False,
        **kwargs,
    ):
        if with_separators:
            cutter_config = (cutter_config or {}) | {"count_separators": True}
            joiner_config = (joiner_config or {}) | {"add_separator_to_parts_end": True}
        super().__init__(
            *args, cutter_config=cutter_config, joiner_config=joiner_config, **kwargs
        )

    def check_is_one_part(self, text):
        return len(text) <= self.max_part_length

    def __call__(self, text):
        if self.not_process_if_only_one_part and self.check_is_one_part(text):
            return [text]
        max_part_length = self.max_part_length - self.calculate_part_header_length(text)
        return self.apply_parts_header(
            self.joiner(*self.cutter(text, max_part_length), max_part_length)
        )
