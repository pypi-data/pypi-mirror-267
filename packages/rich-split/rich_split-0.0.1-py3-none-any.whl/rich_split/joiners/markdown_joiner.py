import copy

from marko.md_renderer import MarkdownRenderer

from rich_split.exceptions import JoinError
from rich_split.joiners.base_joiner import BaseJoiner


class MarkdownJoiner(BaseJoiner):
    def __init__(self, joiner_config):
        self.joiner_config = joiner_config
        temp_joiner_config = self.joiner_config
        self.text_joiner = temp_joiner_config.pop("class")(**self.joiner_config)
        self.renderer = MarkdownRenderer()

    def render(self, element):
        return self.renderer.render(element)

    def __call__(self, document, max_part_length):
        self.join_strings(document, max_part_length)
        for part in map(
            self.render, self.transform_to_parts(document, max_part_length)
        ):
            if len(part) > max_part_length:
                print(repr(part))
                raise JoinError
            yield part

    def join_strings(self, element, max_part_length):
        insertions = []
        for i, child in enumerate(element.children):
            if isinstance(child.children, str):
                continue
            if isinstance(child.children, tuple):
                string_parts = self.text_joiner(
                    child.children[0],
                    child.children[1],
                    # -1 is required, because marko adds \n to every RawText string.
                    # It's not a marko problem, it's just the way markdown works
                    max_part_length - child.additional_markdown_length - 1,
                )
                insertion = []
                for string_part in string_parts:
                    child_copy = copy.deepcopy(child)
                    child_copy.children = string_part
                    child_copy.markdown_element_length = len(string_part)
                    insertion.append(child_copy)
                insertions.append((i, insertion))
                continue
            self.join_strings(child, max_part_length - child.additional_markdown_length)
        for index, insertions in reversed(insertions):
            element.children = (
                element.children[:index] + insertion + element.children[index + 1 :]
            )

    def transform_to_parts(self, element, max_part_length):
        if len(self.render(element)) <= max_part_length:
            return [element]
        dropped_children = []

        def child_gen():
            index = 0
            while dropped_children or index < len(element.children):
                if dropped_children:
                    yield dropped_children.pop(0)
                    continue
                yield element.children[index]
                index += 1

        parts = []
        part_element = copy.deepcopy(element)
        part_element.children = []
        for child in child_gen():
            part_element.children.append(child)
            if len(self.render(part_element)) <= max_part_length:
                continue
            part_element.children.pop()
            if part_element.children:
                parts.append(copy.deepcopy(part_element))
                dropped_children.append(child)
                part_element.children = []
                continue
            for inner_part in self.transform_to_parts(
                child, max_part_length - child.additional_markdown_length
            ):
                new_part = copy.deepcopy(part_element)
                new_part.children = [inner_part]
                parts.append(new_part)
        if part_element.children:
            parts.append(part_element)
        return parts
