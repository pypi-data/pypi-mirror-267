import copy
import math
from abc import ABC, abstractmethod


class BaseSplitter(ABC):
    cutter_config = None
    joiner_config = None
    part_header_config = None

    def __init__(
        self,
        max_part_length,
        cutter_config=None,
        joiner_config=None,
        part_header_config=None,
        not_process_if_only_one_part=True,
    ):
        self.max_part_length = max_part_length
        self.cutter_config = (self.cutter_config or {}) | (cutter_config or {})
        self.cutter_config = copy.deepcopy(self.cutter_config)
        self.joiner_config = (self.joiner_config or {}) | (joiner_config or {})
        self.joiner_config = copy.deepcopy(self.joiner_config)
        self.part_header_config = (self.part_header_config or {}) | (
            part_header_config or {}
        )
        self.part_header_config = copy.deepcopy(self.part_header_config)
        self.not_process_if_only_one_part = not_process_if_only_one_part
        cutter_config = dict(self.cutter_config)
        cls = cutter_config.pop("class")
        self.cutter = cls(**cutter_config)
        joiner_config = dict(self.joiner_config)
        cls = joiner_config.pop("class")
        self.joiner = cls(**joiner_config)

    @abstractmethod
    def check_is_one_part(self, text):
        return False

    @abstractmethod
    def __call__(self, text):
        pass

    def calculate_part_header_length(self, text):
        part_header_length = 0
        if self.part_header_config.get("use_part_numbers", False):
            min_part_count = math.ceil(len(text) / self.max_part_length)
            if min_part_count < 10:
                min_part_count = round(min_part_count * 1.2)
            part_header_length = len(
                self.part_header_config["template"].format(
                    current=min_part_count, total=min_part_count
                )
            )
        elif self.part_header_config.get("use_fixed_length_header", False):
            part_header_length = len(self.part_header_config["header"])
        part_header_length += self.part_header_config.get(
            "part_header_length_offset", 0
        )
        return part_header_length

    def apply_parts_header(self, parts):
        if self.part_header_config.get("use_part_numbers", False):
            add_leading_zeros = self.part_header_config.get("add_leading_zeros", False)
            total_parts = len(parts)
            template = self.part_header_config["template"]
            new_parts = []
            for part_number, part in enumerate(parts, start=1):
                part_number = (
                    str(part_number).zfill(total_parts)
                    if add_leading_zeros
                    else part_number
                )
                new_parts.append(
                    self.apply_part_header(
                        template.format(current=part_number, total=total_parts), part
                    )
                )
        elif self.part_header_config.get("use_fixed_length_header", False):
            header = self.part_header_config["header"]
            new_parts = [self.apply_part_header(header, part) for part in parts]
        else:
            new_parts = list(parts)
        return new_parts

    def apply_part_header(self, header, part):
        return header + part
