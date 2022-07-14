#!/bin/bash -eux
SCRIPT_DIR="${BASH_SOURCE%/*}"

NAME="test_cli"
cat "${SCRIPT_DIR}/${NAME}.yml" | poetry run python "${SCRIPT_DIR}/src/yaml_pipe/cli.py" --block_id 0 --dotindex "aaa.bbb.ccc"
cat "${SCRIPT_DIR}/${NAME}.yml" | poetry run python "${SCRIPT_DIR}/src/yaml_pipe/cli.py" --block_id 0 --dotlist "aaa.bbb.ccc=CCC"
cat "${SCRIPT_DIR}/${NAME}.yml" | poetry run python "${SCRIPT_DIR}/src/yaml_pipe/cli.py" --block_id 1 --file "${SCRIPT_DIR}/${NAME}_update.yml"
