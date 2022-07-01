# Standard Library
import uuid
from pathlib import Path
from typing import Dict
from typing import List
from typing import TypedDict

# Third Party Library
import nox_poetry
from nox_poetry import Session

python_code_path_list: List[str] = [
    "src",
    "noxfile.py",
]
assert all(isinstance(path, str) for path in python_code_path_list)
env_common: Dict[str, str] = {"PYTHONPATH": f"{Path(__file__).parent / 'src'}"}
nox_tmp_dir: Path = Path(__file__).parent / ".nox_tmp"
python_version_list: List[str] = ["3.8", "3.9", "3.10"]
# python_version_list: List[str] = ["3.10"]


class SessionKwargs(TypedDict, total=False):
    env: Dict[str, str]
    success_codes: List[int]


def install_package(session: Session, dev: bool = False) -> None:
    session.install("--upgrade", "pip")
    session.run("pip", "-V")
    requirements_txt_path: Path = nox_tmp_dir / f"poetry-requirements-{str(uuid.uuid4())}.txt"
    requirements_txt_path.parent.mkdir(exist_ok=True, parents=True)
    try:
        session.install()
    except Exception as e:
        raise e
    else:
        requirements_txt_path.unlink(missing_ok=True)


@nox_poetry.session(python=python_version_list)
def format(session: Session) -> None:
    env: Dict[str, str] = {}
    env.update(env_common)
    kwargs: SessionKwargs = dict(env=env, success_codes=[0, 1])

    # session.install(".")
    session.run_always(*"poetry install".split(" "), external=True)
    session.run(
        "autoflake8",
        "--in-place",
        "--recursive",
        "--remove-unused-variables",
        "--in-place",
        "--exit-zero-even-if-changed",
        *python_code_path_list,
        **kwargs,
    )
    session.run("isort", *python_code_path_list, **kwargs)
    session.run("black", *python_code_path_list, **kwargs)


@nox_poetry.session(python=python_version_list)
def lint(session: Session) -> None:
    env: Dict[str, str] = {}
    env.update(env_common)
    kwargs: SessionKwargs = dict(env=env)

    # session.install(".")
    session.run_always(*"poetry install".split(" "), external=True)
    session.run("flake8", "--statistics", "--count", "--show-source", *python_code_path_list, **kwargs)
    session.run("autoflake8", "--check", "--recursive", "--remove-unused-variables", *python_code_path_list, **kwargs)
    session.run("isort", "--check", *python_code_path_list, **kwargs)
    session.run("black", "--check", *python_code_path_list, **kwargs)
    session.run("mypy", "--check", "--no-incremental", *python_code_path_list, **kwargs)


@nox_poetry.session(python=python_version_list)
def test(session: Session) -> None:
    env: Dict[str, str] = {}
    env.update(env_common)
    kwargs: SessionKwargs = dict(env=env)

    # session.install(".")
    session.run_always(*"poetry install".split(" "), external=True)
    session.run("pytest", **kwargs)
