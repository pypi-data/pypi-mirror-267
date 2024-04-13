from rich_split.cutters.base_cutter import BaseCutter


class MarkdownCutter(BaseCutter):
    def __init__(
        self,
        cutter_config,
    ):
        self.cutter_config = cutter_config
        temp_cutter_config = dict(self.cutter_config)
        self.text_cutter = temp_cutter_config.pop("class")(**temp_cutter_config)

    def __call__(self, element, max_chunk_length):
        if element.markdown_element_length <= max_chunk_length:
            return
        if isinstance(element.children, str):
            # -1 is required, because marko adds \n to every RawText string.
            # It's not a marko problem, it's just the way markdown works
            element.children = self.text_cutter(element.children, max_chunk_length - 1)
            return
        for child in element.children:
            self(child, max_chunk_length - child.additional_markdown_length)
