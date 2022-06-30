# Standard Library
import argparse
import os
import sys
import typing as t
from logging import NullHandler
from logging import getLogger

# Third Party Library
from omegaconf import DictConfig
from omegaconf import ListConfig
from omegaconf import OmegaConf

logger = getLogger(__name__)
logger.addHandler(NullHandler())


def assert_unknown_args(args: t.List[str]) -> None:
    unknown_args: t.List[str] = []
    for arg in args:
        if arg.startswith("--"):
            unknown_args.append(arg)
    if unknown_args:
        raise ValueError(f"See --help. Unknown arguments: {unknown_args}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Get yaml as stdin and parse it!")
    # parser.add_argument("args", action="store", type=str, help="dotlist. (ex: 'foo=bar fizz.buzz=\"Hello World!\"' )")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="dotlist. (ex: 'foo=bar fizz.buzz=\"Hello World!\"' )")
    parser.add_argument(
        "--block_id",
        type=int,
        default=None,
        help="Block id started from 0."
        'If the input is multi block yaml (separated by "---"), manipulate the block specified by this argument.'
        "All block is manipulated, if not specified.",
    )

    argparse_args, unknown = parser.parse_known_args()
    assert_unknown_args(unknown)
    omegaconf_args: DictConfig = OmegaConf.from_dotlist(argparse_args.args)

    yaml_blocks: t.List[t.Union[DictConfig, ListConfig]] = []
    yaml_block: t.Union[DictConfig, ListConfig]
    yaml_seprators: t.Set[str] = set(("---\n", f"---{os.linesep}"))

    line: str
    block_lines: t.List[str] = []
    for line in sys.stdin.readlines():  # TODO: support other inputs
        if line in yaml_seprators:
            yaml_block = OmegaConf.create("".join(block_lines))
            if len(yaml_block) > 0:
                yaml_blocks.append(yaml_block)
            block_lines = []
            continue

        block_lines.append(line)

    logger.debug(f"cli_args= {omegaconf_args}")

    if argparse_args.block_id is not None:
        yaml_blocks[argparse_args.block_id] = OmegaConf.merge(yaml_blocks[argparse_args.block_id], omegaconf_args)
    else:
        for i, yaml_block in enumerate(yaml_blocks):
            yaml_blocks[i] = OmegaConf.merge(yaml_block, omegaconf_args)

    for yaml_block in yaml_blocks:
        print("---")
        print(OmegaConf.to_yaml(yaml_block))


if __name__ == "__main__":
    # Standard Library
    import logging

    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] - %(message)s",
        level=logging.INFO,
    )
    main()
