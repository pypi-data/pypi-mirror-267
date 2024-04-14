"""Tests for repod.common.models."""

from contextlib import nullcontext as does_not_raise
from typing import ContextManager
from unittest.mock import patch

from pydantic import ValidationError
from pytest import mark, raises
from pytest_lazy_fixtures import lf

from repod.common import models
from repod.version.alpm import vercmp
from tests.conftest import (
    create_default_full_version,
    create_default_invalid_full_version,
)


@mark.parametrize(
    "backup, expectation",
    [
        (None, does_not_raise()),
        ([], does_not_raise()),
        (["foo"], does_not_raise()),
        (["home/"], does_not_raise()),
        (["/foo"], raises(ValidationError)),
        (["home/foo"], raises(ValidationError)),
    ],
)
def test_backup_validate_backup(backup: list[str] | None, expectation: ContextManager[str]) -> None:
    """Tests for repod.common.models.Backup.validate_backup."""
    with expectation:
        models.Backup(backup=backup)


@mark.parametrize(
    "builddate, expectation",
    [
        (-1, raises(ValueError)),
        (1, does_not_raise()),
    ],
)
def test_builddate(builddate: int, expectation: ContextManager[str]) -> None:
    """Tests for repod.common.models.BuildDate."""
    with expectation:
        assert builddate == models.BuildDate(builddate=builddate).builddate  # nosec: B101


@mark.parametrize(
    "csize, expectation",
    [
        (-1, raises(ValueError)),
        (1, does_not_raise()),
    ],
)
def test_csize(csize: int, expectation: ContextManager[str]) -> None:
    """Tests for repod.common.models.CSize."""
    with expectation:
        assert csize == models.CSize(csize=csize).csize  # nosec: B101


@mark.parametrize(
    "value, expectation",
    [
        ("1", does_not_raise()),
        (1, does_not_raise()),
        (None, does_not_raise()),
        ("0", raises(ValidationError)),
        ("-1", raises(ValidationError)),
        ("1.1", raises(ValidationError)),
    ],
)
def test_epoch(value: int | None, expectation: ContextManager[str]) -> None:
    """Tests for repod.common.models.Epoch."""
    with expectation:
        assert isinstance(models.Epoch(epoch=value), models.Epoch)  # nosec: B101


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1", "1", 0),
        ("1", "2", -1),
        ("2", "1", 1),
        (1, 1, 0),
        (1, 2, -1),
        (2, 1, 1),
    ],
)
def test_epoch_vercmp(subj: int | None, obj: int | None, expectation: int) -> None:
    """Tests for repod.common.models.Epoch compared using vercmp."""
    assert expectation == vercmp(  # nosec: B101
        a=str(models.Epoch(epoch=subj).epoch), b=str(models.Epoch(epoch=obj).epoch)
    )


@mark.parametrize(
    "file_list, expectation",
    [
        (None, does_not_raise()),
        ([], does_not_raise()),
        (["foo"], does_not_raise()),
        (["home/"], does_not_raise()),
        (["home/foo"], raises(ValidationError)),
        (["/foo"], raises(ValidationError)),
    ],
)
def test_filelist_validate_files(file_list: list[str] | None, expectation: ContextManager[str]) -> None:
    """Tests for repod.common.models.FileList."""
    with expectation:
        models.FileList(files=file_list)


@mark.parametrize(
    "isize, expectation",
    [
        (-1, raises(ValueError)),
        (1, does_not_raise()),
    ],
)
def test_isize(isize: int, expectation: ContextManager[str]) -> None:
    """Tests for repod.common.models.ISize."""
    with expectation:
        assert isize == models.ISize(isize=isize).isize  # nosec: B101


@mark.parametrize(
    "name, expectation",
    [
        (".foo", raises(ValueError)),
        ("-foo", raises(ValueError)),
        ("foo'", raises(ValueError)),
        ("foo", does_not_raise()),
    ],
)
def test_name(name: str, expectation: ContextManager[str]) -> None:
    """Tests for repod.common.models.ISize."""
    with expectation:
        assert name == models.Name(name=name).name  # nosec: B101


def test_packager(default_packager: str, default_invalid_packager: str) -> None:
    """Tests for repod.common.models.Packager."""
    with does_not_raise():
        models.Packager(packager=default_packager)
    with raises(ValidationError):
        models.Packager(packager=default_invalid_packager)


@mark.parametrize(
    "value, expectation",
    [
        ("1", does_not_raise()),
        ("1.1", does_not_raise()),
        (1, raises(ValidationError)),
        (1.1, raises(ValidationError)),
        ("0", raises(ValidationError)),
        ("-1", raises(ValidationError)),
        ("1.a", raises(ValidationError)),
    ],
)
def test_pkgrel(value: str, expectation: ContextManager[str]) -> None:
    """Tests for repod.common.models.PkgRel."""
    with expectation:
        assert isinstance(models.PkgRel(pkgrel=value), models.PkgRel)  # nosec: B101


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1", "1", 0),
        ("2", "1", 1),
        ("1", "2", -1),
        ("1", "1.1", -1),
        ("1.1", "1", 1),
        ("1.1", "1.1", 0),
        ("1.2", "1.1", 1),
        ("1.1", "1.2", -1),
    ],
)
@mark.parametrize("pyalpm_vercmp", [lf("pyalpm_vercmp_fun")])
def test_pkgrel_vercmp(subj: str, obj: str, expectation: int, pyalpm_vercmp: bool) -> None:
    """Tests for repod.common.models.PkgRel comparing using vercmp."""
    with patch("repod.version.alpm.PYALPM_VERCMP", pyalpm_vercmp):
        assert expectation == vercmp(  # nosec: B101
            a=models.PkgRel(pkgrel=subj).pkgrel, b=models.PkgRel(pkgrel=obj).pkgrel
        )


@mark.parametrize(
    "value, expectation",
    [
        ("1", does_not_raise()),
        ("1.1", does_not_raise()),
        ("1.a", does_not_raise()),
        (1, raises(ValidationError)),
        (1.1, raises(ValidationError)),
        ("0", does_not_raise()),
        ("foo", does_not_raise()),
        ("-1", raises(ValidationError)),
        (".1", raises(ValidationError)),
    ],
)
def test_pkgver(value: str, expectation: ContextManager[str]) -> None:
    """Tests for repod.common.models.PkgVer."""
    with expectation:
        assert isinstance(models.PkgVer(pkgver=value), models.PkgVer)  # nosec: B101


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1", "1", 0),
        ("2", "1", 1),
        ("1", "2", -1),
        ("1", "1.1", -1),
        ("1.1", "1", 1),
        ("1.1", "1.1", 0),
        ("1.2", "1.1", 1),
        ("1.1", "1.2", -1),
        ("1+2", "1+1", 1),
        ("1+1", "1+2", -1),
        ("1.1", "1.1a", 1),
        ("1.1a", "1.1", -1),
        ("1.1", "1.1a1", 1),
        ("1.1a1", "1.1", -1),
        ("1.1", "1.11a", -1),
        ("1.11a", "1.1", 1),
        ("1.1_a", "1.1", 1),
        ("1.1", "1.1_a", -1),
        ("1.1", "1.1.a", -1),
        ("1.a", "1.1", -1),
        ("1.1", "1.a", 1),
        ("1.a1", "1.1", -1),
        ("1.1", "1.a1", 1),
        ("1.a11", "1.1", -1),
        ("1.1", "1.a11", 1),
        ("a.1", "1.1", -1),
        ("1.1", "a.1", 1),
        ("foo", "1.1", -1),
        ("1.1", "foo", 1),
        ("a1a", "a1b", -1),
        ("a1b", "a1a", 1),
        ("20220102", "20220202", -1),
        ("20220202", "20220102", 1),
        ("1.0..", "1.0.", 0),
        ("1.0.", "1.0", 1),
        ("1..0", "1.0", 1),
        ("1..0", "1..0", 0),
        ("1..0", "1..1", -1),
        ("1.0", "1+0", 0),
        ("1.1a1", "1.111", -1),
        ("01", "1", 0),
        ("001a", "1a", 0),
        ("1.a001a.1", "1.a1a.1", 0),
    ],
)
@mark.parametrize("pyalpm_vercmp", [lf("pyalpm_vercmp_fun")])
def test_pkgver_vercmp(subj: str, obj: str, expectation: int, pyalpm_vercmp: bool) -> None:
    """Tests for repod.common.models.PkgVer comparing using vercmp."""
    with patch("repod.version.alpm.PYALPM_VERCMP", pyalpm_vercmp):
        assert expectation == vercmp(  # nosec: B101
            a=models.PkgVer(pkgver=subj).pkgver, b=models.PkgVer(pkgver=obj).pkgver
        )


@mark.parametrize(
    "value, expectation",
    [
        (f"{create_default_full_version()}", does_not_raise()),
        (f"{create_default_invalid_full_version()}", raises(ValidationError)),
    ],
)
def test_version(value: str, expectation: ContextManager[str]) -> None:
    """Tests for repod.common.models.Version."""
    with expectation:
        assert isinstance(models.Version(version=value), models.Version)  # nosec: B101


@mark.parametrize(
    "value, expectation",
    [
        ("1:1.0.0-1", models.Epoch(epoch=1)),
        ("1.0.0-1", None),
    ],
)
def test_version_get_epoch(value: str, expectation: models.Epoch | None) -> None:
    """Tests for repod.common.models.Version.get_epoch."""
    assert models.Version(version=value).get_epoch() == expectation  # nosec: B101


@mark.parametrize(
    "value, expectation",
    [
        ("1:1.0.0-1", models.PkgVer(pkgver="1.0.0")),
        ("1:1_0_0-1", models.PkgVer(pkgver="1_0_0")),
        ("1.0.0-1", models.PkgVer(pkgver="1.0.0")),
        ("1_0_0-1", models.PkgVer(pkgver="1_0_0")),
    ],
)
def test_version_get_pkgver(value: str, expectation: models.PkgVer | None) -> None:
    """Tests for repod.common.models.Version.get_pkgver."""
    assert models.Version(version=value).get_pkgver() == expectation  # nosec: B101


@mark.parametrize(
    "value, expectation",
    [
        ("1:1.0.0-1", models.PkgRel(pkgrel="1")),
        ("1:1_0_0-1", models.PkgRel(pkgrel="1")),
        ("1.0.0-1", models.PkgRel(pkgrel="1")),
        ("1_0_0-1", models.PkgRel(pkgrel="1")),
        ("1:1.0.0-1.1", models.PkgRel(pkgrel="1.1")),
        ("1:1_0_0-1.1", models.PkgRel(pkgrel="1.1")),
        ("1.0.0-1.1", models.PkgRel(pkgrel="1.1")),
        ("1_0_0-1.1", models.PkgRel(pkgrel="1.1")),
    ],
)
def test_version_get_pkgrel(value: str, expectation: models.PkgRel | None) -> None:
    """Tests for repod.common.models.Version.get_pkgrel."""
    assert models.Version(version=value).get_pkgrel() == expectation  # nosec: B101


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1.0.0-1", "1.0.0-1", 0),
        ("1.0.0-1", "1.0.0-2", -1),
        ("1.0.0-2", "1.0.0-1", 1),
        ("1.0.1-1", "1.0.0-1", 1),
        ("1.0.0-1", "1.0.1-1", -1),
        ("1:1.0.0-1", "1:1.0.0-1", 0),
        ("1:1.0.0-1", "1:1.0.0-2", -1),
        ("1:1.0.0-2", "1:1.0.0-1", 1),
        ("1:1.0.1-1", "1:1.0.0-1", 1),
        ("1:1.0.0-1", "1:1.0.1-1", -1),
        ("2:1.0.0-1", "1:1.0.0-1", 1),
        ("1:1.0.0-1", "2:1.0.1-1", -1),
        ("1:1.0.0-1", "1.0.0-1", 1),
        ("1.0.0-1", "1:1.0.0-1", -1),
    ],
)
@mark.parametrize("pyalpm_vercmp", [lf("pyalpm_vercmp_fun")])
def test_version_vercmp(subj: str, obj: str, expectation: int, pyalpm_vercmp: bool) -> None:
    """Tests for repod.common.models.Version.vercmp."""
    with patch("repod.version.alpm.PYALPM_VERCMP", pyalpm_vercmp):
        assert models.Version(version=subj).vercmp(version=models.Version(version=obj)) == expectation  # nosec: B101


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1.2.3-1", "1.2.3-2", True),
        ("1.2.3-2", "1.2.3-1", False),
    ],
)
def test_version_is_older_than(subj: str, obj: str, expectation: bool) -> None:
    """Tests for repod.common.models.Version.is_older_than."""
    assert models.Version(version=subj).is_older_than(version=models.Version(version=obj)) is expectation  # nosec: B101


@mark.parametrize(
    "subj, obj, expectation",
    [
        ("1.2.3-1", "1.2.3-2", False),
        ("1.2.3-2", "1.2.3-1", True),
    ],
)
def test_version_is_newer_than(subj: str, obj: str, expectation: bool) -> None:
    """Tests for repod.common.models.Version.is_newer_than."""
    assert models.Version(version=subj).is_newer_than(version=models.Version(version=obj)) is expectation  # nosec: B101
