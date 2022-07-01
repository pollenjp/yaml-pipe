# Standard Library
import typing as t
from logging import NullHandler
from logging import getLogger

# Third Party Library
import pytest
from omegaconf import OmegaConf
from pydantic import BaseModel

# First Party Library
from yaml_pipe.cli import YamlBlock
from yaml_pipe.cli import YamlParser

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class TestYamlParser:
    def setup_class(self) -> None:
        pass

    def teardown_class(self) -> None:
        pass

    def setup_method(self, method: t.Callable[..., t.Any]) -> None:
        self.parser = YamlParser()

    def teardown_method(self, method: t.Callable[..., t.Any]) -> None:
        pass

    class ParseYamlParam(BaseModel):
        yaml_str: str
        update_yaml: YamlBlock
        ret_val: t.List[YamlBlock]
        block_id: t.Optional[int] = None

        class Config:
            arbitrary_types_allowed = True

    @pytest.mark.parametrize(
        "param",
        [
            pytest.param(
                ParseYamlParam(
                    yaml_str="""
---
hoge:
  fuga: FUGA
foo:
  bar: BAR
""",
                    update_yaml=OmegaConf.from_dotlist(["hoge.fuga=fuga", "foo.bar=bar"]),
                    ret_val=[
                        OmegaConf.create(
                            """
hoge:
  fuga: fuga
foo:
  bar: bar
"""
                        )
                    ],
                )
            ),
            pytest.param(
                ParseYamlParam(
                    yaml_str="""
---
hoge:
  fuga: FUGA
---
foo:
  bar: BAR
""",
                    update_yaml=OmegaConf.from_dotlist(["foo.bar=bar"]),
                    block_id=1,
                    ret_val=[
                        OmegaConf.create(
                            """
hoge:
  fuga: FUGA
"""
                        ),
                        OmegaConf.create(
                            """
foo:
  bar: BAR
"""
                        ),
                    ],
                )
            ),
        ],
    )
    def test_parse_yaml(self, param: ParseYamlParam) -> None:
        yaml_blocks: t.List[YamlBlock] = YamlParser.parse_yaml(
            param.yaml_str, param.update_yaml, block_id=param.block_id
        )
        assert len(yaml_blocks) == len(param.ret_val)
        for v1, v2 in zip(yaml_blocks, param.ret_val):
            assert v1, v2
