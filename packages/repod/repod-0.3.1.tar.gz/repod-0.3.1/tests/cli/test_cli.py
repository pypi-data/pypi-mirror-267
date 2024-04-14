"""Tests for repod.cli.cli."""

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from logging import DEBUG
from pathlib import Path
from random import sample
from re import Match, fullmatch
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from pytest import LogCaptureFixture, mark, raises

from repod import commands
from repod.cli import cli
from repod.common.enums import (
    ArchitectureEnum,
    FilesVersionEnum,
    PackageDescVersionEnum,
    tar_compression_types_for_filename_regex,
)
from repod.config import UserSettings
from repod.config.defaults import DEFAULT_DATABASE_COMPRESSION


@mark.parametrize(
    "message, argparser",
    [
        ("foo", None),
        ("foo", ArgumentParser()),
    ],
)
@patch("repod.cli.cli.exit")
def test_exit_on_error(exit_mock: Mock, message: str, argparser: ArgumentParser | None) -> None:
    """Tests for repod.cli.cli.exit_on_error."""
    cli.exit_on_error(message=message, argparser=argparser)
    exit_mock.assert_called_once_with(1)


@mark.parametrize(
    "args, calls_exit_on_error",
    [
        (Namespace(package="inspect", buildinfo=False, mtree=False, pkginfo=False, with_signature=False), False),
        (Namespace(package="inspect", buildinfo=True, mtree=False, pkginfo=False, with_signature=False), False),
        (Namespace(package="inspect", buildinfo=False, mtree=True, pkginfo=False, with_signature=False), False),
        (Namespace(package="inspect", buildinfo=False, mtree=False, pkginfo=True, with_signature=False), False),
        (Namespace(package="inspect", buildinfo=False, mtree=False, pkginfo=False, with_signature=True), False),
        (Namespace(package="inspect", buildinfo=True, mtree=False, pkginfo=False, with_signature=True), False),
        (Namespace(package="inspect", buildinfo=False, mtree=True, pkginfo=False, with_signature=True), False),
        (Namespace(package="inspect", buildinfo=False, mtree=False, pkginfo=True, with_signature=True), False),
        (Namespace(package="foo"), True),
    ],
)
@patch("repod.cli.cli.exit_on_error")
def test_repod_file_package(
    exit_on_error_mock: Mock,
    caplog: LogCaptureFixture,
    default_package_file: tuple[Path, ...],
    tmp_path: Path,
    args: Namespace,
    calls_exit_on_error: bool,
) -> None:
    """Tests for repod.cli.cli.repod_file_package."""
    caplog.set_level(DEBUG)

    settings_mock = Mock()
    args.file = [default_package_file[0]]

    cli.repod_file_package(args=args, settings=settings_mock)
    if calls_exit_on_error:
        exit_on_error_mock.assert_called_once()


@mark.parametrize(
    "args, calls_exit_on_error",
    [
        (
            Namespace(repo="importdb", architecture=ArchitectureEnum.ANY, debug=False, staging=False, testing=False),
            False,
        ),
        (
            Namespace(
                repo="writedb",
                architecture=ArchitectureEnum.ANY,
                debug=False,
                staging=False,
                testing=False,
            ),
            False,
        ),
        (
            Namespace(
                repo="importpkg",
                architecture=ArchitectureEnum.ANY,
                dry_run=True,
                with_signature=False,
                debug=False,
                staging=False,
                testing=False,
            ),
            False,
        ),
        (Namespace(repo="foo"), True),
    ],
)
@patch("repod.cli.cli.repod_file_repo_importpkg")
@patch("repod.cli.cli.write_sync_databases")
@patch("repod.cli.cli.exit_on_error")
def test_repod_file_repo(
    exit_on_error_mock: Mock,
    write_sync_databases_mock: Mock,
    repod_file_repo_importpkg_mock: Mock,
    caplog: LogCaptureFixture,
    default_package_file: tuple[Path, ...],
    outputpackagebasev1_json_files_in_dir: Path,
    default_sync_db_file: tuple[Path, Path],
    tmp_path: Path,
    args: Namespace,
    calls_exit_on_error: bool,
) -> None:
    """Tests for repod.cli.cli.repod_file_repo."""
    caplog.set_level(DEBUG)

    settings_mock = Mock()
    settings_mock.get_repo_path = Mock(return_value=tmp_path)
    settings_mock.get_repo_database_compression = Mock(return_value=DEFAULT_DATABASE_COMPRESSION)
    syncdb_settings_mock = Mock()
    syncdb_settings_mock.desc_version = PackageDescVersionEnum.DEFAULT
    syncdb_settings_mock.files_version = FilesVersionEnum.DEFAULT
    settings_mock.syncdb_settings = syncdb_settings_mock

    if args.repo == "importdb":
        args.file = default_sync_db_file[1]
        args.name = tmp_path
    if args.repo == "writedb":
        args.name = "default"

    cli.repod_file_repo(args=args, settings=settings_mock)
    if args.repo == "importpkg":
        repod_file_repo_importpkg_mock.assert_called_once()
    if args.repo == "writedb":
        write_sync_databases_mock.assert_called_once()
    if calls_exit_on_error:
        exit_on_error_mock.assert_called_once()


@mark.parametrize("dry_run", [(True), (False)])
@patch("repod.cli.cli.add_packages_dryrun")
@patch("repod.cli.cli.add_packages")
def test_repod_file_repo_importpkg(
    add_packages_mock: Mock,
    add_packages_dryrun_mock: Mock,
    dry_run: bool,
    usersettings: UserSettings,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.cli.cli.repod_file_importpkg."""
    caplog.set_level(DEBUG)

    file: list[Path] = []
    name = Path("foo")
    architecture = ArchitectureEnum.ANY
    debug_bool = False
    staging_bool = False
    testing_bool = False
    with_signature = True
    namespace = Namespace(
        file=file,
        name=name,
        architecture=architecture,
        debug=debug_bool,
        staging=staging_bool,
        testing=testing_bool,
        with_signature=with_signature,
        dry_run=dry_run,
        source_url=[],
    )

    cli.repod_file_repo_importpkg(args=namespace, settings=usersettings)
    if dry_run:
        add_packages_dryrun_mock.assert_called_once_with(
            settings=usersettings,
            files=file,
            repo_name=name,
            repo_architecture=architecture,
            debug_repo=debug_bool,
            with_signature=with_signature,
            pkgbase_urls={},
        )
    else:
        add_packages_mock.assert_called_once_with(
            settings=usersettings,
            files=file,
            repo_name=name,
            repo_architecture=architecture,
            debug_repo=debug_bool,
            staging_repo=staging_bool,
            testing_repo=testing_bool,
            with_signature=with_signature,
            pkgbase_urls={},
        )


@mark.parametrize(
    "args, calls_exit_on_error",
    [(Namespace(schema="export"), False), (Namespace(schema="foo"), True)],
)
@patch("repod.cli.cli.exit_on_error")
def test_repod_file_schema(
    exit_on_error_mock: Mock,
    tmp_path: Path,
    args: Namespace,
    calls_exit_on_error: bool,
) -> None:
    """Tests for repod.cli.cli.repod_file_schema."""
    if args.schema == "export":
        args.dir = tmp_path

    cli.repod_file_schema(args=args)
    if calls_exit_on_error:
        exit_on_error_mock.assert_called_once()


@mark.parametrize(
    "args, calls_exit_on_error",
    [
        (
            Namespace(subcommand="package", config=None, system=False, verbose_mode=False, debug_mode=False),
            False,
        ),
        (
            Namespace(
                subcommand="package", config=Path("/foo.conf"), system=False, verbose_mode=False, debug_mode=False
            ),
            False,
        ),
        (
            Namespace(subcommand="package", config=None, system=False, verbose_mode=True, debug_mode=False),
            False,
        ),
        (
            Namespace(subcommand="package", config=None, system=False, verbose_mode=False, debug_mode=True),
            False,
        ),
        (
            Namespace(subcommand="package", config=None, system=False, verbose_mode=True, debug_mode=True),
            False,
        ),
        (
            Namespace(subcommand="repo", config=None, system=False, verbose_mode=False, debug_mode=False),
            False,
        ),
        (
            Namespace(subcommand="schema", config=None, system=False, verbose_mode=False, debug_mode=False),
            False,
        ),
        (
            Namespace(subcommand="foo", config=None, system=False, verbose_mode=False, debug_mode=False),
            True,
        ),
        (
            Namespace(subcommand="package", config=None, system=True, verbose_mode=False, debug_mode=False),
            False,
        ),
        (
            Namespace(subcommand="package", config=None, system=True, verbose_mode=True, debug_mode=False),
            False,
        ),
        (
            Namespace(subcommand="package", config=None, system=True, verbose_mode=False, debug_mode=True),
            False,
        ),
        (
            Namespace(subcommand="package", config=None, system=True, verbose_mode=True, debug_mode=True),
            False,
        ),
        (
            Namespace(subcommand="repo", config=None, system=True, verbose_mode=False, debug_mode=False),
            False,
        ),
        (
            Namespace(subcommand="schema", config=None, system=True, verbose_mode=False, debug_mode=False),
            False,
        ),
        (
            Namespace(subcommand="foo", config=None, system=True, verbose_mode=False, debug_mode=False),
            True,
        ),
    ],
)
@patch("repod.cli.cli.repod_file_schema")
@patch("repod.cli.cli.repod_file_repo")
@patch("repod.cli.cli.repod_file_package")
@patch("repod.cli.argparse.ArgumentParser.parse_args")
@patch("repod.cli.cli.SystemSettings")
@patch("repod.cli.cli.UserSettings")
@patch("repod.cli.cli.exit_on_error")
def test_repod_file(
    exit_on_error_mock: Mock,
    usersettings_mock: Mock,
    systemsettings_mock: Mock,
    parse_args_mock: Mock,
    repod_file_package_mock: Mock,
    repod_file_repo_mock: Mock,
    repod_file_schema_mock: Mock,
    args: Namespace,
    calls_exit_on_error: bool,
) -> None:
    """Tests for repod.cli.cli.repod_file."""
    user_settings = Mock()
    usersettings_mock.return_value = user_settings
    system_settings = Mock()
    systemsettings_mock.return_value = system_settings

    parse_args_mock.return_value = args

    cli.repod_file()
    match args.subcommand:
        case "package":
            repod_file_package_mock.assert_called_once_with(
                args=args, settings=system_settings if args.system else user_settings
            )
        case "repo":
            repod_file_repo_mock.assert_called_once_with(
                args=args, settings=system_settings if args.system else user_settings
            )
        case "schema":
            repod_file_schema_mock.assert_called_once_with(args=args)
    match args.system:
        case True:
            systemsettings_mock.assert_called_once()
        case False:
            usersettings_mock.assert_called_once()

    if calls_exit_on_error:
        exit_on_error_mock.assert_called_once()


@patch("repod.cli.argparse.ArgumentParser.parse_args")
def test_repod_file_raise_on_argumenterror(parse_args_mock: Mock) -> None:
    """Tests for repod.cli.cli.repod_file raising on ArgumentTypeError."""
    parse_args_mock.side_effect = ArgumentTypeError
    with raises(RuntimeError):
        cli.repod_file()


def transform_databases(repo_name: str, base_path: Path) -> None:
    """Transform a repository sync database to management repository and back.

    Repository sync databases in default locations on pacman based distributions (i.e. /var/lib/pacman/sync/) are
    considered by name.

    Parameters
    ----------
    repo_name: str
        Name of the repository (identifying a local repository sync database)
    base_path: Path
        The base directory below which repod specific data is stored
    """
    custom_config = f"""
    [[repositories]]

    architecture = "x86_64"
    name = "{base_path}/data/repo/package/{repo_name}"
    debug = "{base_path}/data/repo/package/{repo_name}-debug"
    staging = "{base_path}/data/repo/package/{repo_name}-staging"
    staging_debug = "{base_path}/data/repo/package/{repo_name}-staging-debug"
    testing = "{base_path}/data/repo/package/{repo_name}-testing"
    testing_debug = "{base_path}/data/repo/package/{repo_name}-testing-debug"
    package_pool = "{base_path}/data/pool/package/{repo_name}"
    source_pool = "{base_path}/data/pool/source/{repo_name}"

    [repositories.management_repo]
    directory = "{base_path}/management/{repo_name}"
    """

    config_path = base_path / "repod.conf"
    with open(config_path, "w") as file:
        file.write(custom_config)

    commands.run_command(
        cmd=[
            "repod-file",
            "-d",
            "-c",
            f"{config_path}",
            "repo",
            "importdb",
            f"/var/lib/pacman/sync/{repo_name}.files",
            f"{base_path}/data/repo/package/{repo_name}/",
        ],
        debug=True,
        check=True,
    )
    commands.run_command(
        cmd=[
            "repod-file",
            "-d",
            "-c",
            f"{config_path}",
            "repo",
            "writedb",
            f"{base_path}/data/repo/package/{repo_name}/",
        ],
        debug=True,
        check=True,
    )


def list_database(repo_name: str, base_path: Path, architecture: str) -> None:
    """List contents (packages) of a repository sync database and files tracked in a files database of a repository.

    First all package names of the repository are printed, afterwards all files.

    Parameters
    ----------
    repo_name: str
        Name of the repository (identifying a local repository sync database)
    base_path: Path
        The base directory below which repod specific data is stored
    architecture: str
        The architecture of the repository
    """
    syncdb_path = Path(f"{base_path}/data/repo/package/{repo_name}/{architecture}/")
    with TemporaryDirectory(prefix="pacman_", dir=base_path) as dbpath:
        (Path(dbpath) / "sync").symlink_to(syncdb_path)
        cache_path = base_path / "cache"
        cache_path.mkdir(parents=True)
        pacman_conf_path = cache_path / "pacman.conf"
        pacman_conf_contents = f"""[options]
        HoldPkg = pacman glibc
        Architecture = auto
        SigLevel = Required DatabaseOptional
        LocalFileSigLevel = Optional
        [{repo_name}]
        Include = /etc/pacman.d/mirrorlist
        """

        with open(pacman_conf_path, "w") as file:
            print(pacman_conf_contents, file=file)

        commands.run_command(
            cmd=[
                "pacman",
                "--config",
                str(pacman_conf_path),
                "--cache",
                str(cache_path),
                "--logfile",
                f"{cache_path}/pacman.log",
                "--dbpath",
                f"{dbpath}",
                "-Sl",
                f"{repo_name}",
            ],
            debug=True,
            check=True,
        )
        commands.run_command(
            cmd=[
                "pacman",
                "--config",
                str(pacman_conf_path),
                "--cache",
                str(cache_path),
                "--logfile",
                f"{cache_path}/pacman.log",
                "--dbpath",
                f"{dbpath}",
                "-Fl",
            ],
            debug=True,
            check=True,
        )


@mark.integration
@mark.skipif(
    not Path("/var/lib/pacman/sync/core.files").exists(),
    reason="/var/lib/pacman/sync/core.files does not exist",
)
def test_transform_core_databases(tmp_path: Path) -> None:
    """Integration tests for transforming the packages of a repository named core."""
    name = "core"
    transform_databases(repo_name=name, base_path=tmp_path)
    list_database(repo_name=name, base_path=tmp_path, architecture="x86_64")


@mark.integration
@mark.skipif(
    not Path("/var/lib/pacman/sync/extra.files").exists(),
    reason="/var/lib/pacman/sync/extra.files does not exist",
)
def test_transform_extra_databases(tmp_path: Path) -> None:
    """Integration tests for transforming the packages of a repository named extra."""
    name = "extra"
    transform_databases(repo_name=name, base_path=tmp_path)
    list_database(repo_name=name, base_path=tmp_path, architecture="x86_64")


@mark.integration
@mark.skipif(
    not Path("/var/lib/pacman/sync/community.files").exists(),
    reason="/var/lib/pacman/sync/community.files does not exist",
)
def test_transform_community_databases(tmp_path: Path) -> None:
    """Integration tests for transforming the packages of a repository named community."""
    name = "community"
    transform_databases(repo_name="community", base_path=tmp_path)
    list_database(repo_name=name, base_path=tmp_path, architecture="x86_64")


@mark.integration
@mark.skipif(
    not Path("/var/lib/pacman/sync/multilib.files").exists(),
    reason="/var/lib/pacman/sync/multilib.files does not exist",
)
def test_transform_multilib_databases(tmp_path: Path) -> None:
    """Integration tests for transforming the packages of a repository named multilib."""
    name = "multilib"
    transform_databases(repo_name=name, base_path=tmp_path)
    list_database(repo_name=name, base_path=tmp_path, architecture="x86_64")


@mark.integration
@mark.skipif(
    not Path("/var/cache/pacman/pkg/").exists(),
    reason="Package cache in /var/cache/pacman/pkg/ does not exist",
)
def test_import_into_default_repo(tmp_path: Path) -> None:
    """Integration tests for importing a set of packages into a repod managed repository."""
    packages = sorted(
        [
            str(path)
            for path in list(Path("/var/cache/pacman/pkg/").iterdir())
            if isinstance(fullmatch(rf"^.*\.pkg\.tar({tar_compression_types_for_filename_regex()})$", str(path)), Match)
        ]
    )
    if len(packages) > 5:
        packages = sample(packages, 5)

    custom_config = f"""
    archiving = {{ packages = "{tmp_path}/archive/package/", sources = "{tmp_path}/archive/sources/" }}

    [[repositories]]
    architecture = "x86_64"
    build_requirements_exist = false
    name = "{tmp_path}/data/repo/package/default/"
    debug = "{tmp_path}/data/repo/package/default-debug/"
    staging = "{tmp_path}/data/repo/package/default-staging/"
    staging_debug = "{tmp_path}/data/repo/package/default-staging-debug/"
    testing = "{tmp_path}/data/repo/package/default-testing/"
    testing_debug = "{tmp_path}/data/repo/package/default-testing-debug/"
    package_pool = "{tmp_path}/data/pool/package/default/"
    source_pool = "{tmp_path}/data/pool/source/default/"

    [repositories.management_repo]
    directory = "{tmp_path}/management/default/"
    """

    config_path = tmp_path / "repod.conf"
    with open(config_path, "w") as file:
        file.write(custom_config)

    commands.run_command(
        cmd=[
            "repod-file",
            "-d",
            "-c",
            f"{config_path}",
            "repo",
            "importpkg",
            "-s",
        ]
        + packages
        + [f"{tmp_path}/data/repo/package/default/"],
        debug=True,
        check=True,
    )
    list_database(repo_name="default", base_path=tmp_path, architecture="x86_64")


@mark.integration
def test_write_empty_sync_db(tmp_path: Path) -> None:
    """Integration tests for writing an empty repository sync database."""
    custom_config = f"""
    [[repositories]]

    architecture = "x86_64"
    name = "{tmp_path}/data/repo/package/default/"
    debug = "{tmp_path}/data/repo/package/default-debug/"
    staging = "{tmp_path}/data/repo/package/default-staging/"
    staging_debug = "{tmp_path}/data/repo/package/default-staging-debug/"
    testing = "{tmp_path}/data/repo/package/default-testing/"
    testing_debug = "{tmp_path}/data/repo/package/default-testing-debug/"
    package_pool = "{tmp_path}/data/pool/package/default/"
    source_pool = "{tmp_path}/data/pool/source/default/"

    [repositories.management_repo]
    directory = "{tmp_path}/management/default/"
    """

    config_path = tmp_path / "repod.conf"
    with open(config_path, "w") as file:
        file.write(custom_config)

    commands.run_command(
        cmd=[
            "repod-file",
            "-d",
            "-c",
            f"{config_path}",
            "repo",
            "writedb",
            f"{tmp_path}/data/repo/package/default/",
        ],
        debug=True,
        check=True,
    )
    list_database(repo_name="default", base_path=tmp_path, architecture="x86_64")
