"""Tests for repod.archive.archive."""

from contextlib import nullcontext as does_not_raise
from pathlib import Path
from typing import ContextManager

from pytest import mark, raises

from repod.archive import archive
from repod.errors import RepoManagementValidationError


@mark.parametrize(
    "source, destination, expectation",
    [
        (Path("/foo"), Path("/bar"), does_not_raise()),
        (Path("foo"), Path("/bar"), raises(ValueError)),
        (Path("/foo"), Path("bar"), raises(ValueError)),
        (None, Path("/bar"), raises(ValueError)),
        (Path("/foo"), None, raises(ValueError)),
    ],
)
def test_copysourcedestination(source: Path, destination: Path, expectation: ContextManager[str]) -> None:
    """Tests for repod.archive.archive.CopySourceDestination."""
    with expectation:
        archive.CopySourceDestination(source=source, destination=destination)


@mark.parametrize(
    "source, output_dir_is_path, expectation",
    [
        (Path("/foo/foo-1.0.0-1-any.pkg.tar.zst"), True, does_not_raise()),
        (Path("/foo/foo-1.0.0-1-any.pkg.tar.zst.sig"), True, does_not_raise()),
        (None, True, raises(RepoManagementValidationError)),
        (Path("/foo"), True, raises(RepoManagementValidationError)),
        (Path("/foo/foo-1.0.0-1-any.pkg.tar.zst"), False, raises(RepoManagementValidationError)),
        (Path("/foo/foo-1.0.0-1-any.pkg.tar.zst.sig"), False, raises(RepoManagementValidationError)),
    ],
)
def test_copysourcedestination_from_archive_dir(
    source: Path,
    output_dir_is_path: bool,
    expectation: ContextManager[str],
    tmp_path: Path,
) -> None:
    """Tests for repod.archive.archive.CopySourceDestination.from_archive_dir."""
    with expectation:
        archive.CopySourceDestination.from_archive_dir(
            source=source,
            output_dir=tmp_path if output_dir_is_path else None,  # type: ignore[arg-type]
        )


def test_copysourcedestination_copy_file(
    text_file: Path,
) -> None:
    """Tests for repod.archive.archive.CopySourceDestination.copy_file."""
    source = text_file
    destination = text_file.parent / "foo" / text_file.name

    assert source.exists()  # nosec: B101
    assert not destination.exists()  # nosec: B101

    obj = archive.CopySourceDestination(
        source=source,
        destination=destination,
    )
    obj.copy_file()

    assert source.exists()  # nosec: B101
    assert destination.exists()  # nosec: B101


def test_copysourcedestination_remove_destination(
    text_file: Path,
) -> None:
    """Tests for repod.archive.archive.CopySourceDestination.remove_destination."""
    source = text_file
    destination = text_file.parent / "foo" / text_file.name

    assert source.exists()  # nosec: B101
    assert not destination.exists()  # nosec: B101

    obj = archive.CopySourceDestination(
        source=source,
        destination=destination,
    )
    obj.copy_file()

    assert source.exists()  # nosec: B101
    assert destination.exists()  # nosec: B101

    obj.remove_destination()

    assert source.exists()  # nosec: B101
    assert not destination.exists()  # nosec: B101
    assert destination.parent.exists()  # nosec: B101
