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
    def __call__(self, yaml_str: str, update_yaml: YamlBlock, block_id: t.Optional[int] = None) -> None:
        yaml_blocks: t.List[YamlBlock] = self.parse_yaml(yaml_str, update_yaml, block_id=block_id)
        self.stdout_yaml(yaml_blocks)

    @staticmethod
    def parse_yaml(
        yaml_str: str,
        update_yaml: YamlBlock,
        *,
        block_id: t.Optional[int] = None,
    ) -> t.List[YamlBlock]:
        yaml_block: YamlBlock
        yaml_blocks: t.List[YamlBlock] = []
        yaml_blocks = [OmegaConf.create(y) for y in yaml.safe_load_all(yaml_str)]

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
        "omegaconf_args", nargs=argparse.REMAINDER, help="dotlist. (ex: 'foo=bar fizz.buzz=\"Hello World!\"' )"
    )
    parser.add_argument(
        "--block_id",
        type=int,
        default=None,
        help="Block id started from 0."
        'If the input is multi block yaml (separated by "---"), manipulate the block specified by this argument.'
        "All block is manipulated, if not specified.",
    )
    parser.add_argument("-f", "--file", type=lambda x: Path(x), default=None, help="yaml file")
    args, unknown = parser.parse_known_args()

    if args.file is not None and args.omegaconf_args:
        raise ValueError("--file and omegaconf_args are exclusive.")

    assert_unknown_args(unknown)
    return args


def main() -> None:

    argparse_args = get_argparse()

    update_yaml: YamlBlock
    if argparse_args.file is not None:
        update_yaml = OmegaConf.load(argparse_args.file)
    else:
        update_yaml = OmegaConf.from_dotlist(argparse_args.omegaconf_args)

    args = Args(update_yaml=update_yaml, block_id=argparse_args.block_id, yaml_file=argparse_args.file)
    logger.debug(f"{args=}")

    yaml_parser = YamlParser()
    yaml_parser("".join(sys.stdin.readlines()), update_yaml=args.update_yaml, block_id=args.block_id)


if __name__ == "__main__":
    # Standard Library
    import logging

    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] - %(message)s",
        level=logging.DEBUG,
    )
    main()
