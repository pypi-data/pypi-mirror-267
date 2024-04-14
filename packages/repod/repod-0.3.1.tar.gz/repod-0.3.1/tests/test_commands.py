"""Tests for repod.commands."""

from contextlib import nullcontext as does_not_raise
from pathlib import Path
from subprocess import CalledProcessError  # nosec: B404
from typing import ContextManager

from pytest import mark, raises

from repod import commands


@mark.parametrize("env", [(None), ({"FOO": "BAR"})])
def test__print_env(env: dict[str, str] | None) -> None:
    """Tests for repod.commands._print_env."""
    commands._print_env(env)


@mark.parametrize(
    "cmd, env, debug, echo, quiet, check, cwd, expectation",
    [
        (["ls", "-lah"], {"FOO": "BAR"}, False, False, False, False, None, does_not_raise()),
        (["ls", "-lah"], {"FOO": "BAR"}, True, False, False, False, None, does_not_raise()),
        (["cd", "-f"], {"FOO": "BAR"}, True, False, False, True, None, raises(CalledProcessError)),
    ],
)
@mark.asyncio
def test_run_command(
    cmd: str | list[str],
    env: dict[str, str] | None,
    debug: bool,
    echo: bool,
    quiet: bool,
    check: bool,
    cwd: str | Path | None,
    expectation: ContextManager[str],
) -> None:
    """Tests for repod.commands.run_command."""
    with expectation:
        commands.run_command(cmd=cmd, env=env, debug=debug, echo=echo, quiet=quiet, check=check, cwd=cwd)
