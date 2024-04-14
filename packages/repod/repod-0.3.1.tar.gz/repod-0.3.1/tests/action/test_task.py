"""Tests for repod.action.task."""

from contextlib import nullcontext as does_not_raise
from copy import deepcopy
from logging import DEBUG
from pathlib import Path
from typing import ContextManager
from unittest.mock import Mock, patch

from orjson import JSONEncodeError
from pydantic import ValidationError
from pytest import LogCaptureFixture, mark, raises

from repod.action import task
from repod.action.check import PacmanKeyPackagesSignatureVerificationCheck
from repod.common.enums import (
    ActionStateEnum,
    ArchitectureEnum,
    CompressionTypeEnum,
    FilesVersionEnum,
    PackageDescVersionEnum,
    PkgVerificationTypeEnum,
    RepoFileEnum,
    RepoTypeEnum,
)
from repod.config import PackageRepo, UserSettings
from repod.config.defaults import DEFAULT_ARCHITECTURE, DEFAULT_NAME
from repod.errors import RepoManagementFileError, TaskError
from repod.repo.management import OutputPackageBase


@mark.parametrize(
    "archive_dir_exists, files_in_archive, deps_in_archive, deps_in_input_list, expectation",
    [
        (True, True, True, False, does_not_raise()),
        (True, True, False, False, raises(TaskError)),
        (True, False, False, False, does_not_raise()),
        (False, False, False, False, does_not_raise()),
        (False, False, False, True, does_not_raise()),
        (True, False, False, True, does_not_raise()),
    ],
)
def test_read_build_requirements_from_archive_dir(
    archive_dir_exists: bool,
    files_in_archive: bool,
    deps_in_archive: bool,
    deps_in_input_list: bool,
    expectation: ContextManager[str],
    default_installed: list[str],
    outputpackagebasev1: OutputPackageBase,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.read_build_requirements_from_archive_dir."""
    caplog.set_level(DEBUG)

    pkgs_in_archive: set[str] = set()
    return_value: set[str] = set()

    if deps_in_input_list:
        pkgs_in_archive = set([dep for dep in default_installed])
        return_value = set([dep for dep in default_installed])

    archive_dir = None
    if archive_dir_exists:
        archive_dir = tmp_path / "archive"
        archive_dir.mkdir()

        if files_in_archive:
            for dep in default_installed:
                dep_dir = archive_dir / dep[0] / "-".join(dep.split("-")[0:-3])
                dep_dir.mkdir(parents=True)
                (dep_dir / f"{dep}.pkg.tar.zst").touch() if deps_in_archive else (dep_dir / f"{dep}.txt").touch()
            return_value = set([dep for dep in default_installed]) if deps_in_archive else set()

    with expectation:
        task.read_build_requirements_from_archive_dir(
            pkgbases=[outputpackagebasev1],
            archive_dir=archive_dir,
            pkgs_in_archive=pkgs_in_archive,
        )
        assert return_value == pkgs_in_archive  # nosec: B101


@mark.parametrize(
    "dep_exists, dep_in_input_list, dep_search_mismatch, from_file_raises, expectation",
    [
        (True, False, False, False, does_not_raise()),
        (True, True, False, False, does_not_raise()),
        (True, True, True, False, does_not_raise()),
        (True, False, True, False, does_not_raise()),
        (False, False, False, False, does_not_raise()),
        (True, False, False, True, raises(TaskError)),
    ],
)
def test_read_build_requirements_from_management_repo_dirs(
    dep_exists: bool,
    dep_in_input_list: bool,
    dep_search_mismatch: bool,
    from_file_raises: bool,
    expectation: ContextManager[str],
    outputpackagebasev1: OutputPackageBase,
    outputpackagebasev1_json_files_in_dir: Path,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.read_build_requirements_from_management_repo_dirs."""
    caplog.set_level(DEBUG)

    pkgs_in_repo: set[str] = set()
    return_value: set[str] = set()

    management_dirs = [tmp_path / "empty_management" / "foo"]
    for dir_ in management_dirs:
        dir_.mkdir(parents=True)

    if dep_search_mismatch:
        installed = [
            f"{pkg.name}-2000-1-{pkg.arch}" for pkg in outputpackagebasev1.packages  # type: ignore[attr-defined]
        ]
    else:
        installed = [
            f"{pkg.name}-{outputpackagebasev1.version}-{pkg.arch}"  # type: ignore[attr-defined]
            for pkg in outputpackagebasev1.packages  # type: ignore[attr-defined]
        ]
        if dep_exists:
            return_value = set([dep for dep in installed])

    if dep_in_input_list:
        pkgs_in_repo.add(installed[0])
        if dep_search_mismatch:
            return_value.add(installed[0])

    if dep_exists:
        del outputpackagebasev1.packages[0]  # type: ignore[attr-defined]
        outputpackagebasev1.packages[0].name = "foo2000"  # type: ignore[attr-defined]
        outputpackagebasev1.buildinfo.installed = installed  # type: ignore[attr-defined]
        management_dirs = [outputpackagebasev1_json_files_in_dir]

    with expectation:
        if from_file_raises:
            with patch("repod.action.task.OutputPackageBase.from_file", side_effect=RepoManagementFileError):
                task.read_build_requirements_from_management_repo_dirs(
                    pkgbases=[outputpackagebasev1],
                    management_directories=management_dirs,
                    pkgs_in_repo=pkgs_in_repo,
                )
        else:
            task.read_build_requirements_from_management_repo_dirs(
                pkgbases=[outputpackagebasev1],
                management_directories=management_dirs,
                pkgs_in_repo=pkgs_in_repo,
            )
            assert return_value == pkgs_in_repo  # nosec: B101


@mark.parametrize(
    "add_above, above_exists, add_below, below_exists",
    [
        (True, True, True, True),
        (True, True, False, False),
        (True, True, True, False),
        (True, True, False, True),
        (True, False, True, True),
        (False, True, True, True),
        (False, False, True, True),
        (False, False, False, False),
    ],
)
def test_read_pkgbases_from_stability_layers(
    add_above: bool,
    above_exists: bool,
    add_below: bool,
    below_exists: bool,
    outputpackagebasev1_json_files_in_dir: Path,
    tmp_path: Path,
) -> None:
    """Tests for repod.action.task.read_pkgbases_from_stability_layers."""
    current_pkgbases: list[OutputPackageBase] = []
    current_filenames: list[str] = []
    current_package_names: list[str] = []
    pkgbases_above: list[OutputPackageBase] = []
    pkgbases_below: list[OutputPackageBase] = []

    above = [outputpackagebasev1_json_files_in_dir if above_exists else tmp_path / "foo"] if add_above else []
    below = [outputpackagebasev1_json_files_in_dir if below_exists else tmp_path / "foo"] if add_below else []

    task.read_pkgbases_from_stability_layers(
        directory=outputpackagebasev1_json_files_in_dir,
        pkgbase_names=["foo"],
        stability_layer_dirs=(above, below),
        current_pkgbases=current_pkgbases,
        current_filenames=current_filenames,
        current_package_names=current_package_names,
        pkgbases_above=pkgbases_above,
        pkgbases_below=pkgbases_below,
    )


@mark.parametrize(
    "path, expectation",
    [
        (Path("/foo.tmp"), does_not_raise()),
        (Path("/foo"), raises(ValidationError)),
        (Path("foo"), raises(ValidationError)),
    ],
)
def test_sourcedestination_validate_source(path: Path, expectation: ContextManager[str]) -> None:
    """Tests for repod.action.task.SourceDestination.validate_source."""
    with expectation:
        task.SourceDestination(source=path, destination=Path("/foo"), destination_backup=Path("/foo.bkp"))


@mark.parametrize(
    "path, expectation",
    [
        (Path("/foo"), does_not_raise()),
        (Path("/foo.tmp"), raises(ValidationError)),
        (Path("/foo.bkp"), raises(ValidationError)),
        (Path("foo"), raises(ValidationError)),
    ],
)
def test_sourcedestination_validate_destination(path: Path, expectation: ContextManager[str]) -> None:
    """Tests for repod.action.task.SourceDestination.validate_destination."""
    with expectation:
        task.SourceDestination(source=Path("/foo.tmp"), destination=path, destination_backup=Path("/foo.bkp"))


@mark.parametrize(
    "path, expectation",
    [
        (Path("/foo.bkp"), does_not_raise()),
        (Path("/foo.tmp"), raises(ValidationError)),
        (Path("foo"), raises(ValidationError)),
    ],
)
def test_sourcedestination_validate_destination_backup(path: Path, expectation: ContextManager[str]) -> None:
    """Tests for repod.action.task.SourceDestination.validate_destination_backup."""
    with expectation:
        task.SourceDestination(source=Path("/foo.tmp"), destination=Path("/foo"), destination_backup=path)


@mark.parametrize(
    "package_verification, with_signature, add_dependencies",
    [
        (None, True, False),
        (None, False, False),
        (None, True, True),
        (None, False, True),
        (PkgVerificationTypeEnum.PACMANKEY, False, False),
        (PkgVerificationTypeEnum.PACMANKEY, True, False),
        (PkgVerificationTypeEnum.PACMANKEY, False, True),
        (PkgVerificationTypeEnum.PACMANKEY, True, True),
    ],
)
def test_createoutputpackagebasestask(
    package_verification: PkgVerificationTypeEnum | None,
    with_signature: bool,
    add_dependencies: bool,
    default_package_file: tuple[Path, ...],
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.CreateOutputPackageBasesTask."""
    caplog.set_level(DEBUG)

    dependencies = [Mock()]

    task_ = task.CreateOutputPackageBasesTask(
        architecture=ArchitectureEnum.ANY,
        package_paths=[default_package_file[0]],
        with_signature=with_signature,
        package_verification=package_verification,
        debug_repo=False,
        pkgbase_urls={},
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )

    if package_verification == PkgVerificationTypeEnum.PACMANKEY and with_signature:
        found_check = False
        for check in task_.pre_checks:
            if isinstance(check, PacmanKeyPackagesSignatureVerificationCheck):
                found_check = True

        assert found_check  # nosec: B101

    if add_dependencies:
        assert task_.dependencies == dependencies  # nosec: B101


@mark.parametrize(
    "with_signature, package_from_file_raises, outputpackagebase_from_package_raises, return_value",
    [
        (True, False, False, ActionStateEnum.SUCCESS_TASK),
        (True, True, False, ActionStateEnum.FAILED_TASK),
        (True, False, True, ActionStateEnum.FAILED_TASK),
        (False, False, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, False, ActionStateEnum.FAILED_TASK),
        (False, False, True, ActionStateEnum.FAILED_TASK),
    ],
)
def test_createoutputpackagebasestask_do(
    with_signature: bool,
    package_from_file_raises: bool,
    outputpackagebase_from_package_raises: bool,
    return_value: ActionStateEnum,
    default_package_file: tuple[Path, ...],
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.CreateOutputPackageBasesTask.do."""
    caplog.set_level(DEBUG)

    task_ = task.CreateOutputPackageBasesTask(
        architecture=ArchitectureEnum.ANY,
        package_paths=[default_package_file[0]],
        with_signature=with_signature,
        debug_repo=False,
        pkgbase_urls={},
        package_verification=None,
    )

    if package_from_file_raises:
        with patch("repod.action.task.Package.from_file", side_effect=RepoManagementFileError):
            assert task_.do() == return_value  # nosec: B101
    elif outputpackagebase_from_package_raises:
        with patch("repod.action.task.OutputPackageBase.from_package", side_effect=ValueError):
            assert task_.do() == return_value  # nosec: B101
    else:
        assert task_.do() == return_value  # nosec: B101

    if return_value == ActionStateEnum.SUCCESS_TASK:
        assert isinstance(task_.pkgbases[0], OutputPackageBase)  # nosec: B101


def test_createoutputpackagebasestask_undo(
    default_package_file: tuple[Path, ...],
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.CreateOutputPackageBasesTask.undo."""
    caplog.set_level(DEBUG)

    task_ = task.CreateOutputPackageBasesTask(
        architecture=ArchitectureEnum.ANY,
        package_paths=[default_package_file[0]],
        with_signature=True,
        debug_repo=False,
        pkgbase_urls={},
        package_verification=None,
    )

    task_.do()
    assert isinstance(task_.pkgbases[0], OutputPackageBase)  # nosec: B101

    assert task_.undo() == ActionStateEnum.NOT_STARTED  # nosec: B101
    assert task_.pkgbases == []  # nosec: B101


@mark.parametrize(
    "add_pkgbases, add_dependencies, expectation",
    [
        (True, False, does_not_raise()),
        (False, True, does_not_raise()),
        (False, False, raises(RuntimeError)),
    ],
)
def test_printoutputpackagebasestask(
    add_pkgbases: bool,
    add_dependencies: bool,
    expectation: ContextManager[str],
    outputpackagebasev1: OutputPackageBase,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.PrintOutputPackageBasesTask."""
    caplog.set_level(DEBUG)

    dependencies = [
        Mock(),
        Mock(spec=task.CreateOutputPackageBasesTask),
        Mock(),
    ]

    with expectation:
        task_ = task.PrintOutputPackageBasesTask(
            dumps_option=0,
            pkgbases=[outputpackagebasev1] if add_pkgbases else None,
            dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
        )

    if expectation is does_not_raise():  # type: ignore[comparison-overlap]
        assert task_.dumps_option == 0  # nosec: B101

        if add_pkgbases and not add_dependencies:
            assert task_.pkgbases == [outputpackagebasev1]  # nosec: B101
            assert not task_.input_from_dependency  # nosec: B101
            assert not task_.dependencies  # nosec: B101

        if add_dependencies:
            assert task_.dependencies == dependencies  # nosec: B101
            assert task_.pkgbases == []  # nosec: B101
            assert task_.input_from_dependency  # nosec: B101


@mark.parametrize(
    "add_pkgbases, add_dependencies, dependency_state, dumps_raises, return_value",
    [
        (True, False, ActionStateEnum.SUCCESS, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, ActionStateEnum.SUCCESS, False, ActionStateEnum.SUCCESS_TASK),
        (True, True, ActionStateEnum.SUCCESS, False, ActionStateEnum.SUCCESS_TASK),
        (True, False, ActionStateEnum.SUCCESS, True, ActionStateEnum.FAILED_TASK),
        (False, True, ActionStateEnum.SUCCESS, True, ActionStateEnum.FAILED_TASK),
        (True, True, ActionStateEnum.SUCCESS, True, ActionStateEnum.FAILED_TASK),
        (True, True, ActionStateEnum.FAILED_TASK, False, ActionStateEnum.FAILED_DEPENDENCY),
    ],
)
def test_printoutputpackagebasestask_do(
    add_pkgbases: bool,
    add_dependencies: bool,
    dependency_state: ActionStateEnum,
    dumps_raises: bool,
    return_value: ActionStateEnum,
    outputpackagebasev1: OutputPackageBase,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.PrintOutputPackageBasesTask.do."""
    caplog.set_level(DEBUG)

    dependencies = [
        Mock(),
        Mock(
            spec=task.CreateOutputPackageBasesTask,
            state=dependency_state,
            pkgbases=[outputpackagebasev1],
        ),
        Mock(),
    ]

    task_ = task.PrintOutputPackageBasesTask(
        dumps_option=0,
        pkgbases=[outputpackagebasev1] if add_pkgbases else None,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )
    if dumps_raises:
        with patch("repod.action.task.dumps", side_effect=JSONEncodeError):
            assert task_.do() == return_value  # nosec: B101
    else:
        assert task_.do() == return_value  # nosec: B101


@mark.parametrize(
    "add_pkgbases, add_dependencies, do",
    [
        (True, True, True),
        (True, False, True),
        (False, True, True),
        (True, True, False),
        (True, False, False),
        (False, True, False),
    ],
)
def test_printoutputpackagebasestask_undo(
    add_pkgbases: bool,
    add_dependencies: bool,
    do: bool,
    outputpackagebasev1: OutputPackageBase,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.PrintOutputPackageBasesTask.undo."""
    caplog.set_level(DEBUG)

    dependencies = [
        Mock(
            spec=task.CreateOutputPackageBasesTask,
            state=ActionStateEnum.SUCCESS,
            pkgbases=[outputpackagebasev1],
            undo=Mock(return_value=ActionStateEnum.NOT_STARTED),
        ),
    ]

    task_ = task.PrintOutputPackageBasesTask(
        dumps_option=0,
        pkgbases=[outputpackagebasev1] if add_pkgbases else None,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )

    if do:
        assert task_.do() == ActionStateEnum.SUCCESS_TASK  # nosec: B101

    assert task_.undo() == ActionStateEnum.NOT_STARTED  # nosec: B101

    if add_pkgbases and not add_dependencies:
        assert task_.pkgbases == [outputpackagebasev1]  # nosec: B101

    if add_dependencies:
        assert task_.pkgbases == []  # nosec: B101


@mark.parametrize(
    "add_pkgbases, add_dependencies, expectation",
    [
        (True, True, does_not_raise()),
        (True, False, does_not_raise()),
        (False, True, does_not_raise()),
        (False, False, raises(RuntimeError)),
    ],
)
def test_writeoutputpackagebasestotmpfileindirtask(
    add_pkgbases: bool,
    add_dependencies: bool,
    expectation: ContextManager[str],
    outputpackagebasev1: OutputPackageBase,
    caplog: LogCaptureFixture,
    tmp_path: Path,
) -> None:
    """Tests for repod.action.task.WriteOutputPackageBasesToTmpFileInDirTask."""
    caplog.set_level(DEBUG)

    dependencies = [
        Mock(),
        Mock(spec=task.CreateOutputPackageBasesTask, pkgbases=outputpackagebasev1, state=ActionStateEnum.SUCCESS),
        Mock(),
    ]

    with expectation:
        task_ = task.WriteOutputPackageBasesToTmpFileInDirTask(
            directory=tmp_path,
            pkgbases=[outputpackagebasev1] if add_pkgbases else None,
            dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
        )
        assert task_.directory == tmp_path  # nosec: B101
        assert not task_.filenames  # nosec: B101

        if add_dependencies:
            assert task_.dependencies == dependencies  # nosec: B101
            assert task_.pkgbases == []  # nosec: B101
        else:
            assert task_.pkgbases == [outputpackagebasev1]  # nosec: B101


@mark.parametrize(
    "add_pkgbases, add_dependencies, dependency_state, dumps_raises, return_value",
    [
        (True, False, ActionStateEnum.SUCCESS, False, ActionStateEnum.SUCCESS_TASK),
        (True, False, ActionStateEnum.SUCCESS, True, ActionStateEnum.FAILED_TASK),
        (False, True, ActionStateEnum.SUCCESS, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, ActionStateEnum.SUCCESS, True, ActionStateEnum.FAILED_TASK),
        (True, False, ActionStateEnum.FAILED_TASK, False, ActionStateEnum.SUCCESS_TASK),
        (True, False, ActionStateEnum.FAILED_TASK, True, ActionStateEnum.FAILED_TASK),
        (False, True, ActionStateEnum.FAILED_TASK, False, ActionStateEnum.FAILED_DEPENDENCY),
        (False, True, ActionStateEnum.FAILED_TASK, True, ActionStateEnum.FAILED_DEPENDENCY),
    ],
)
def test_writeoutputpackagebasestotmpfileindirtask_do(
    add_pkgbases: bool,
    add_dependencies: bool,
    dependency_state: ActionStateEnum,
    dumps_raises: bool,
    return_value: ActionStateEnum,
    outputpackagebasev1: OutputPackageBase,
    caplog: LogCaptureFixture,
    tmp_path: Path,
) -> None:
    """Tests for repod.action.task.WriteOutputPackageBasesToTmpFileInDirTask.do."""
    caplog.set_level(DEBUG)

    dependencies = [
        Mock(),
        Mock(
            spec=task.CreateOutputPackageBasesTask,
            pkgbases=[outputpackagebasev1],
            state=dependency_state,
        ),
        Mock(),
    ]
    task_ = task.WriteOutputPackageBasesToTmpFileInDirTask(
        directory=tmp_path,
        pkgbases=[outputpackagebasev1] if add_pkgbases else None,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )
    if dumps_raises:
        with patch("repod.action.task.dumps", side_effect=JSONEncodeError):
            assert task_.do() == return_value  # nosec: B101
    else:
        assert task_.do() == return_value  # nosec: B101
        if return_value == ActionStateEnum.SUCCESS_TASK:
            assert task_.filenames[0] == (  # nosec: B101
                tmp_path / Path(f"{outputpackagebasev1.base}.json.tmp")  # type: ignore[attr-defined]
            )
            assert (tmp_path / task_.filenames[0]).exists()  # nosec: B101
        else:
            assert task_.filenames == []  # nosec: B101


@mark.parametrize(
    "add_dependencies, do, remove_file, return_value",
    [
        (False, True, False, ActionStateEnum.NOT_STARTED),
        (False, False, False, ActionStateEnum.NOT_STARTED),
        (False, True, True, ActionStateEnum.NOT_STARTED),
        (True, True, False, ActionStateEnum.NOT_STARTED),
        (True, False, False, ActionStateEnum.NOT_STARTED),
        (True, True, True, ActionStateEnum.NOT_STARTED),
    ],
)
def test_writeoutputpackagebasestotmpfileindirtask_undo(
    add_dependencies: bool,
    do: bool,
    remove_file: bool,
    return_value: ActionStateEnum,
    outputpackagebasev1: OutputPackageBase,
    caplog: LogCaptureFixture,
    tmp_path: Path,
) -> None:
    """Tests for repod.action.task.WriteOutputPackageBasesToTmpFileInDirTask.undo."""
    caplog.set_level(DEBUG)

    dependencies = [
        Mock(
            spec=task.CreateOutputPackageBasesTask,
            pkgbases=[outputpackagebasev1],
            state=ActionStateEnum.SUCCESS,
            undo=Mock(return_value=ActionStateEnum.NOT_STARTED),
        ),
    ]
    task_ = task.WriteOutputPackageBasesToTmpFileInDirTask(
        directory=tmp_path,
        pkgbases=[outputpackagebasev1],
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )

    if do:
        task_.do()
        if remove_file:
            for filename in task_.filenames:
                (tmp_path / filename).unlink()

    assert task_.undo() == return_value  # nosec: B101

    if add_dependencies:
        assert task_.pkgbases == []  # nosec: B101


@mark.parametrize(
    "add_paths, correct_path_length, add_dependencies, expectation",
    [
        (True, True, False, does_not_raise()),
        (True, False, False, raises(RuntimeError)),
        (False, False, True, does_not_raise()),
        (True, False, True, does_not_raise()),
        (True, True, True, does_not_raise()),
        (False, False, False, raises(RuntimeError)),
    ],
)
def test_movetmpfilestask(
    add_paths: bool,
    correct_path_length: bool,
    add_dependencies: bool,
    expectation: ContextManager[str],
    caplog: LogCaptureFixture,
    tmp_path: Path,
) -> None:
    """Tests for repod.action.task.MoveTmpFilesTask."""
    caplog.set_level(DEBUG)

    source = tmp_path / "foo.tmp"
    destination = tmp_path / "foo"
    destination_backup = tmp_path / "foo.bkp"
    paths = [[source, destination]] if correct_path_length else [[source]]
    source_destination = [
        task.SourceDestination(
            source=source,
            destination=destination,
            destination_backup=destination_backup,
            backup_done=False,
        )
    ]

    dependencies = [
        Mock(),
        Mock(
            spec=task.WriteOutputPackageBasesToTmpFileInDirTask,
        ),
        Mock(),
    ]

    with expectation:
        task_ = task.MoveTmpFilesTask(
            paths=paths if add_paths else None,
            dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
        )

    if add_paths and correct_path_length and not add_dependencies:
        assert task_.paths == source_destination  # nosec: B101
    if add_dependencies:
        assert task_.paths == []  # nosec: B101


@mark.parametrize(
    (
        "add_paths, add_dependencies, pkgbases_dep, syncdb_dep, dependency_state, dependency_absolute, "
        "destination_exists, copy2_raises, rename_raises, return_value"
    ),
    [
        (True, False, False, False, None, True, True, False, False, ActionStateEnum.SUCCESS_TASK),
        (True, False, False, False, None, True, True, True, False, ActionStateEnum.FAILED_TASK),
        (True, False, False, False, None, True, True, False, True, ActionStateEnum.FAILED_TASK),
        (True, False, False, False, None, True, False, False, False, ActionStateEnum.SUCCESS_TASK),
        (True, False, False, False, None, True, False, True, False, ActionStateEnum.SUCCESS_TASK),
        (True, False, False, False, None, True, False, False, True, ActionStateEnum.FAILED_TASK),
        (False, True, False, True, ActionStateEnum.SUCCESS, True, True, False, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, False, True, ActionStateEnum.SUCCESS, True, True, True, False, ActionStateEnum.FAILED_TASK),
        (False, True, False, True, ActionStateEnum.SUCCESS, True, True, False, True, ActionStateEnum.FAILED_TASK),
        (False, True, False, True, ActionStateEnum.SUCCESS, True, False, False, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, False, True, ActionStateEnum.SUCCESS, False, False, False, False, ActionStateEnum.FAILED_TASK),
        (False, True, False, True, ActionStateEnum.SUCCESS, True, False, True, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, False, True, ActionStateEnum.SUCCESS, True, False, False, True, ActionStateEnum.FAILED_TASK),
        (False, True, True, False, ActionStateEnum.SUCCESS, True, True, False, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, True, False, ActionStateEnum.SUCCESS, True, True, True, False, ActionStateEnum.FAILED_TASK),
        (False, True, True, False, ActionStateEnum.SUCCESS, True, True, False, True, ActionStateEnum.FAILED_TASK),
        (False, True, True, False, ActionStateEnum.SUCCESS, True, False, False, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, True, False, ActionStateEnum.SUCCESS, False, False, False, False, ActionStateEnum.FAILED_TASK),
        (False, True, True, False, ActionStateEnum.SUCCESS, True, False, True, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, True, False, ActionStateEnum.SUCCESS, True, False, False, True, ActionStateEnum.FAILED_TASK),
        (
            False,
            True,
            True,
            False,
            ActionStateEnum.FAILED_TASK,
            True,
            False,
            False,
            False,
            ActionStateEnum.FAILED_DEPENDENCY,
        ),
        (
            False,
            True,
            True,
            False,
            ActionStateEnum.FAILED_TASK,
            True,
            False,
            False,
            False,
            ActionStateEnum.FAILED_DEPENDENCY,
        ),
        (
            False,
            True,
            False,
            True,
            ActionStateEnum.FAILED_TASK,
            True,
            False,
            False,
            False,
            ActionStateEnum.FAILED_DEPENDENCY,
        ),
    ],
)
def test_movetmpfilestask_do(
    add_paths: bool,
    add_dependencies: bool,
    pkgbases_dep: bool,
    syncdb_dep: bool,
    dependency_state: ActionStateEnum | None,
    dependency_absolute: bool,
    destination_exists: bool,
    copy2_raises: bool,
    rename_raises: bool,
    return_value: ActionStateEnum,
    caplog: LogCaptureFixture,
    tmp_path: Path,
) -> None:
    """Tests for repod.action.task.MoveTmpFilesTask.do."""
    caplog.set_level(DEBUG)

    default_db = tmp_path / "default.db.tar.gz.tmp"
    default_db.touch()
    default_db_symlink = tmp_path / "default.db.tmp"
    default_db_symlink.touch()
    files_db = tmp_path / "default.files.tar.gz.tmp"
    files_db.touch()
    files_db_symlink = tmp_path / "default.files.tmp"
    files_db_symlink.touch()
    filename_source = Path("foo.tmp")
    source = tmp_path / filename_source
    source.touch()
    filename_destination = Path("foo")
    destination = tmp_path / filename_destination
    if destination_exists:
        destination.touch()
        Path(str(default_db).replace(".tmp", "")).touch()
        Path(str(files_db).replace(".tmp", "")).touch()

    paths = [[source, destination]]

    dependencies = [
        Mock(
            state=ActionStateEnum.SUCCESS,
        ),
    ]
    if pkgbases_dep:
        dependencies.append(
            Mock(
                spec=task.WriteOutputPackageBasesToTmpFileInDirTask,
                state=dependency_state,
                filenames=[source if dependency_absolute else filename_source],
            )
        )
    if syncdb_dep:
        dependencies.append(
            Mock(
                spec=task.WriteSyncDbsToTmpFilesInDirTask,
                state=dependency_state,
                default_syncdb_path=default_db if dependency_absolute else default_db.name,
                default_syncdb_symlink_path=default_db_symlink if dependency_absolute else default_db_symlink.name,
                files_syncdb_path=files_db if dependency_absolute else files_db.name,
                files_syncdb_symlink_path=files_db_symlink if dependency_absolute else files_db_symlink.name,
            )
        )
    dependencies.append(
        Mock(
            state=ActionStateEnum.SUCCESS,
        )
    )

    task_ = task.MoveTmpFilesTask(
        paths=paths if add_paths else None,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )

    match (destination_exists, copy2_raises, rename_raises):
        case (True, False, False):
            assert task_.do() == return_value  # nosec: B101
            assert not task_.paths[0].source.exists()  # nosec: B101
            assert task_.paths[0].destination.exists()  # nosec: B101
            assert task_.paths[0].destination_backup.exists()  # nosec: B101
            assert task_.paths[0].backup_done  # nosec: B101
        case (True, True, False):
            with patch("repod.action.task.copy2", side_effect=Exception("ERROR")):
                assert task_.do() == return_value  # nosec: B101
            assert task_.paths[0].source.exists()  # nosec: B101
            assert task_.paths[0].destination.exists()  # nosec: B101
            assert not task_.paths[0].destination_backup.exists()  # nosec: B101
            assert not task_.paths[0].backup_done  # nosec: B101
        case (True, False, True):
            with patch("repod.action.task.Path.rename", side_effect=Exception("ERROR")):
                assert task_.do() == return_value  # nosec: B101
            assert task_.paths[0].source.exists()  # nosec: B101
            assert task_.paths[0].destination.exists()  # nosec: B101
            assert task_.paths[0].destination_backup.exists()  # nosec: B101
            assert task_.paths[0].backup_done  # nosec: B101
        case (False, False, False):
            assert task_.do() == return_value  # nosec: B101
            if task_.state == ActionStateEnum.SUCCESS:
                assert not task_.paths[0].source.exists()  # nosec: B101
                assert task_.paths[0].destination.exists()  # nosec: B101
                assert not task_.paths[0].destination_backup.exists()  # nosec: B101
                assert not task_.paths[0].backup_done  # nosec: B101
        case (False, True, False):
            with patch("repod.action.task.copy2", side_effect=Exception("ERROR")):
                assert task_.do() == return_value  # nosec: B101
            assert not task_.paths[0].source.exists()  # nosec: B101
            assert task_.paths[0].destination.exists()  # nosec: B101
            assert not task_.paths[0].destination_backup.exists()  # nosec: B101
            assert not task_.paths[0].backup_done  # nosec: B101
        case (False, False, True):
            with patch("repod.action.task.Path.rename", side_effect=Exception("ERROR")):
                assert task_.do() == return_value  # nosec: B101
            if not (not dependency_absolute and add_dependencies and pkgbases_dep):
                assert task_.paths[0].source.exists()  # nosec: B101
                assert not task_.paths[0].destination.exists()  # nosec: B101
                assert not task_.paths[0].destination_backup.exists()  # nosec: B101
                assert not task_.paths[0].backup_done  # nosec: B101


@mark.parametrize(
    "do, destination_exists, copy2_raises, rename_raises, remove_backup, return_value",
    [
        (False, False, False, False, False, ActionStateEnum.NOT_STARTED),
        (True, True, False, False, False, ActionStateEnum.NOT_STARTED),
        (True, False, False, False, False, ActionStateEnum.NOT_STARTED),
        (True, False, True, False, False, ActionStateEnum.NOT_STARTED),
        (True, False, False, True, False, ActionStateEnum.NOT_STARTED),
        (True, True, False, True, False, ActionStateEnum.NOT_STARTED),
        (True, True, False, False, True, ActionStateEnum.FAILED_UNDO_TASK),
    ],
)
def test_movetmpfilestask_undo(
    do: bool,
    destination_exists: bool,
    copy2_raises: bool,
    rename_raises: bool,
    remove_backup: bool,
    return_value: ActionStateEnum,
    caplog: LogCaptureFixture,
    tmp_path: Path,
) -> None:
    """Tests for repod.action.task.MoveTmpFilesTask.undo."""
    caplog.set_level(DEBUG)

    source = tmp_path / "foo.tmp"
    source.touch()
    destination = tmp_path / "foo"
    if destination_exists:
        destination.touch()

    task_ = task.MoveTmpFilesTask(paths=[[source, destination]])

    if do:
        if copy2_raises:
            with patch("repod.action.task.copy2", side_effect=Exception("ERROR")):
                task_.do()
        elif rename_raises:
            with patch("repod.action.task.Path.rename", side_effect=Exception("ERROR")):
                task_.do()
        else:
            task_.do()

    if remove_backup:
        task_.paths[0].destination_backup.unlink()

    assert task_.undo() == return_value  # nosec: B101


@mark.parametrize(
    "file_type, add_dependencies",
    [
        (RepoFileEnum.PACKAGE, False),
        (RepoFileEnum.PACKAGE_SIGNATURE, False),
        (RepoFileEnum.PACKAGE, True),
        (RepoFileEnum.PACKAGE_SIGNATURE, True),
    ],
)
def test_filestorepodirtask(
    file_type: RepoFileEnum,
    add_dependencies: bool,
    default_package_file: tuple[Path, ...],
    usersettings: UserSettings,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.FilesToRepoDirTask."""
    caplog.set_level(DEBUG)

    dependencies = [Mock()]
    file = default_package_file[0] if file_type == RepoFileEnum.PACKAGE else default_package_file[1]

    task_ = task.FilesToRepoDirTask(
        files=[file],
        file_type=file_type,
        settings=usersettings,
        name=Path(DEFAULT_NAME),
        architecture=DEFAULT_ARCHITECTURE,
        repo_type=RepoTypeEnum.STABLE,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )

    assert task_.files == [file]  # nosec: B101
    assert task_.repo_files == []  # nosec: B101

    if add_dependencies:
        assert task_.dependencies == dependencies  # nosec: B101


@mark.parametrize(
    "file_type, get_repo_path_raises, repofile_copy_from_raises, return_value",
    [
        (RepoFileEnum.PACKAGE, False, False, ActionStateEnum.SUCCESS_TASK),
        (RepoFileEnum.PACKAGE_SIGNATURE, False, False, ActionStateEnum.SUCCESS_TASK),
        (RepoFileEnum.PACKAGE, True, False, ActionStateEnum.FAILED_TASK),
        ("foo", False, False, ActionStateEnum.FAILED_TASK),
        (RepoFileEnum.PACKAGE, False, True, ActionStateEnum.FAILED_TASK),
        (RepoFileEnum.PACKAGE_SIGNATURE, True, False, ActionStateEnum.FAILED_TASK),
        ("foo", False, False, ActionStateEnum.FAILED_TASK),
        (RepoFileEnum.PACKAGE_SIGNATURE, False, True, ActionStateEnum.FAILED_TASK),
    ],
)
def test_filestorepodirtask_do(
    file_type: RepoFileEnum,
    get_repo_path_raises: bool,
    repofile_copy_from_raises: bool,
    return_value: ActionStateEnum,
    default_package_file: tuple[Path, ...],
    usersettings: UserSettings,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.FilesToRepoDirTask.do."""
    caplog.set_level(DEBUG)

    file = default_package_file[0] if file_type == RepoFileEnum.PACKAGE else default_package_file[1]

    task_ = task.FilesToRepoDirTask(
        files=[file],
        file_type=file_type,
        settings=usersettings,
        name=Path(DEFAULT_NAME),
        architecture=DEFAULT_ARCHITECTURE,
        repo_type=RepoTypeEnum.STABLE,
    )

    if get_repo_path_raises:
        with patch("repod.action.task.UserSettings.get_repo_path", side_effect=RuntimeError):
            assert task_.do() == return_value  # nosec: B101
    elif repofile_copy_from_raises:
        with patch("repod.action.task.RepoFile.copy_from", side_effect=RepoManagementFileError):
            assert task_.do() == return_value  # nosec: B101
    else:
        assert task_.do() == return_value  # nosec: B101
        if isinstance(file_type, RepoFileEnum):
            assert task_.repo_files[0].file_path.exists()  # nosec: B101
            assert task_.repo_files[0].symlink_path.exists()  # nosec: B101


@mark.parametrize(
    "file_type, do",
    [
        (RepoFileEnum.PACKAGE, True),
        (RepoFileEnum.PACKAGE, False),
        (RepoFileEnum.PACKAGE_SIGNATURE, True),
        (RepoFileEnum.PACKAGE_SIGNATURE, False),
    ],
)
def test_filestorepodirtask_undo(
    file_type: RepoFileEnum,
    do: bool,
    default_package_file: tuple[Path, ...],
    usersettings: UserSettings,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.FilesToRepoDirTask.undo."""
    caplog.set_level(DEBUG)

    files_to_check: list[Path] = []

    file = default_package_file[0] if file_type == RepoFileEnum.PACKAGE else default_package_file[1]

    task_ = task.FilesToRepoDirTask(
        files=[file],
        file_type=file_type,
        settings=usersettings,
        name=Path(DEFAULT_NAME),
        architecture=DEFAULT_ARCHITECTURE,
        repo_type=RepoTypeEnum.STABLE,
    )

    if do:
        assert task_.do() == ActionStateEnum.SUCCESS_TASK  # nosec: B101
        assert task_.repo_files[0].file_path.exists()  # nosec: B101
        files_to_check.append(task_.repo_files[0].file_path)
        assert task_.repo_files[0].symlink_path.exists()  # nosec: B101
        files_to_check.append(task_.repo_files[0].symlink_path)

    assert task_.undo() == ActionStateEnum.NOT_STARTED  # nosec: B101
    for path in files_to_check:
        assert not path.exists()  # nosec: B101


def test_addtorepotask() -> None:
    """Tests for repod.action.task.AddToRepoTask."""
    assert task.AddToRepoTask(dependencies=[])  # nosec: B101


def test_addtorepotask_do() -> None:
    """Tests for repod.action.task.AddToRepoTask.do."""
    assert task.AddToRepoTask(dependencies=[]).do() == ActionStateEnum.SUCCESS_TASK  # nosec: B101


def test_addtorepotask_undo() -> None:
    """Tests for repod.action.task.AddToRepoTask.undo."""
    task_ = task.AddToRepoTask(dependencies=[])
    assert task_.do() == ActionStateEnum.SUCCESS_TASK  # nosec: B101
    assert task_.undo() == ActionStateEnum.NOT_STARTED  # nosec: B101


@mark.parametrize(
    "add_dependencies, compression_type, desc_version, files_version",
    [
        (True, CompressionTypeEnum.NONE, PackageDescVersionEnum.DEFAULT, FilesVersionEnum.DEFAULT),
        (False, CompressionTypeEnum.NONE, PackageDescVersionEnum.DEFAULT, FilesVersionEnum.DEFAULT),
    ],
)
def test_writesyncdbstotmpfilesindirtask(
    add_dependencies: bool,
    desc_version: PackageDescVersionEnum,
    files_version: FilesVersionEnum,
    compression_type: CompressionTypeEnum,
    outputpackagebasev1_json_files_in_dir: Path,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.WriteSyncDbsToTmpFilesInDirTask."""
    caplog.set_level(DEBUG)

    dependencies = [Mock()]
    task_ = task.WriteSyncDbsToTmpFilesInDirTask(
        compression=compression_type,
        desc_version=desc_version,
        files_version=files_version,
        management_repo_dir=outputpackagebasev1_json_files_in_dir,
        package_repo_dir=tmp_path,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )

    if add_dependencies:
        assert task_.dependencies == dependencies  # nosec: B101

    assert task_.default_syncdb_path.suffix == ".tmp"  # nosec: B101
    assert task_.files_syncdb_path.suffix == ".tmp"  # nosec: B101


@mark.parametrize(
    "add_dependencies, desc_version, return_value, json_files_exist, target_is_dir",
    [
        (
            True,
            PackageDescVersionEnum.DEFAULT,
            ActionStateEnum.SUCCESS_TASK,
            True,
            False,
        ),
        (
            False,
            PackageDescVersionEnum.DEFAULT,
            ActionStateEnum.SUCCESS_TASK,
            True,
            False,
        ),
        (
            True,
            "foo",
            ActionStateEnum.FAILED_TASK,
            True,
            False,
        ),
        (
            False,
            "foo",
            ActionStateEnum.FAILED_TASK,
            True,
            False,
        ),
        (
            True,
            PackageDescVersionEnum.DEFAULT,
            ActionStateEnum.SUCCESS_TASK,
            False,
            False,
        ),
        (
            False,
            PackageDescVersionEnum.DEFAULT,
            ActionStateEnum.SUCCESS_TASK,
            False,
            False,
        ),
        (
            True,
            PackageDescVersionEnum.DEFAULT,
            ActionStateEnum.FAILED_TASK,
            False,
            True,
        ),
        (
            False,
            PackageDescVersionEnum.DEFAULT,
            ActionStateEnum.FAILED_TASK,
            False,
            True,
        ),
    ],
)
def test_writesyncdbstotmpfilesindirtask_do(
    add_dependencies: bool,
    desc_version: PackageDescVersionEnum,
    return_value: ActionStateEnum,
    json_files_exist: bool,
    target_is_dir: bool,
    outputpackagebasev1_json_files_in_dir: Path,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.WriteSyncDbsToTmpFilesInDirTask.do."""
    caplog.set_level(DEBUG)

    if json_files_exist:
        management_repo_dir = outputpackagebasev1_json_files_in_dir
    else:
        management_repo_dir = tmp_path / "foo"

    dependencies = [Mock()]
    task_ = task.WriteSyncDbsToTmpFilesInDirTask(
        compression=CompressionTypeEnum.NONE,
        desc_version=desc_version,
        files_version=FilesVersionEnum.DEFAULT,
        management_repo_dir=management_repo_dir,
        package_repo_dir=tmp_path,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )

    if target_is_dir:
        task_.default_syncdb_path.mkdir(parents=True)
        task_.files_syncdb_path.mkdir(parents=True)

    assert task_.do() == return_value  # nosec: B101
    if json_files_exist and not target_is_dir and isinstance(desc_version, PackageDescVersionEnum):
        assert task_.default_syncdb_path.exists()  # nosec: B101
        assert task_.files_syncdb_path.exists()  # nosec: B101


@mark.parametrize(
    "add_dependencies, return_value, do, target_is_dir",
    [
        (True, ActionStateEnum.NOT_STARTED, True, False),
        (False, ActionStateEnum.NOT_STARTED, True, False),
        (True, ActionStateEnum.NOT_STARTED, False, False),
        (False, ActionStateEnum.NOT_STARTED, False, False),
        (True, ActionStateEnum.NOT_STARTED, True, True),
        (False, ActionStateEnum.NOT_STARTED, True, True),
        (True, ActionStateEnum.NOT_STARTED, False, True),
        (False, ActionStateEnum.NOT_STARTED, False, True),
    ],
)
def test_writesyncdbstotmpfilesindirtask_undo(
    add_dependencies: bool,
    return_value: ActionStateEnum,
    do: bool,
    target_is_dir: bool,
    outputpackagebasev1_json_files_in_dir: Path,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.WriteSyncDbsToTmpFilesInDirTask.undo."""
    caplog.set_level(DEBUG)

    dependencies = [
        Mock(
            state=ActionStateEnum.SUCCESS,
            undo=Mock(return_value=ActionStateEnum.NOT_STARTED),
        ),
    ]
    task_ = task.WriteSyncDbsToTmpFilesInDirTask(
        compression=CompressionTypeEnum.NONE,
        desc_version=PackageDescVersionEnum.DEFAULT,
        files_version=FilesVersionEnum.DEFAULT,
        management_repo_dir=outputpackagebasev1_json_files_in_dir,
        package_repo_dir=tmp_path,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )

    if do:
        assert task_.do()  # nosec: B101
        assert task_.default_syncdb_path.exists()  # nosec: B101
        assert task_.files_syncdb_path.exists()  # nosec: B101

    if target_is_dir:
        if do:
            task_.default_syncdb_path.unlink()
            task_.files_syncdb_path.unlink()

        task_.default_syncdb_path.mkdir(parents=True, exist_ok=True)
        task_.files_syncdb_path.mkdir(parents=True, exist_ok=True)

    assert task_.undo() == return_value  # nosec: B101


@mark.parametrize(
    "add_paths, add_dependencies, expectation",
    [
        (True, False, does_not_raise()),
        (True, True, does_not_raise()),
        (False, True, does_not_raise()),
        (False, False, raises(RuntimeError)),
    ],
)
def test_removebackupfilestask(
    add_paths: bool,
    add_dependencies: bool,
    expectation: ContextManager[str],
) -> None:
    """Tests for repod.action.task.RemoveBackupFilesTask."""
    path = Path("foo.bkp")
    paths = [path]
    dependencies = [
        Mock(),
        Mock(
            spec=task.MoveTmpFilesTask,
            paths=[Mock(destination_backup=path)],
        ),
    ]

    with expectation:
        task_ = task.RemoveBackupFilesTask(
            paths=paths if add_paths else None,
            dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
        )

    if add_dependencies:
        assert task_.input_from_dependency  # nosec: B101
        assert task_.paths == []  # nosec: B101
    else:
        if add_paths:
            assert not task_.input_from_dependency  # nosec: B101
            assert task_.paths == [path]  # nosec: B101


@mark.parametrize(
    "add_paths, add_dependencies, add_move_dep, dep_state, return_value",
    [
        (True, False, False, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (True, True, False, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (False, True, True, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (False, True, True, ActionStateEnum.FAILED, ActionStateEnum.FAILED_DEPENDENCY),
    ],
)
def test_removebackupfilestask_do(
    add_paths: bool,
    add_dependencies: bool,
    add_move_dep: bool,
    dep_state: ActionStateEnum,
    return_value: ActionStateEnum,
    tmp_path: Path,
) -> None:
    """Tests for repod.action.task.RemoveBackupFilesTask.do."""
    path = tmp_path / Path("foo.bkp")
    path.touch()
    paths = [path]
    dependencies = [
        Mock(),
    ]
    if add_move_dep:
        dependencies.append(
            Mock(
                spec=task.MoveTmpFilesTask,
                paths=[Mock(destination_backup=path)],
                state=dep_state,
            )
        )

    task_ = task.RemoveBackupFilesTask(
        paths=paths if add_paths else None,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )
    assert task_.do() == return_value  # nosec: B101

    if dep_state != ActionStateEnum.SUCCESS and add_dependencies and add_move_dep:
        assert path.exists()  # nosec: B101
    else:
        assert not path.exists()  # nosec: B101


@mark.parametrize(
    "add_paths, add_dependencies, do, return_value",
    [
        (True, False, True, ActionStateEnum.NOT_STARTED),
        (True, False, False, ActionStateEnum.NOT_STARTED),
        (False, True, True, ActionStateEnum.NOT_STARTED),
        (False, True, False, ActionStateEnum.NOT_STARTED),
    ],
)
def test_removebackupfilestask_undo(
    add_paths: bool,
    add_dependencies: bool,
    do: bool,
    return_value: ActionStateEnum,
    tmp_path: Path,
) -> None:
    """Tests for repod.action.task.RemoveBackupFilesTask.undo."""
    path = tmp_path / Path("foo.bkp")
    path.touch()
    paths = [path]
    dependencies = [
        Mock(
            undo=Mock(return_value=ActionStateEnum.NOT_STARTED),
        ),
        Mock(
            spec=task.MoveTmpFilesTask,
            paths=[Mock(destination_backup=path)],
            state=ActionStateEnum.SUCCESS,
            undo=Mock(return_value=ActionStateEnum.NOT_STARTED),
        ),
    ]

    task_ = task.RemoveBackupFilesTask(
        paths=paths if add_paths else None,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )
    if do:
        task_.do()

    assert task_.undo() == return_value  # nosec: B101


@mark.parametrize(
    "dir_exists, add_dir, add_pkgbases, add_dependencies, expectation",
    [
        (True, True, True, False, does_not_raise()),
        (True, True, False, True, does_not_raise()),
        (True, True, False, False, raises(RuntimeError)),
        (False, True, False, False, raises(RuntimeError)),
        (False, True, True, False, raises(RuntimeError)),
        (True, False, True, False, raises(RuntimeError)),
    ],
)
def test_consolidateoutputpackagebasestask(
    dir_exists: bool,
    add_dir: bool,
    add_pkgbases: bool,
    add_dependencies: bool,
    expectation: ContextManager[str],
    outputpackagebasev1: OutputPackageBase,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.ConsolidateOutputPackageBasesTask."""
    caplog.set_level(DEBUG)

    directory = tmp_path / "foo"
    if dir_exists:
        directory = tmp_path

    pkgbases = [outputpackagebasev1]

    dependencies = [
        Mock(),
        Mock(
            spec=task.CreateOutputPackageBasesTask,
            pkgbases=[Mock(pkgbases=pkgbases)],
        ),
    ]

    with expectation:
        task_ = task.ConsolidateOutputPackageBasesTask(
            directory=directory if add_dir else None,  # type: ignore[arg-type]
            stability_layer_dirs=([], []),
            dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
            pkgbases=pkgbases if add_pkgbases else None,
        )

    if dir_exists and add_dir:
        if add_dependencies:
            assert task_.input_from_dependency  # nosec: B101
            assert task_.pkgbases == []  # nosec: B101
        else:
            if add_pkgbases:
                assert not task_.input_from_dependency  # nosec: B101
                assert task_.pkgbases == pkgbases  # nosec: B101


@mark.parametrize(
    (
        "pkgbase_without_file, add_pkgbases, add_required_dep, required_dep_state, "
        "add_dependencies, from_file_raises, return_value"
    ),
    [
        (False, True, False, ActionStateEnum.SUCCESS, False, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, False, ActionStateEnum.SUCCESS, False, True, ActionStateEnum.FAILED_TASK),
        (False, False, True, ActionStateEnum.SUCCESS, True, False, ActionStateEnum.SUCCESS_TASK),
        (False, False, True, ActionStateEnum.SUCCESS, True, True, ActionStateEnum.FAILED_TASK),
        (False, False, True, ActionStateEnum.FAILED, True, False, ActionStateEnum.FAILED_DEPENDENCY),
        (True, True, False, ActionStateEnum.SUCCESS, False, False, ActionStateEnum.SUCCESS_TASK),
        (True, True, False, ActionStateEnum.SUCCESS, False, True, ActionStateEnum.FAILED_TASK),
        (True, False, True, ActionStateEnum.SUCCESS, True, False, ActionStateEnum.SUCCESS_TASK),
        (True, False, True, ActionStateEnum.SUCCESS, True, True, ActionStateEnum.FAILED_TASK),
        (True, False, True, ActionStateEnum.FAILED, True, False, ActionStateEnum.FAILED_DEPENDENCY),
    ],
)
def test_consolidateoutputpackagebasestask_do(
    pkgbase_without_file: bool,
    add_pkgbases: bool,
    add_required_dep: bool,
    required_dep_state: ActionStateEnum,
    add_dependencies: bool,
    from_file_raises: bool,
    return_value: ActionStateEnum,
    outputpackagebasev1: OutputPackageBase,
    outputpackagebasev1_json_files_in_dir: Path,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.ConsolidateOutputPackageBasesTask.do."""
    caplog.set_level(DEBUG)

    pkgbases = [outputpackagebasev1]
    if pkgbase_without_file:
        other_pkgbase = deepcopy(outputpackagebasev1)
        other_pkgbase.base = "beh"  # type: ignore[attr-defined]
        pkgbases.append(other_pkgbase)

    dependencies = [
        Mock(),
    ]
    if add_required_dep:
        dependencies.append(
            Mock(
                spec=task.CreateOutputPackageBasesTask,
                pkgbases=pkgbases,
                state=required_dep_state,
            )
        )

    task_ = task.ConsolidateOutputPackageBasesTask(
        directory=outputpackagebasev1_json_files_in_dir,
        stability_layer_dirs=([], []),
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
        pkgbases=pkgbases if add_pkgbases else None,
    )
    if from_file_raises:
        with patch("repod.action.task.OutputPackageBase.from_file", side_effect=RepoManagementFileError):
            assert task_.do() == return_value  # nosec: B101
    else:
        assert task_.do() == return_value  # nosec: B101


@mark.parametrize(
    "dep_undo_success, add_dependencies, add_pkgbases, do, return_value",
    [
        (True, True, False, True, ActionStateEnum.NOT_STARTED),
        (True, True, False, False, ActionStateEnum.NOT_STARTED),
        (False, False, True, True, ActionStateEnum.NOT_STARTED),
        (False, False, True, False, ActionStateEnum.NOT_STARTED),
    ],
)
def test_consolidateoutputpackagebasestask_undo(
    dep_undo_success: bool,
    add_dependencies: bool,
    add_pkgbases: bool,
    do: bool,
    return_value: ActionStateEnum,
    tmp_path: Path,
    outputpackagebasev1: OutputPackageBase,
    outputpackagebasev1_json_files_in_dir: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.ConsolidateOutputPackageBasesTask.undo."""
    caplog.set_level(DEBUG)

    pkgbases = [outputpackagebasev1]
    dependencies = [
        Mock(
            undo=Mock(return_value=ActionStateEnum.NOT_STARTED),
        ),
        Mock(
            spec=task.CreateOutputPackageBasesTask,
            pkgbases=pkgbases,
            state=ActionStateEnum.SUCCESS,
            undo=Mock(
                return_value=ActionStateEnum.NOT_STARTED if dep_undo_success else ActionStateEnum.FAILED_UNDO_TASK,
            ),
        ),
    ]

    task_ = task.ConsolidateOutputPackageBasesTask(
        directory=outputpackagebasev1_json_files_in_dir,
        stability_layer_dirs=([], []),
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
        pkgbases=pkgbases if add_pkgbases else None,
    )
    if do:
        task_.do()

    assert task_.undo() == return_value  # nosec: B101


@mark.parametrize(
    "add_directory, add_names, add_dependencies, expectation",
    [
        (True, True, True, does_not_raise()),
        (True, True, False, does_not_raise()),
        (True, False, True, does_not_raise()),
        (True, False, False, raises(RuntimeError)),
        (False, False, False, raises(RuntimeError)),
        (False, True, False, raises(RuntimeError)),
        (False, False, True, raises(RuntimeError)),
    ],
)
def test_removemanagementreposymlinkstask(
    add_directory: bool,
    add_names: bool,
    add_dependencies: bool,
    expectation: ContextManager[str],
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.RemoveManagementRepoSymlinksTask."""
    caplog.set_level(DEBUG)

    names = ["foo"]
    dependencies = [
        Mock(),
        Mock(
            spec=task.ConsolidateOutputPackageBasesTask,
            current_package_names=[],
            package_names=[],
            state=ActionStateEnum.SUCCESS,
        ),
        Mock(),
    ]

    with expectation:
        task_ = task.RemoveManagementRepoSymlinksTask(
            directory=tmp_path if add_directory else None,  # type: ignore[arg-type]
            names=names if add_names else None,
            dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
        )
        assert task_.directory == tmp_path  # nosec: B101

        if add_dependencies:
            assert task_.dependencies == dependencies  # nosec: B101
            assert task_.input_from_dependency  # nosec: B101
            assert not task_.names  # nosec: B101
        else:
            assert task_.names == names  # nosec: B101
            assert not task_.input_from_dependency  # nosec: B101


@mark.parametrize(
    "add_names, add_dependencies, dependency_state, return_value",
    [
        (True, True, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (True, False, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (False, True, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (True, False, ActionStateEnum.FAILED, ActionStateEnum.FAILED_DEPENDENCY),
        (False, True, ActionStateEnum.FAILED, ActionStateEnum.FAILED_DEPENDENCY),
    ],
)
def test_removemanagementreposymlinkstask_do(
    add_names: bool,
    add_dependencies: bool,
    dependency_state: ActionStateEnum,
    return_value: ActionStateEnum,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.RemoveManagementRepoSymlinksTask.do."""
    caplog.set_level(DEBUG)

    (tmp_path / "pkgnames").mkdir()
    file = tmp_path / "pkgnames" / "foo.json"
    file.touch()

    names = ["foo"]
    dependencies = [
        Mock(),
        Mock(
            spec=task.ConsolidateOutputPackageBasesTask,
            current_package_names=["foo"],
            package_names=[],
            state=dependency_state,
        ),
        Mock(),
    ]

    task_ = task.RemoveManagementRepoSymlinksTask(
        directory=tmp_path,
        names=names if add_names else None,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )
    task_.do() == return_value

    if (add_dependencies and dependency_state == ActionStateEnum.SUCCESS) or add_names:
        assert not file.exists()  # nosec: B101
    else:
        assert file.exists()  # nosec: B101


@mark.parametrize(
    "add_names, add_dependencies, do",
    [
        (True, True, True),
        (False, True, True),
        (True, False, True),
        (True, True, False),
        (False, True, False),
        (True, False, False),
    ],
)
def test_removemanagementreposymlinkstask_undo(
    add_names: bool,
    add_dependencies: bool,
    do: bool,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.RemoveManagementRepoSymlinksTask.undo."""
    caplog.set_level(DEBUG)

    (tmp_path / "pkgnames").mkdir()
    file = tmp_path / "pkgnames" / "foo.json"
    file.touch()

    names = ["foo"]
    dependencies = [
        Mock(),
        Mock(
            spec=task.ConsolidateOutputPackageBasesTask,
            current_package_names=["foo"],
            package_names=[],
            state=ActionStateEnum.SUCCESS,
        ),
        Mock(),
    ]

    task_ = task.RemoveManagementRepoSymlinksTask(
        directory=tmp_path,
        names=names if add_names else None,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )

    if do:
        task_.do()

    task_.undo() == ActionStateEnum.NOT_STARTED

    if add_dependencies and do:
        assert not task_.names  # nosec: B101


@mark.parametrize(
    "add_directory, add_filenames, add_dependencies, expectation",
    [
        (True, True, True, does_not_raise()),
        (True, True, False, does_not_raise()),
        (True, False, True, does_not_raise()),
        (True, False, False, raises(RuntimeError)),
        (False, False, False, raises(RuntimeError)),
        (False, True, False, raises(RuntimeError)),
        (False, False, True, raises(RuntimeError)),
    ],
)
def test_removepackagereposymlinkstask(
    add_directory: bool,
    add_filenames: bool,
    add_dependencies: bool,
    expectation: ContextManager[str],
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.RemovePackageRepoSymlinksTask."""
    caplog.set_level(DEBUG)

    filenames = ["foo-1.0.0-1-x86_64.pkg.tar.zst"]
    dependencies = [
        Mock(),
        Mock(
            spec=task.ConsolidateOutputPackageBasesTask,
            current_filenames=[],
            state=ActionStateEnum.SUCCESS,
        ),
        Mock(),
    ]

    with expectation:
        task_ = task.RemovePackageRepoSymlinksTask(
            directory=tmp_path if add_directory else None,  # type: ignore[arg-type]
            filenames=filenames if add_filenames else None,
            dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
        )
        assert task_.directory == tmp_path  # nosec: B101

        if add_dependencies:
            assert task_.dependencies == dependencies  # nosec: B101
            assert task_.input_from_dependency  # nosec: B101
            assert not task_.filenames  # nosec: B101
        else:
            assert task_.filenames == filenames  # nosec: B101
            assert not task_.input_from_dependency  # nosec: B101


@mark.parametrize(
    "add_filenames, add_dependencies, dependency_state, return_value",
    [
        (True, True, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (True, False, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (False, True, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (True, False, ActionStateEnum.FAILED, ActionStateEnum.FAILED_DEPENDENCY),
        (False, True, ActionStateEnum.FAILED, ActionStateEnum.FAILED_DEPENDENCY),
    ],
)
def test_removepackagereposymlinkstask_do(
    add_filenames: bool,
    add_dependencies: bool,
    dependency_state: ActionStateEnum,
    return_value: ActionStateEnum,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.RemovePackageRepoSymlinksTask.do."""
    caplog.set_level(DEBUG)

    filenames = ["foo-1.0.0-1-x86_64.pkg.tar.zst"]
    package_file = tmp_path / filenames[0]
    package_file.touch()
    signature_file = tmp_path / f"{filenames[0]}.sig"
    signature_file.touch()

    dependencies = [
        Mock(),
        Mock(
            spec=task.ConsolidateOutputPackageBasesTask,
            current_filenames=filenames,
            state=dependency_state,
        ),
        Mock(),
    ]

    task_ = task.RemovePackageRepoSymlinksTask(
        directory=tmp_path,
        filenames=filenames if add_filenames else None,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )
    task_.do() == return_value

    if (add_dependencies and dependency_state == ActionStateEnum.SUCCESS) or add_filenames:
        assert not package_file.exists()  # nosec: B101
        assert not signature_file.exists()  # nosec: B101
    else:
        assert package_file.exists()  # nosec: B101
        assert signature_file.exists()  # nosec: B101


@mark.parametrize(
    "add_filenames, add_dependencies, do",
    [
        (True, True, True),
        (False, True, True),
        (True, False, True),
        (True, True, False),
        (False, True, False),
        (True, False, False),
    ],
)
def test_removepackagereposymlinkstask_undo(
    add_filenames: bool,
    add_dependencies: bool,
    do: bool,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.RemovePackageRepoSymlinksTask.undo."""
    caplog.set_level(DEBUG)

    filenames = ["foo-1.0.0-1-x86_64.pkg.tar.zst"]
    (tmp_path / "pkgnames").mkdir()
    package_file = tmp_path / "pkgnames" / filenames[0]
    package_file.touch()
    signature_file = tmp_path / "pkgnames" / f"{filenames[0]}.sig"
    signature_file.touch()

    dependencies = [
        Mock(),
        Mock(
            spec=task.ConsolidateOutputPackageBasesTask,
            current_filenames=filenames,
            state=ActionStateEnum.SUCCESS,
        ),
        Mock(),
    ]

    task_ = task.RemovePackageRepoSymlinksTask(
        directory=tmp_path,
        filenames=filenames if add_filenames else None,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )

    if do:
        task_.do()

    task_.undo() == ActionStateEnum.NOT_STARTED

    if add_dependencies and do:
        assert not task_.filenames  # nosec: B101


def test_cleanuprepotask() -> None:
    """Tests for repod.action.task.CleanupRepoTask."""
    assert task.CleanupRepoTask(dependencies=[])  # nosec: B101


def test_cleanuprepotask_do() -> None:
    """Tests for repod.action.task.CleanupRepoTask.do."""
    assert task.CleanupRepoTask(dependencies=[]).do() == ActionStateEnum.SUCCESS_TASK  # nosec: B101


def test_cleanuprepotask_undo() -> None:
    """Tests for repod.action.task.CleanupRepoTask.undo."""
    task_ = task.CleanupRepoTask(dependencies=[])
    assert task_.do() == ActionStateEnum.SUCCESS_TASK  # nosec: B101
    assert task_.undo() == ActionStateEnum.NOT_STARTED  # nosec: B101


@mark.parametrize(
    "add_archive_dir, add_filenames, add_dependencies, expectation",
    [
        (True, True, True, does_not_raise()),
        (True, False, True, does_not_raise()),
        (True, True, False, does_not_raise()),
        (True, False, False, raises(RuntimeError)),
        (False, True, True, raises(RuntimeError)),
        (False, False, True, raises(RuntimeError)),
    ],
)
def test_addtoarchivetask(
    add_archive_dir: bool,
    add_filenames: bool,
    add_dependencies: bool,
    expectation: ContextManager[str],
    tmp_path: Path,
    default_package_file: tuple[Path, ...],
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.AddToArchiveTask."""
    caplog.set_level(DEBUG)

    archive_dir = None
    if add_archive_dir:
        archive_dir = tmp_path / "archive"
        archive_dir.mkdir()

    filenames = None
    if add_filenames:
        filenames = list(default_package_file)

    dependencies = None
    if add_dependencies:
        dependencies = [
            Mock(),
            Mock(
                spec=task.FilesToRepoDirTask,
            ),
            Mock(),
        ]

    with expectation:
        task.AddToArchiveTask(
            archive_dir=archive_dir,  # type: ignore[arg-type]
            filenames=filenames,
            dependencies=dependencies,  # type: ignore[arg-type]
        )


@mark.parametrize(
    "add_archive_dir, add_filenames, add_dependencies, dependency_state, return_value",
    [
        (True, True, True, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (True, False, True, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (True, True, True, ActionStateEnum.FAILED, ActionStateEnum.FAILED_DEPENDENCY),
        (True, False, True, ActionStateEnum.FAILED, ActionStateEnum.FAILED_DEPENDENCY),
        (True, True, False, None, ActionStateEnum.SUCCESS_TASK),
    ],
)
def test_addtoarchivetask_do(
    add_archive_dir: bool,
    add_filenames: bool,
    add_dependencies: bool,
    dependency_state: ActionStateEnum,
    return_value: ActionStateEnum,
    tmp_path: Path,
    default_package_file: tuple[Path, ...],
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.AddToArchiveTask.do."""
    caplog.set_level(DEBUG)

    archive_dir = None
    if add_archive_dir:
        archive_dir = tmp_path / "archive"
        archive_dir.mkdir()

    filenames = None
    if add_filenames:
        filenames = list(default_package_file)

    dependencies = None
    if add_dependencies:
        dependencies = [
            Mock(),
            Mock(
                spec=task.FilesToRepoDirTask,
                files=default_package_file,
                state=dependency_state,
            ),
            Mock(),
        ]

    task_ = task.AddToArchiveTask(
        archive_dir=archive_dir,  # type: ignore[arg-type]
        filenames=filenames,
        dependencies=dependencies,  # type: ignore[arg-type]
    )
    assert task_.do() == return_value  # nosec: B101


@mark.parametrize(
    "add_archive_dir, add_filenames, add_dependencies, dependency_state, do",
    [
        (True, True, True, ActionStateEnum.SUCCESS, True),
        (True, False, True, ActionStateEnum.SUCCESS, True),
        (True, True, False, None, True),
        (True, True, True, ActionStateEnum.SUCCESS, False),
        (True, False, True, ActionStateEnum.SUCCESS, False),
        (True, True, False, None, False),
    ],
)
def test_addtoarchivetask_undo(
    add_archive_dir: bool,
    add_filenames: bool,
    add_dependencies: bool,
    dependency_state: ActionStateEnum,
    do: bool,
    tmp_path: Path,
    default_package_file: tuple[Path, ...],
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.AddToArchiveTask.undo."""
    caplog.set_level(DEBUG)

    archive_dir = None
    if add_archive_dir:
        archive_dir = tmp_path / "archive"
        archive_dir.mkdir()

    filenames = None
    if add_filenames:
        filenames = list(default_package_file)

    dependencies = None
    if add_dependencies:
        dependencies = [
            Mock(
                spec=task.FilesToRepoDirTask,
                files=default_package_file,
                state=dependency_state,
                undo=Mock(return_value=ActionStateEnum.NOT_STARTED),
            ),
        ]

    task_ = task.AddToArchiveTask(
        archive_dir=archive_dir,  # type: ignore[arg-type]
        filenames=filenames,
        dependencies=dependencies,  # type: ignore[arg-type]
    )
    if do:
        task_.do()
        if add_dependencies:
            assert task_.files  # nosec: B101
    assert task_.undo() == ActionStateEnum.NOT_STARTED  # nosec: B101

    if add_dependencies and do:
        assert not task_.files  # nosec: B101


@mark.parametrize(
    (
        "add_archive_dir, add_management_dirs, management_dirs_exist, "
        "add_pkgbases, add_dependencies, add_matching_dep, expectation"
    ),
    [
        (True, True, True, True, False, False, does_not_raise()),
        (True, True, True, True, True, True, does_not_raise()),
        (True, True, True, False, True, True, does_not_raise()),
        (False, True, True, True, False, False, does_not_raise()),
        (False, True, True, True, True, True, does_not_raise()),
        (False, True, True, False, True, True, does_not_raise()),
        (True, False, True, True, False, False, raises(RuntimeError)),
        (True, False, True, True, True, True, raises(RuntimeError)),
        (False, False, True, True, False, False, raises(RuntimeError)),
        (False, False, True, True, True, True, raises(RuntimeError)),
        (True, True, False, True, False, False, raises(RuntimeError)),
        (True, True, False, True, True, True, raises(RuntimeError)),
        (False, True, False, True, False, False, raises(RuntimeError)),
        (False, True, False, True, True, True, raises(RuntimeError)),
        (True, True, True, False, False, False, raises(RuntimeError)),
        (False, True, True, False, False, False, raises(RuntimeError)),
    ],
)
def test_reproduciblebuildenvironmenttask(
    add_archive_dir: bool,
    add_management_dirs: bool,
    management_dirs_exist: bool,
    add_pkgbases: bool,
    add_dependencies: bool,
    add_matching_dep: bool,
    expectation: ContextManager[str],
    outputpackagebasev1: OutputPackageBase,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.ReproducibleBuildEnvironmentTask."""
    caplog.set_level(DEBUG)

    archive_dir = None
    if add_archive_dir:
        archive_dir = Path("foo")

    dependencies = [Mock()]
    if add_matching_dep:
        dependencies += [Mock(spec=task.CreateOutputPackageBasesTask)]

    management_dirs = []
    if add_management_dirs:
        management_dirs = [tmp_path / "foo"]
        if management_dirs_exist:
            management_dirs = [tmp_path]

    with expectation:
        task_ = task.ReproducibleBuildEnvironmentTask(
            archive_dir=archive_dir,
            management_directories=management_dirs,
            pkgbases=[outputpackagebasev1] if add_pkgbases else [],
            dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
        )
        if add_dependencies:
            assert task_.dependencies == dependencies  # nosec: B101


@mark.parametrize(
    (
        "deps_in_archive, deps_in_repo, deps_in_transaction, add_pkgbases, add_dependencies, add_matching_dep, "
        "dependency_state, read_from_mgmt_repo_raises, read_from_archive_dir_raises, return_value"
    ),
    [
        (True, False, False, True, False, False, None, False, False, ActionStateEnum.SUCCESS_TASK),
        (True, False, False, True, False, False, None, True, False, ActionStateEnum.FAILED_TASK),
        (True, False, False, True, False, False, None, False, True, ActionStateEnum.FAILED_TASK),
        (True, False, False, False, True, True, ActionStateEnum.SUCCESS, False, False, ActionStateEnum.SUCCESS_TASK),
        (True, False, False, False, True, True, ActionStateEnum.SUCCESS, True, False, ActionStateEnum.FAILED_TASK),
        (True, False, False, False, True, True, ActionStateEnum.SUCCESS, False, True, ActionStateEnum.FAILED_TASK),
        (
            True,
            False,
            False,
            False,
            True,
            True,
            ActionStateEnum.FAILED,
            False,
            False,
            ActionStateEnum.FAILED_DEPENDENCY,
        ),
        (False, True, False, True, False, False, None, False, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, False, True, False, False, None, True, False, ActionStateEnum.FAILED_TASK),
        (False, True, False, True, False, False, None, False, True, ActionStateEnum.FAILED_TASK),
        (False, True, False, False, True, True, ActionStateEnum.SUCCESS, False, False, ActionStateEnum.SUCCESS_TASK),
        (False, True, False, False, True, True, ActionStateEnum.SUCCESS, True, False, ActionStateEnum.FAILED_TASK),
        (False, True, False, False, True, True, ActionStateEnum.SUCCESS, False, True, ActionStateEnum.FAILED_TASK),
        (
            False,
            True,
            False,
            False,
            True,
            True,
            ActionStateEnum.FAILED,
            False,
            False,
            ActionStateEnum.FAILED_DEPENDENCY,
        ),
        (False, False, True, True, False, False, None, False, False, ActionStateEnum.SUCCESS_TASK),
        (False, False, True, True, False, False, None, True, False, ActionStateEnum.FAILED_TASK),
        (False, False, True, True, False, False, None, False, True, ActionStateEnum.FAILED_TASK),
        (False, False, True, False, True, True, ActionStateEnum.SUCCESS, False, False, ActionStateEnum.SUCCESS_TASK),
        (False, False, True, False, True, True, ActionStateEnum.SUCCESS, True, False, ActionStateEnum.FAILED_TASK),
        (False, False, True, False, True, True, ActionStateEnum.SUCCESS, False, True, ActionStateEnum.FAILED_TASK),
        (
            False,
            False,
            True,
            False,
            True,
            True,
            ActionStateEnum.FAILED,
            False,
            False,
            ActionStateEnum.FAILED_DEPENDENCY,
        ),
    ],
)
def test_reproduciblebuildenvironmenttask_do(  # noqa: C901
    deps_in_archive: bool,
    deps_in_repo: bool,
    deps_in_transaction: bool,
    add_pkgbases: bool,
    add_dependencies: bool,
    add_matching_dep: bool,
    dependency_state: ActionStateEnum,
    read_from_mgmt_repo_raises: bool,
    read_from_archive_dir_raises: bool,
    return_value: ActionStateEnum,
    default_installed: list[str],
    outputpackagebasev1: OutputPackageBase,
    outputpackagebasev1_json_files_in_dir: Path,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.ReproducibleBuildEnvironmentTask.do."""
    caplog.set_level(DEBUG)

    pkgs_in_archive: set[str] = set()
    pkgs_in_repo: set[str] = set()
    pkgs_in_transaction: set[str] = set()

    archive_dir = None
    if deps_in_archive:
        archive_dir = tmp_path / "archive"
        for dep in default_installed:
            dep_dir = archive_dir / dep[0] / "-".join(dep.split("-")[0:-3])
            dep_dir.mkdir(parents=True)
            (dep_dir / f"{dep}.pkg.tar.zst").touch()
        pkgs_in_archive = set([dep for dep in default_installed])
    elif deps_in_repo:
        installed = [
            f"{pkg.name}-{outputpackagebasev1.version}-{pkg.arch}"  # type: ignore[attr-defined]
            for pkg in outputpackagebasev1.packages  # type: ignore[attr-defined]
        ]

        del outputpackagebasev1.packages[0]  # type: ignore[attr-defined]
        outputpackagebasev1.packages[0].name = "foo2000"  # type: ignore[attr-defined]
        outputpackagebasev1.buildinfo.installed = installed  # type: ignore[attr-defined]
        pkgs_in_repo = set([dep for dep in installed])
    elif deps_in_transaction:
        installed = [
            f"{pkg.name}-{outputpackagebasev1.version}-{pkg.arch}"  # type: ignore[attr-defined]
            for pkg in outputpackagebasev1.packages  # type: ignore[attr-defined]
        ]
        pkgs_in_transaction = set([dep for dep in installed])

    dependencies = [Mock()]
    if add_matching_dep:
        dependencies += [
            Mock(
                spec=task.CreateOutputPackageBasesTask,
                pkgbases=[outputpackagebasev1],
                state=dependency_state,
            )
        ]

    task_ = task.ReproducibleBuildEnvironmentTask(
        archive_dir=archive_dir,
        management_directories=[outputpackagebasev1_json_files_in_dir],
        pkgbases=[outputpackagebasev1] if add_pkgbases else None,
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )

    if read_from_mgmt_repo_raises:
        with patch("repod.action.task.read_build_requirements_from_management_repo_dirs", side_effect=TaskError):
            assert return_value == task_.do()  # nosec: B101
    elif read_from_archive_dir_raises:
        with patch("repod.action.task.read_build_requirements_from_archive_dir", side_effect=TaskError):
            assert return_value == task_.do()  # nosec: B101
    else:
        assert return_value == task_.do()  # nosec: B101

    if deps_in_archive and return_value == ActionStateEnum.SUCCESS_TASK:
        assert pkgs_in_archive == task_.pkgs_in_archive  # nosec: B101
    if deps_in_repo and return_value == ActionStateEnum.SUCCESS_TASK:
        assert pkgs_in_repo == task_.pkgs_in_repo  # nosec: B101
    if deps_in_transaction and return_value == ActionStateEnum.SUCCESS_TASK:
        assert pkgs_in_transaction == task_.pkgs_in_transaction  # nosec: B101


@mark.parametrize("do, input_from_dep", [(True, False), (True, True), (False, False), (False, True)])
def test_reproduciblebuildenvironmenttask_undo(
    do: bool,
    input_from_dep: bool,
    outputpackagebasev1: OutputPackageBase,
    outputpackagebasev1_json_files_in_dir: Path,
) -> None:
    """Tests for repod.action.task.ReproducibleBuildEnvironmentTask.undo."""
    task_ = task.ReproducibleBuildEnvironmentTask(
        archive_dir=None,
        management_directories=[outputpackagebasev1_json_files_in_dir],
        pkgbases=[outputpackagebasev1],
        dependencies=None,
    )

    if do:
        task_.state = ActionStateEnum.SUCCESS_TASK
        task_.pkgs_in_archive = {"foo-2000-any"}
        task_.pkgs_in_repo = {"bar-2000-any"}
        task_.pkgs_in_transaction = {"baz-2000-any"}
    if input_from_dep:
        task_.input_from_dependency = True
        if not do:
            task_.pkgbases.clear()

    assert ActionStateEnum.NOT_STARTED == task_.undo()  # nosec: B101
    assert not task_.pkgs_in_archive  # nosec: B101
    assert not task_.pkgs_in_repo  # nosec: B101
    assert not task_.pkgs_in_transaction  # nosec: B101
    if input_from_dep:
        assert not task_.pkgbases  # nosec: B101


@mark.parametrize(
    ("add_pkgbases, add_dependencies, add_matching_dep, expectation"),
    [
        (True, False, False, does_not_raise()),
        (True, True, False, does_not_raise()),
        (True, True, True, does_not_raise()),
        (False, True, True, does_not_raise()),
        (False, False, False, raises(RuntimeError)),
    ],
)
def test_repogrouptask(
    add_pkgbases: bool,
    add_dependencies: bool,
    add_matching_dep: bool,
    expectation: ContextManager[str],
    outputpackagebasev1: OutputPackageBase,
    packagerepo_in_tmp_path: PackageRepo,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.RepoGroupTask."""
    caplog.set_level(DEBUG)

    dependencies = [Mock()]
    if add_matching_dep:
        dependencies += [Mock(spec=task.CreateOutputPackageBasesTask)]

    with expectation:
        task_ = task.RepoGroupTask(
            repositories=[packagerepo_in_tmp_path],
            pkgbases=[outputpackagebasev1] if add_pkgbases else [],
            dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
        )
        if add_dependencies:
            assert task_.dependencies == dependencies  # nosec: B101


@mark.parametrize(
    ("add_pkgbases, add_dependencies, add_matching_dep, dependency_state, return_value"),
    [
        (True, False, False, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (True, True, False, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (True, True, True, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (False, True, True, ActionStateEnum.SUCCESS, ActionStateEnum.SUCCESS_TASK),
        (False, True, True, ActionStateEnum.FAILED, ActionStateEnum.FAILED_DEPENDENCY),
    ],
)
def test_repogrouptask_do(
    add_pkgbases: bool,
    add_dependencies: bool,
    add_matching_dep: bool,
    dependency_state: ActionStateEnum,
    return_value: ActionStateEnum,
    outputpackagebasev1: OutputPackageBase,
    packagerepo_in_tmp_path: PackageRepo,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.RepoGroupTask.do."""
    caplog.set_level(DEBUG)

    dependencies = [Mock()]
    if add_matching_dep:
        dependencies += [
            Mock(
                spec=task.CreateOutputPackageBasesTask,
                pkgbases=[outputpackagebasev1],
                state=dependency_state,
            )
        ]

    task_ = task.RepoGroupTask(
        repositories=[packagerepo_in_tmp_path],
        pkgbases=[outputpackagebasev1] if add_pkgbases else [],
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )
    assert return_value == task_.do()  # nosec: B101
    if ActionStateEnum.FAILED == dependency_state:
        assert not task_.pkgbase_names  # nosec: B101
        assert not task_.package_names  # nosec: B101
        assert not task_.repo_management_dirs  # nosec: B101
    else:
        assert task_.pkgbase_names  # nosec: B101
        assert task_.package_names  # nosec: B101
        assert task_.repo_management_dirs  # nosec: B101


@mark.parametrize(
    ("add_pkgbases, add_dependencies, do"),
    [
        (True, False, False),
        (True, False, True),
        (True, True, True),
        (False, True, True),
    ],
)
def test_repogrouptask_undo(
    add_pkgbases: bool,
    add_dependencies: bool,
    do: bool,
    outputpackagebasev1: OutputPackageBase,
    packagerepo_in_tmp_path: PackageRepo,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.action.task.RepoGroupTask.undo."""
    caplog.set_level(DEBUG)

    dependencies = [
        Mock(
            spec=task.CreateOutputPackageBasesTask,
            pkgbases=[outputpackagebasev1],
            state=ActionStateEnum.SUCCESS,
            undo=Mock(return_value=ActionStateEnum.NOT_STARTED),
        ),
    ]

    task_ = task.RepoGroupTask(
        repositories=[packagerepo_in_tmp_path],
        pkgbases=[outputpackagebasev1] if add_pkgbases else [],
        dependencies=dependencies if add_dependencies else None,  # type: ignore[arg-type]
    )
    if do:
        task_.do()

    assert ActionStateEnum.NOT_STARTED == task_.undo()  # nosec: B101
    assert not task_.pkgbase_names  # nosec: B101
    assert not task_.package_names  # nosec: B101
    assert not task_.repo_management_dirs  # nosec: B101
