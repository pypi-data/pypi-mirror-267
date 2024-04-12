from typing import List
from rrcgeoviz.JsonCreatorClasses.Blocks.BaseBlock import BaseBlock
import panel as pn


class BaseSection:
    blocks: List[BaseBlock] = []

    def header_text(self):
        raise NotImplementedError("Add header text here")

    def generate_blocks(self):
        raise NotImplementedError("Return array of panel components")

    def get_json_section_name(self):
        raise NotImplementedError("Return JSON section name here")

    def dict_or_array(self):
        raise NotImplementedError("return either string 'dict' or 'array")

    def get_block_values(self):
        out = []
        for block in self.blocks:
            out.append(block.get_value())

    def generate_section(self, setGrid=False):
        self.blocks = self.generate_blocks()

        output = pn.Column()
        output.append(
            pn.Row(
                pn.layout.HSpacer(),
                pn.widgets.StaticText(
                    value=self.header_text(),
                ),
                pn.layout.HSpacer(),
            )
        )

        if not setGrid:
            for block in self.blocks:
                row = pn.Row(
                    pn.layout.HSpacer(), block.generate_block(), pn.layout.HSpacer()
                ).servable()
                output.append(row)
        else:
            useable_feature_blocks = []
            for block in self.blocks:
                useable_feature_blocks.append(
                    pn.Column(block.generate_block(), sizing_mode="stretch_width")
                )
            output.append(pn.GridBox(*useable_feature_blocks, ncols=5))

        return output

    def __init__(self) -> None:
        self.blocks = None

    def get_blocks(self):
        if self.blocks is None:
            self.blocks = self.generate_blocks()
            return self.blocks
        else:
            return self.blocks
