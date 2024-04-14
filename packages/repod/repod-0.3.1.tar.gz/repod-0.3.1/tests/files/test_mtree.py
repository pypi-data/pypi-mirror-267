"""Tests for repod.files.mtree."""

from contextlib import nullcontext as does_not_raise
from io import StringIO
from logging import DEBUG
from pathlib import Path
from random import choice, randrange, sample
from re import Match, fullmatch
from string import ascii_lowercase, digits
from tempfile import TemporaryDirectory
from typing import ContextManager

from pydantic import ValidationError
from pytest import LogCaptureFixture, mark, raises

from repod.common.enums import tar_compression_types_for_filename_regex
from repod.errors import RepoManagementValidationError
from repod.files import mtree
from repod.files.common import extract_file_from_tarfile, open_tarfile


@mark.parametrize(
    "gid, expectation",
    [
        (randrange(0, 1000, 1), does_not_raise()),  # nosec: B311
        (randrange(1000, 65535, 1), raises(ValidationError)),  # nosec: B311
        (randrange(-65535, 0, 1), raises(ValidationError)),  # nosec: B311
    ],
)
def test_systemgid(gid: int, expectation: ContextManager[str]) -> None:
    """Tests for repod.files.mtree.SystemGID."""
    with expectation:
        mtree.SystemGID(gid=gid)


@mark.parametrize(
    "link, expectation",
    [
        (None, does_not_raise()),
        ("../foo/bar", does_not_raise()),
        ("/foo/bar", does_not_raise()),
        ("/foo/bar", does_not_raise()),
        ("äüö", raises(ValidationError)),
    ],
)
def test_linktarget(link: str | None, expectation: ContextManager[str]) -> None:
    """Tests for repod.files.mtree.LinkTarget."""
    with expectation:
        mtree.LinkTarget(link=link)


@mark.parametrize(
    "md5, expectation",
    [
        (None, does_not_raise()),
        ("".join(choice("abcdef" + digits) for x in range(32)), does_not_raise()),  # nosec: B311
        ("".join(choice("abcdef" + digits) for x in range(33)), raises(ValidationError)),  # nosec: B311
        ("".join(choice("abcdef" + digits) for x in range(31)), raises(ValidationError)),  # nosec: B311
        ("".join(choice(ascii_lowercase + digits) for x in range(32)), raises(ValidationError)),  # nosec: B311
    ],
)
def test_md5(md5: str | None, expectation: ContextManager[str]) -> None:
    """Tests for repod.files.mtree.Md5."""
    with expectation:
        mtree.Md5(md5=md5)


@mark.parametrize(
    "mode, expectation",
    [
        ("".join(choice("01234567") for x in range(3)), does_not_raise()),  # nosec: B311
        ("".join(choice("01234567") for x in range(4)), does_not_raise()),  # nosec: B311
        ("".join(choice("01234567") for x in range(2)), raises(ValidationError)),  # nosec: B311
        ("".join(choice("01234567") for x in range(5)), raises(ValidationError)),  # nosec: B311
        ("".join(choice("89") for x in range(3)), raises(ValidationError)),  # nosec: B311
        ("".join(choice("89") for x in range(4)), raises(ValidationError)),  # nosec: B311
    ],
)
def test_filemode(mode: str, expectation: ContextManager[str]) -> None:
    """Tests for repod.files.mtree.FileMode."""
    with expectation:
        mtree.FileMode(mode=mode)


@mark.parametrize(
    "sha256, expectation",
    [
        (None, does_not_raise()),
        ("".join(choice("abcdef" + digits) for x in range(64)), does_not_raise()),  # nosec: B311
        ("".join(choice("abcdef" + digits) for x in range(65)), raises(ValidationError)),  # nosec: B311
        ("".join(choice("abcdef" + digits) for x in range(63)), raises(ValidationError)),  # nosec: B311
        ("".join(choice(ascii_lowercase + digits) for x in range(64)), raises(ValidationError)),  # nosec: B311
    ],
)
def test_sha256(sha256: str | None, expectation: ContextManager[str]) -> None:
    """Tests for repod.files.mtree.Sha256."""
    with expectation:
        mtree.Sha256(sha256=sha256)


@mark.parametrize(
    "size, expectation",
    [
        (None, does_not_raise()),
        (randrange(0, 1000, 1), does_not_raise()),  # nosec: B311
        (randrange(-1000, 0, 1), raises(ValidationError)),  # nosec: B311
    ],
)
def test_filesize(size: int | None, expectation: ContextManager[str]) -> None:
    """Tests for repod.files.mtree.FileSize."""
    with expectation:
        mtree.FileSize(size=size)


@mark.parametrize(
    "time, expectation",
    [
        (1000.0, does_not_raise()),
        (-1000.0, raises(ValidationError)),
    ],
)
def test_unixtime(time: float, expectation: ContextManager[str]) -> None:
    """Tests for repod.files.mtree.UnixTime."""
    with expectation:
        mtree.UnixTime(time=time)


@mark.parametrize(
    "type_, expectation",
    [
        ("block", does_not_raise()),
        ("char", does_not_raise()),
        ("dir", does_not_raise()),
        ("fifo", does_not_raise()),
        ("file", does_not_raise()),
        ("link", does_not_raise()),
        ("socket", does_not_raise()),
        ("foo", raises(ValidationError)),
    ],
)
def test_mtreefiletype(type_: str, expectation: ContextManager[str]) -> None:
    """Tests for repod.files.mtree.MTreeEntryType."""
    with expectation:
        mtree.MTreeEntryType(type_=type_)


@mark.parametrize(
    "uid, expectation",
    [
        (randrange(0, 1000, 1), does_not_raise()),  # nosec: B311
        (randrange(1000, 65535, 1), raises(ValidationError)),  # nosec: B311
        (randrange(-65535, 0, 1), raises(ValidationError)),  # nosec: B311
    ],
)
def test_systemuid(uid: int, expectation: ContextManager[str]) -> None:
    """Tests for repod.files.mtree.SystemUID."""
    with expectation:
        mtree.SystemUID(uid=uid)


def test_mtreefile_get_file_path() -> None:
    """Tests for repod.files.mtree.MTreeEntry.get_file_path."""
    mtreefile = mtree.MTreeEntry()
    with raises(RuntimeError):
        mtreefile.get_file_path()


def test_mtreefile_get_link_path() -> None:
    """Tests for repod.files.mtree.MTreeEntry.get_link_path."""
    mtreefile = mtree.MTreeEntry()
    with raises(RuntimeError):
        mtreefile.get_link_path()


@mark.parametrize(
    "mtreefilev1, return_value",
    [
        (
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link=None,
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/foo\\040bar",
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            Path("/foo bar"),
        ),
        (
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link=None,
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/" + "".join(map(str, set(range(0x20, 0x7E)) - {ord("#"), ord(" "), ord("="), ord("\\")})),
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            Path("/" + "".join(map(str, set(range(0x20, 0x7E)) - {ord("#"), ord(" "), ord("="), ord("\\")}))),
        ),
        (
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link=None,
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/\\320\\220\\321\\202\\320\\273\\320\\260\\321\\201\\320\\275\\321\\213\\320\\265.svgz",
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            Path("/Атласные.svgz"),  # noqa: RUF001
        ),
    ],
)
def test_mtreefilev1_get_file_path(
    mtreefilev1: mtree.MTreeEntryV1, return_value: Path, caplog: LogCaptureFixture
) -> None:
    """Tests for repod.files.mtree.MTreeEntryV1.get_file_path."""
    caplog.set_level(DEBUG)
    assert mtreefilev1.get_file_path() == return_value  # nosec: B101


@mark.parametrize(
    "resolve, mtreefilev1, return_value",
    [
        (
            False,
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link="/bar\\040baz",
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/foo\\040bar",
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            Path("/bar baz"),
        ),
        (
            False,
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link="bar\\040baz",
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/foo\\040bar",
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            Path("bar baz"),
        ),
        (
            False,
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link="../bar\\040baz",
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/foo/bar/baz",
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            Path("../bar baz"),
        ),
        (
            True,
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link="/bar\\040baz",
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/foo\\040bar",
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            Path("/bar baz"),
        ),
        (
            True,
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link="bar\\040baz",
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/foo\\040bar",
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            Path("/bar baz"),
        ),
        (
            True,
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link="../bar\\040baz",
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/foo/bar/baz",
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            Path("/foo/bar/bar baz"),
        ),
        (
            True,
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link="../\\320\\220\\321\\202\\320\\273\\320\\260\\321\\201\\320\\275\\321\\213\\320\\265.svgz",
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/foo/bar/baz",
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            Path("/foo/bar/Атласные.svgz"),  # noqa: RUF001
        ),
        (
            False,
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link="/foo",
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/foo/bar/baz",
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            Path("/foo"),
        ),
        (
            False,
            mtree.MTreeEntryV1(
                mode="0644",
                size=1000,
                link=None,
                md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
                name="/foo\\040bar",
                type_="file",
                sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
                time=200,
                gid=0,
                uid=0,
            ),
            None,
        ),
    ],
)
def test_mtreefilev1_get_link_path(resolve: bool, mtreefilev1: mtree.MTreeEntryV1, return_value: Path) -> None:
    """Tests for repod.files.mtree.MTreeEntryV1.get_link_path."""
    assert mtreefilev1.get_link_path(resolve=resolve) == return_value  # nosec: B101


def test_mtreefile_get_type() -> None:
    """Tests for repod.files.mtree.MTreeEntry.get_type."""
    mtreefile = mtree.MTreeEntry()
    with raises(RuntimeError):
        mtreefile.get_type()


def test_mtreefilev1_get_type() -> None:
    """Tests for repod.files.mtree.MTreeEntryV1.get_type."""
    assert (  # nosec: B101
        mtree.MTreeEntryV1(
            mode="0644",
            size=1000,
            link=None,
            md5="".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
            name="/foo\\040bar",
            type_="file",
            sha256="".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
            time=200,
            gid=0,
            uid=0,
        ).get_type()
        == "file"
    )


def test_mtree_get_paths(valid_mtree: mtree.MTree) -> None:
    """Tests for repod.files.mtree.MTreeEntryV1.get_paths."""
    assert valid_mtree.get_paths()  # nosec: B101


@mark.parametrize("valid, expectation", [(True, does_not_raise()), (False, raises(RepoManagementValidationError))])
def test_mtree_from_file(
    valid: bool,
    expectation: ContextManager[str],
    mtreeentryv1_stringio: StringIO,
    invalid_mtreeentryv1_stringio: StringIO,
    caplog: LogCaptureFixture,
) -> None:
    """Tests for repod.files.mtree.MTree.from_file."""
    caplog.set_level(DEBUG)

    if valid:
        data = mtreeentryv1_stringio
    else:
        data = invalid_mtreeentryv1_stringio

    with expectation:
        assert isinstance(mtree.MTree.from_file(data=data), mtree.MTree)  # nosec: B101


def test_export_schemas() -> None:
    """Tests for repod.files.mtree.export_schemas."""
    with TemporaryDirectory() as tmp:
        mtree.export_schemas(output=str(tmp))
        mtree.export_schemas(output=tmp)

    with raises(RuntimeError):
        mtree.export_schemas(output="/foobar")

    with raises(RuntimeError):
        mtree.export_schemas(output=Path("/foobar"))


@mark.integration
@mark.skipif(
    not Path("/var/cache/pacman/pkg/").exists(),
    reason="Package cache in /var/cache/pacman/pkg/ does not exist",
)
async def test_read_mtree_files() -> None:
    """Integration tests for repod.files.mtree.MTree.from_file."""
    packages = sorted(
        [
            path
            for path in list(Path("/var/cache/pacman/pkg/").iterdir())
            if isinstance(fullmatch(rf"^.*\.pkg\.tar({tar_compression_types_for_filename_regex()})$", str(path)), Match)
        ]
    )
    if len(packages) > 50:
        packages = sample(packages, 50)
    for package in packages:
        assert isinstance(  # nosec: B101
            mtree.MTree.from_file(
                await extract_file_from_tarfile(  # type: ignore[arg-type]
                    tarfile=open_tarfile(package),
                    file=".MTREE",
                    as_stringio=True,
                    gzip_compressed=True,
                )
            ),
            mtree.MTree,
        )
