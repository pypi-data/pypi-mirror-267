from rich_split.cutters.base_cutter import BaseCutter
from rich_split.exceptions import CutError


class TextCutter(BaseCutter):
    def __init__(
        self,
        separator,
        count_separators=False,
        cutter_config=None,
    ):
        self.separator = separator
        self.count_separators = count_separators
        self.cutter_config = cutter_config or {}

    def __call__(self, text, max_chunk_length):
        chunks = []
        separators = []
        for i, (chunk, separator) in enumerate(self.cut(text)):
            total_length = len(chunk)
            if self.count_separators and separator is not None:
                total_length += len(separator)
            if total_length <= max_chunk_length:
                chunks.append(chunk)
                separators.append(separator)
                continue
            new_chunks, new_separators = self.cut_in_descendant_cutter(
                chunk, max_chunk_length
            )
            chunks.extend(new_chunks)
            separators.extend(new_separators)
            separators[-1] = separator
        return chunks, separators

    def cut(self, text):
        separator = self.separator
        chunks = text.split(separator) if separator else list(text)
        for index in range(len(chunks) - 1):
            yield (chunks[index], separator)
        yield (chunks[-1], None)

    def cut_in_descendant_cutter(self, chunk, max_chunk_length):
        if not self.cutter_config:
            raise CutError
        config = dict(self.cutter_config)
        cls = config.pop("class", self.__class__)
        return cls(**({"count_separators": self.count_separators} | config))(
            chunk, max_chunk_length
        )
