#!/usr/bin/env python3
# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import dataclasses
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from contextlib import ExitStack
from functools import partial
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from zstarfile import ZSTarfile
from zstarfile.extra import open_write_compressed

from go_vendor_tools import __version__
from go_vendor_tools.archive import add_files_to_archive
from go_vendor_tools.config.archive import get_go_dependency_update_commands
from go_vendor_tools.config.base import BaseConfig, load_config
from go_vendor_tools.exceptions import ArchiveError
from go_vendor_tools.specfile_sources import get_path_and_output_from_specfile

try:
    import tomlkit
except ImportError:
    HAS_TOMLKIT = False
else:
    HAS_TOMLKIT = True
    from go_vendor_tools.cli.utils import load_tomlkit_if_exists

if TYPE_CHECKING:
    from _typeshed import StrPath

DEFAULT_OUTPUT = "vendor.tar.bz2"
ARCHIVE_FILES = (Path("go.mod"), Path("go.sum"), Path("vendor"))
OPTIONAL_FILES = frozenset({Path("go.sum")})
GO_PROXY_ENV = {
    "GOPROXY": "https://proxy.golang.org,direct",
    "GOSUMDB": "sum.golang.org",
}


def need_tomlkit(action="this action"):
    if not HAS_TOMLKIT:
        message = f"tomlkit is required for {action}. Please install it!"
        sys.exit(message)


def run_command(
    runner: Callable[..., subprocess.CompletedProcess],
    command: Sequence[StrPath],
    **kwargs: Any,
) -> subprocess.CompletedProcess:
    print(f"$ {shlex.join(map(os.fspath, command))}")  # type: ignore[arg-type]
    return runner(command, **kwargs)


@dataclasses.dataclass()
class CreateArchiveArgs:
    path: Path
    output: Path
    use_top_level_dir: bool
    use_module_proxy: bool
    tidy: bool
    idempotent: bool
    compresslevel: int | None
    compression_type: str | None
    config_path: Path
    config: BaseConfig
    write_config: bool
    _explicitly_passed: list[str] = dataclasses.field(default_factory=list, repr=False)

    CONFIG_OPTS: ClassVar[tuple[str, ...]] = (
        "use_module_proxy",
        "use_top_level_dir",
        "tidy",
        "compresslevel",
        "compression_type",
    )

    @classmethod
    def construct(cls, **kwargs: Any) -> CreateArchiveArgs:
        if kwargs.pop("subcommand") != "create":
            raise AssertionError  # pragma: no cover
        _explicitly_passed = list(kwargs)
        kwargs["config"] = load_config(kwargs["config_path"], kwargs["write_config"])
        for opt in cls.CONFIG_OPTS:
            if kwargs.get(opt) is None:
                kwargs[opt] = kwargs["config"]["archive"][opt]
        if not kwargs["path"].exists():
            raise ArchiveError(f"{kwargs['path']} does not exist!")
        if kwargs["write_config"]:
            need_tomlkit("--write-config")
            if not kwargs["config_path"]:
                raise ArchiveError("--write-config requires --config to be set")
        return CreateArchiveArgs(**kwargs, _explicitly_passed=_explicitly_passed)

    def write_config_opts(self) -> None:
        need_tomlkit("write_config_opts")
        loaded = load_tomlkit_if_exists(self.config_path)
        config = loaded.setdefault("archive", {})
        for opt in self._explicitly_passed:
            if opt not in self.CONFIG_OPTS:
                continue
            config[opt] = getattr(self, opt)
        with open(self.config_path, "w", encoding="utf-8") as fp:
            tomlkit.dump(loaded, fp)


@dataclasses.dataclass()
class OverrideArgs:
    config_path: Path
    import_path: str
    version: str

    @classmethod
    def construct(cls, **kwargs: Any) -> OverrideArgs:
        if kwargs.pop("subcommand") != "override":
            raise AssertionError  # pragma: no cover
        return cls(**kwargs)


def parseargs(argv: list[str] | None = None) -> CreateArchiveArgs | OverrideArgs:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.required = True
    create_subparser = subparsers.add_parser("create")
    create_subparser.add_argument("--version", action="version", version=__version__)
    create_subparser.add_argument(
        "-O", "--output", type=Path, default=None, help=f"Default: {DEFAULT_OUTPUT}"
    )
    create_subparser.add_argument(
        "--top-level-dir",
        dest="use_top_level_dir",
        action=argparse.BooleanOptionalAction,
        default=argparse.SUPPRESS,
    )
    create_subparser.add_argument(
        "--use-module-proxy",
        action=argparse.BooleanOptionalAction,
        default=argparse.SUPPRESS,
    )
    create_subparser.add_argument(
        "-p", action="store_true", dest="use_module_proxy", default=argparse.SUPPRESS
    )
    create_subparser.add_argument("-c", "--config", type=Path, dest="config_path")
    create_subparser.add_argument(
        "--tidy",
        help="%(default)s",
        action=argparse.BooleanOptionalAction,
        default=argparse.SUPPRESS,
    )
    create_subparser.add_argument(
        "-I",
        "--idempotent",
        action="store_true",
        help="Only generate archive if OUTPUT does not already exist",
    )
    create_subparser.add_argument(
        "--compresslevel", type=int, default=argparse.SUPPRESS
    )
    create_subparser.add_argument(
        "--compression",
        dest="compression_type",
        metavar="COMPRESSION_TYPE",
        help=f"Choices: {list(ZSTarfile.OPEN_METH)}",
        default=argparse.SUPPRESS,
    )
    create_subparser.add_argument("--write-config", action="store_true")
    create_subparser.add_argument("path", type=Path)
    override_subparser = subparsers.add_parser("override")
    override_subparser.add_argument(
        "--config", type=Path, dest="config_path", required=True
    )
    override_subparser.add_argument("import_path")
    override_subparser.add_argument("version")

    args = parser.parse_args(argv)
    if args.subcommand == "create":
        return CreateArchiveArgs.construct(**vars(args))
    elif args.subcommand == "override":
        return OverrideArgs.construct(**vars(args))
    else:
        raise RuntimeError("unreachable")


def _create_archive_read_from_specfile(args: CreateArchiveArgs) -> None:
    if args.output:
        sys.exit("Cannot pass --output when reading paths from a specfile!")
    spec_path = args.path
    args.path, args.output = get_path_and_output_from_specfile(args.path)
    if not args.path.is_file():
        sys.exit(
            f"{args.path} does not exist!"
            f" Run 'spectool -g {spec_path}' and try again!"
        )


def create_archive(args: CreateArchiveArgs) -> None:
    _already_checked_is_file = False
    cwd = args.path
    if args.path.suffix == ".spec":
        _create_archive_read_from_specfile(args)
        _already_checked_is_file = True
    else:
        args.output = Path(DEFAULT_OUTPUT)
    if args.idempotent and args.output.exists():
        print(f"{args.output} already exists")
        sys.exit()
    with ExitStack() as stack:
        try:
            tf = stack.enter_context(
                open_write_compressed(
                    args.output,
                    compression_type=args.compression_type,
                    compresslevel=args.compresslevel,
                )
            )
        except ValueError as exc:
            sys.exit(f"Invalid --output value: {exc}")
        # Treat as an archive if it's not a directory
        if _already_checked_is_file or args.path.is_file():
            print(f"* Treating {args.path} as an archive. Unpacking...")
            cwd = Path(stack.enter_context(tempfile.TemporaryDirectory()))
            shutil.unpack_archive(args.path, cwd)
            cwd /= next(cwd.iterdir())
        env = os.environ | GO_PROXY_ENV if args.use_module_proxy else None
        runner = partial(subprocess.run, cwd=cwd, check=True, env=env)
        pre_commands = chain(
            args.config["archive"]["pre_commands"],
            get_go_dependency_update_commands(
                args.config["archive"]["dependency_overrides"]
            ),
        )
        for command in pre_commands:
            run_command(runner, command)
        if args.tidy:
            run_command(runner, ["go", "mod", "tidy"])
        run_command(runner, ["go", "mod", "vendor"])
        # Create vendor directory so it is there even if there are no
        # dependencies to download
        (vdir := cwd / "vendor").mkdir(exist_ok=True)
        (vdir / "modules.txt").touch(exist_ok=True)
        for command in args.config["archive"]["post_commands"]:
            run_command(runner, command)
        print("Creating archive...")
        add_files_to_archive(
            tf,
            Path(cwd),
            ARCHIVE_FILES,
            top_level_dir=args.use_top_level_dir,
            optional_files=OPTIONAL_FILES,
        )
        if args.write_config:
            args.write_config_opts()


def override_command(args: OverrideArgs) -> None:
    need_tomlkit()
    loaded = load_tomlkit_if_exists(args.config_path)
    overrides = loaded.setdefault("archive", {}).setdefault("dependency_overrides", {})
    overrides[args.import_path] = args.version
    with open(args.config_path, "w", encoding="utf-8") as fp:
        tomlkit.dump(loaded, fp)


def main(argv: list[str] | None = None) -> None:
    args = parseargs(argv)
    if isinstance(args, CreateArchiveArgs):
        create_archive(args)
    elif isinstance(args, OverrideArgs):
        override_command(args)


if __name__ == "__main__":
    try:
        main()
    except ArchiveError as exc:
        sys.exit(str(exc))
