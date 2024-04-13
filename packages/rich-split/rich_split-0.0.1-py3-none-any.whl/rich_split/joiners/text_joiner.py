from rich_split.joiners.base_joiner import BaseJoiner


class TextJoiner(BaseJoiner):
    def __init__(self, add_separator_to_parts_end=False):
        self.add_separator_to_parts_end = add_separator_to_parts_end

    def __call__(self, chunks, separators, max_part_length):
        parts = []
        part = []
        part_length = 0
        for i, chunk in enumerate(chunks):
            if (delta := part_length - max_part_length) > 0:
                if self.add_separator_to_parts_end:
                    parts.append("".join(part[:-2]))
                    part = part[-2:]
                    part_length -= len(parts[-1])
                else:
                    if len(part[-1]) >= delta:
                        parts.append("".join(part[:-1]))
                        part = []
                        part_length = 0
                    else:
                        parts.append("".join(part[:-3]))
                        part_length -= len(parts[-1]) + len(part[-3])
                        part = part[-2:]
            part.append(chunk)
            part_length += len(chunk)
            separator = separators[i]
            if separator is not None:
                part.append(separator)
                part_length += len(separator)
        if delta := part_length - max_part_length > 0:
            if self.add_separator_to_parts_end:
                parts.append("".join(part[:-1]))
            else:
                parts.append("".join(part[:-2]))
            parts.append(part[-1])
        else:
            parts.append("".join(part))
        return parts
