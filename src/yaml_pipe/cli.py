# Standard Library
import argparse
import sys
import typing as t
from dataclasses import dataclass
from logging import NullHandler
from logging import getLogger
from pathlib import Path

# Third Party Library
import yaml
from omegaconf import DictConfig
from omegaconf import ListConfig
from omegaconf import OmegaConf

logger = getLogger(__name__)
logger.addHandler(NullHandler())


YamlBlock = t.Union[DictConfig, ListConfig]


class YamlParser:
    def update(self, yaml_str: str, update_yaml: YamlBlock, block_id: t.Optional[int] = None) -> t.List[YamlBlock]:
        yaml_blocks: t.List[YamlBlock]
        yaml_blocks = self.parse_yaml(yaml_str)
        yaml_blocks = self.update_yaml_blocks(yaml_blocks, update_yaml, block_id=block_id)
        return yaml_blocks

    @staticmethod
    def parse_yaml(
        yaml_str: str,
    ) -> t.List[YamlBlock]:
        yaml_block: YamlBlock
        yaml_blocks: t.List[YamlBlock] = [OmegaConf.create(y) for y in yaml.safe_load_all(yaml_str)]
        return yaml_blocks

    @staticmethod
    def update_yaml_blocks(
        yaml_blocks: t.List[YamlBlock],
        update_yaml: YamlBlock,
        *,
        block_id: t.Optional[int] = None,
    ) -> t.List[YamlBlock]:
        if block_id is not None:
            yaml_blocks[block_id] = OmegaConf.merge(yaml_blocks[block_id], update_yaml)
        else:
            for i, yaml_block in enumerate(yaml_blocks):
                yaml_blocks[i] = OmegaConf.merge(yaml_block, update_yaml)

        return yaml_blocks

    @staticmethod
    def stdout_yaml(yaml_blocks: t.List[YamlBlock]) -> None:
        for yaml_block in yaml_blocks:
            print("---")
            print(OmegaConf.to_yaml(yaml_block))

    @staticmethod
    def extract_value(
        yaml_block: YamlBlock,
        dot_key: str,
    ) -> YamlBlock:
        if ":" in dot_key:
            raise NotImplementedError("Support only view.")

        ks = dot_key.strip()
        _target: YamlBlock = yaml_block
        k_list = ks.split(".")
        for k in k_list:
            # list parse
            k, *tmp = k.split("[")
            if k != "":
                _target = t.cast(DictConfig, _target)[k]
            if len(tmp) > 0:
                for i in [int(x[:-1:]) for x in tmp]:  # indices
                    _target = _target[i]
        logger.debug(f"{type( _target )=}")
        return _target


def assert_unknown_args(args: t.List[str]) -> None:
    unknown_args: t.List[str] = []
    for arg in args:
        if arg.startswith("--"):
            unknown_args.append(arg)
    if unknown_args:
        raise ValueError(f"See --help. Unknown arguments: {unknown_args}")


@dataclass
class Args:
    update_yaml: YamlBlock
    block_id: t.Optional[int] = None
    yaml_file: t.Optional[str] = None


def get_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Get yaml as stdin and parse it!")
    parser.add_argument(
        "--block_id",
        type=int,
        default=None,
        help="Block id 0 origin (the index is started from 0)."
        'If the input is multi block yaml (separated by "---"), manipulate the block specified by this argument.'
        "All block is manipulated, if not specified.",
    )
    args_group1 = parser.add_mutually_exclusive_group(required=True)
    args_group1.add_argument("--file", type=lambda x: Path(x), default=None, help="yaml file")
    args_group1.add_argument(
        "--dotindex",
        nargs=argparse.REMAINDER,
        help=(
            "Dot and list-index format. e.g. --dotindex 'xxx.yyy[0].zzz: 123'."
            "Support only view."
            "If each key has a value, update yaml. Otherwise, read yaml."
        ),
    )
    args_group1.add_argument(
        "--dotlist",
        nargs=argparse.REMAINDER,
        help="dotlist. e.g. 'foo=bar fizz.buzz=\"Hello World!\"'",
    )

    args, unknown = parser.parse_known_args()

    assert_unknown_args(unknown)
    return args


def main() -> None:

    argparse_args = get_argparse()

    yaml_blocks: t.List[YamlBlock]

    # view values
    if argparse_args.dotindex:
        yaml_blocks = YamlParser.parse_yaml(yaml_str="\n".join(sys.stdin.readlines()))
        yaml_block: YamlBlock
        if len(yaml_blocks) == 1:
            yaml_block = yaml_blocks[0]
        else:
            if argparse_args.block_id is None:
                raise ValueError("Multi block yaml and no block_id specified.")
            yaml_block = yaml_blocks[argparse_args.block_id]

        for dot_key in argparse_args.dotindex:
            val: t.Union[str, int, t.List[t.Any], t.Dict[str, t.Any], YamlBlock] = YamlParser.extract_value(
                yaml_block, dot_key
            )
            if isinstance(val, (list, dict, DictConfig, ListConfig)):
                print(f"{OmegaConf.to_yaml(val)}")
            else:
                print(f"{val}")
        return

    # edit values

    update_yaml: YamlBlock
    if argparse_args.file is not None:
        update_yaml = OmegaConf.load(argparse_args.file)
    elif argparse_args.dotlist:
        update_yaml = OmegaConf.from_dotlist(argparse_args.dotlist)

    args = Args(update_yaml=update_yaml, block_id=argparse_args.block_id, yaml_file=argparse_args.file)
    logger.debug(f"{args=}")
    yaml_blocks = YamlParser().update(
        "".join(sys.stdin.readlines()), update_yaml=args.update_yaml, block_id=args.block_id
    )
    YamlParser.stdout_yaml(yaml_blocks)


if __name__ == "__main__":
    # Standard Library
    import logging

    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] - %(message)s",
        level=logging.DEBUG,
    )
    main()
