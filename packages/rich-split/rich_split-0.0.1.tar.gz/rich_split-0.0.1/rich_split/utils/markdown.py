import copy
import itertools

from marko.md_renderer import MarkdownRenderer

renderer = MarkdownRenderer()


def add_markdown_elements_length(element):
    lists = [[element]]
    for e in itertools.chain.from_iterable(lists):
        e.markdown_element_length = len(renderer.render(e))
        if not isinstance(e.children, str):
            lists.append(e.children)


def add_tree_elements_length(element):
    element.tree_element_length = 0
    if isinstance(element.children, str):
        element.tree_element_length = len(element.children)
        return
    for child in element.children:
        add_tree_elements_length(child)
        element.tree_element_length += child.tree_element_length


def add_markdown_children_elements_additional_length(element):
    if isinstance(element.children, str):
        return
    if len(element.children) == 1:
        element.children[0].additional_markdown_length = (
            element.markdown_element_length
            - element.children[0].markdown_element_length
        )
        add_markdown_children_elements_additional_length(element.children[0])
    else:
        element_copy = copy.deepcopy(element)
        for child in element.children:
            element_copy.children = [child]
            child.additional_markdown_length = (
                len(renderer.render(element_copy)) - child.markdown_element_length
            )
            add_markdown_children_elements_additional_length(child)
