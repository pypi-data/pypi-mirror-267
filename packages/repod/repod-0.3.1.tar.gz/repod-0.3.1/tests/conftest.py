"""Pytest conftest."""

import gzip
import sys
from copy import deepcopy
from io import BytesIO, StringIO
from logging import DEBUG, debug
from os import chdir
from pathlib import Path
from random import choice
from string import ascii_lowercase, ascii_uppercase, digits
from tarfile import open as tarfile_open
from tempfile import NamedTemporaryFile, TemporaryDirectory
from textwrap import dedent
from typing import IO, Any, AsyncGenerator, Generator
from unittest.mock import Mock, patch

import orjson
import pytest_asyncio
from pydantic import BaseModel
from pytest import LogCaptureFixture, fixture

from repod.common.enums import (
    ArchitectureEnum,
    CompressionTypeEnum,
    FilesVersionEnum,
    PackageDescVersionEnum,
    PkgTypeEnum,
)
from repod.config.settings import (
    DEFAULT_ARCHITECTURE,
    DEFAULT_DATABASE_COMPRESSION,
    DEFAULT_NAME,
    ArchiveSettings,
    ManagementRepo,
    PackageRepo,
    UserSettings,
)
from repod.files import open_tarfile
from repod.files.buildinfo import BuildInfo, BuildInfoV1, BuildInfoV2
from repod.files.common import ZstdTarFile
from repod.files.mtree import MTree, MTreeEntryV1
from repod.files.package import PackageV1, PackageV2
from repod.files.pkginfo import PkgInfo, PkgInfoV1, PkgInfoV2, PkgType
from repod.repo.management import OutputBuildInfo, OutputPackageBase
from repod.repo.management.outputpackage import OutputPackageBaseV1, OutputPackageV1
from repod.repo.package import Files, PackageDesc, RepoDbTypeEnum
from repod.repo.package.repofile import relative_to_shared_base
from repod.repo.package.syncdb import (
    FilesV1,
    PackageDescV1,
    PackageDescV2,
    SyncDatabase,
)


class SchemaVersion9999(BaseModel):
    """An invalid SchemaVersion."""

    schema_version: int = 9999


class BuildInfoV9999(BuildInfo, SchemaVersion9999):
    """An invalid BuildInfo."""

    pass


class FilesV9999(Files, SchemaVersion9999):
    """An invalid Files."""

    pass


class OutputPackageBaseV9999(OutputPackageBase, SchemaVersion9999):
    """An invalid OutputPackageBase."""

    pass


class PackageDescV9999(PackageDesc, SchemaVersion9999):
    """An invalid PackageDesc."""

    pass


def create_default_arch() -> str:
    """Return a (pseudo-randomly selected) ArchitectureEnum as string."""
    return str(choice([arch.value for arch in ArchitectureEnum]))  # nosec: B311


@fixture(scope="session")
def default_arch() -> str:
    """Return a session-wide (pseudo-randomly selected) ArchitectureEnum as string."""
    return create_default_arch()


def create_base64_pgpsig() -> str:
    """Return a fake base64 encoded PGP signature string."""
    return "".join(choice(ascii_uppercase + ascii_lowercase + digits + "/+") for x in range(400)) + "=="  # nosec: B311


@fixture(scope="session")
def base64_pgpsig() -> str:
    """Return a session-wide fake base64 encoded PGP signature string."""
    return create_base64_pgpsig()


def create_default_buildenv() -> str:
    """Return a dummy repod.files.buildinfo.BuildEnv string."""
    return "foo"


@fixture(scope="session")
def default_buildenv() -> str:
    """Return a session-wide dummy repod.files.buildinfo.BuildEnv string."""
    return create_default_buildenv()


def create_default_invalid_buildenv() -> str:
    """Return an invalid repod.files.buildinfo.BuildEnv string."""
    return "! foo"


@fixture(scope="session")
def default_invalid_buildenv() -> str:
    """Return a session-wide invalid repod.files.buildinfo.BuildEnv string."""
    return create_default_invalid_buildenv()


def create_default_description() -> str:
    """Return a dummy description string."""
    return "description"


@fixture(scope="session")
def default_description() -> str:
    """Return a session-wide dummy description string."""
    return create_default_description()


def create_default_filename() -> str:
    """Return a dummy package filename string."""
    return f"foo-{create_default_full_version()}-any.pkg.tar.zst"


@fixture(scope="session")
def default_filename() -> str:
    """Return a session-wide dummy package filename string."""
    return create_default_filename()


def create_default_license() -> str:
    """Return a dummy license string."""
    return "GPL"


@fixture(scope="session")
def default_license() -> str:
    """Return a session-wide dummy license string."""
    return create_default_license()


def create_default_full_version() -> str:
    """Return a version string (including epoch, pkgver and pkgrel)."""
    return "1:1.0.0-1"


@fixture(scope="session")
def default_full_version() -> str:
    """Return a session-wide version string (including epoch, pkgver and pkgrel)."""
    return create_default_full_version()


def create_default_invalid_full_version() -> str:
    """Return an invalid version string."""
    return "0:1/0-0.1"


@fixture(scope="function")
def default_invalid_full_version() -> str:
    """Return a session-wide invalid version string."""
    return create_default_invalid_full_version()


def create_default_option() -> str:
    """Return a dummy option string."""
    return "foo"


@fixture(scope="session")
def default_option() -> str:
    """Return a session-wide dummy option string."""
    return create_default_option()


def create_default_invalid_option() -> str:
    """Return an invalid option string."""
    return "! foo"


@fixture(scope="function")
def default_invalid_option() -> str:
    """Return a session-wide invalid option string."""
    return create_default_invalid_option()


def create_default_package_name() -> str:
    """Return a dummy package name string."""
    return "foo"


@fixture(scope="session")
def default_package_name() -> str:
    """Return a session-wide dummy package name string."""
    return create_default_package_name()


def create_default_invalid_package_name() -> str:
    """Return an invalid package name string."""
    return ".foo"


@fixture(scope="session")
def default_invalid_package_name() -> str:
    """Return a session-wide invalid package name string."""
    return create_default_invalid_package_name()


def create_default_packager() -> str:
    """Return a dummy packager string."""
    return "Foobar McFooface <foobar@archlinux.org>"


@fixture(scope="session")
def default_packager() -> str:
    """Return a session-wide dummy packager string."""
    return create_default_packager()


def create_default_invalid_packager() -> str:
    """Return an invalid packager string."""
    return "Foobar McFooface <foo>"


@fixture(scope="session")
def default_invalid_packager() -> str:
    """Return a session-wide invalid packager string."""
    return create_default_invalid_packager()


@fixture(scope="session")
def default_pkgtype() -> str:
    """Return a session-wide pkgtype string."""
    return "pkg"


@fixture(scope="session")
def default_invalid_pkgtype() -> str:
    """Return a session-wide invalid pkgtype string."""
    return "foo"


def create_url() -> str:
    """Return a dummy URL string."""
    return "https://foobar.tld"


@fixture(scope="session")
def url() -> str:
    """Return a session-wide dummy URL string."""
    return create_url()


@fixture(scope="session")
def default_version() -> str:
    """Return a session-wide version (pkgver) string."""
    return "1.0.0"


@fixture(scope="session")
def default_invalid_version() -> str:
    """Return a session-wide invalid version (pkgver) string."""
    return "-1.0.0"


@fixture(
    scope="session",
    params=[arch.value for arch in ArchitectureEnum],
)
def arch(request: Any) -> str:
    """Return all available ArchitectureEnum members session-wide as string."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "foo",
        "!foo",
        "!1234",
        "foo123",
        "foo-123",
        "foo.123",
        "foo_",
    ],
)
def buildenv(request: Any) -> str:
    """Return a set of valid buildenv strings session-wide."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "",
        "!",
        "! foo",
    ],
)
def invalid_buildenv(request: Any) -> str:
    """Return a set of invalid buildenv strings session-wide."""
    return str(request.param)


@fixture(
    scope="session",
    params=[name.value for name in CompressionTypeEnum],
)
def compression_type(request: Any) -> str:
    """Return all members of CompressionTypeEnum session-wide as string."""
    return str("." + request.param if request.param else request.param)


@fixture(
    scope="session",
    params=[
        ".foo",
        "_foo",
    ],
)
def invalid_compression_type(request: Any) -> str:
    """Return a set of invalid compression types session-wide as string."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "foobar@mcfooface.tld",
        "foo.bar@mcfooface.tld",
        "foo.bar@mc-fooface.tld",
        "foo_bar@mc-fooface.tld",
        "foo_bar@mc.fooface.tld",
        "foo-bar@mc.fooface.tld",
        "foobar@mcfooface.tld-foo",
    ],
)
def email(request: Any) -> str:
    """Return a set of valid email address strings session-wide."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "foo",
        "@mcfooface.tld",
        "foobar@.tld",
        "foobar@mcfooface.",
        "foobar@mcfooface",
        "foobar@@mcfooface.tld",
    ],
)
def invalid_email(request: Any) -> str:
    """Return a set of invalid email address strings session-wide."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "1:",
        "10:",
        "100:",
    ],
)
def epoch(request: Any) -> str:
    """Return a set of valid epoch strings session-wide."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "0:",
        "1",
        ":1",
    ],
)
def invalid_epoch(request: Any) -> str:
    """Return a set of invalid epoch strings session-wide."""
    return str(request.param)


def create_md5sum() -> str:
    """Return a dummy MD5 string."""
    return "".join(choice("abcdef" + digits) for x in range(32))  # nosec: B311


@fixture(scope="session")
def md5sum() -> str:
    """Return a session-wide dummy MD5 string."""
    return create_md5sum()


@fixture(
    scope="session",
    params=[
        "foo",
        "!foo",
        "!1234",
        "foo123",
        "foo-123",
        "foo.123",
        "foo_",
    ],
)
def option(request: Any) -> str:
    """Return string session-wide from a set of valid option strings."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "",
        "!",
        "! foo",
    ],
)
def invalid_option(request: Any) -> str:
    """Return string session-wide from a set of invalid option strings."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "foo",
        "_foo",
        "@foo",
        "+foo",
        "foo.+_-123",
    ],
)
def package_name(request: Any) -> str:
    """Return string session-wide from a set of valid package name strings."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "foo!",
        "",
        ".foo",
        "-foo",
        "fo,o",
        "fo*o",
    ],
)
def invalid_package_name(request: Any) -> str:
    """Return string session-wide from a set of invalid package name strings."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "1",
        "10",
        "1.1",
        "1.10",
        "10.10",
    ],
)
def pkgrel(request: Any) -> str:
    """Return string session-wide from a set of valid pkgrel strings."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "0",
        "1.0",
        "0.1",
        "",
    ],
)
def invalid_pkgrel(request: Any) -> str:
    """Return string session-wide from a set of invalid pkgrel strings."""
    return str(request.param)


@fixture(
    scope="session",
    params=[pkgtype.value for pkgtype in PkgTypeEnum],
)
def pkgtype(request: Any) -> str:
    """Return string session-wide from the set of PkgTypeEnum values."""
    return str(request.param)


@fixture(scope="session")
def invalid_pkgtype() -> str:
    """Return invalid pkgtype string session-wide."""
    return "foo"


@fixture(
    scope="session",
    params=[
        "Foobar",
        "Foobar McFooface",
        "Foobar Mc-Fooface",
        "Foobar McFooface (The great Bar)",
        "Foobar McFooface (The great Bar..)",
        "Foobar McFooface (The 1st)",
        "foo",
    ],
)
def packager_name(request: Any) -> str:
    """Return string session-wide from a set of valid packager name strings."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "",
        "Foobar!",
        "Foobar, McFooface",
    ],
)
def invalid_packager_name(request: Any) -> str:
    """Return string session-wide from a set of invalid packager name strings."""
    return str(request.param)


def create_sha256sum() -> str:
    """Return dummy SHA-256 sum string."""
    return "".join(choice("abcdef" + digits) for x in range(64))  # nosec: B311


@fixture(scope="session")
def sha256sum() -> str:
    """Return session-wide dummy SHA-256 sum string."""
    return create_sha256sum()


@fixture(scope="session")
def signature() -> str:
    """Return session-wide signature file suffix string."""
    return ".sig"


@fixture(scope="session")
def invalid_signature() -> str:
    """Return session-wide invalid signature file suffix string."""
    return ".foo"


@fixture(
    scope="session",
    params=[
        "0.0.1",
        "0_0_1",
        "0+0+1",
        "0.1.0",
        "1.0.0",
        "1.0.0.0.0.1",
        "abc1.0.0",
        "1.0.abc",
        "0",
        "1.",
        "1..",
        "foo",
    ],
)
def version(request: Any) -> str:
    """Return string session-wide from a set of valid version strings."""
    return str(request.param)


@fixture(
    scope="session",
    params=[
        "-1",
        "1 0",
        "1-0",
        "1/0",
    ],
)
def invalid_version(request: Any) -> str:
    """Return string session-wide from a set of invalid version strings."""
    return str(request.param)


@fixture(scope="function")
def mtreeentryv1_stringio() -> Generator[StringIO, None, None]:
    """Yield MTreeEntryV1 in a StringIO function-wide."""
    mtree_contents = """
        #mtree
        /set type=file uid=0 gid=0 mode=644
        ./.BUILDINFO time=1651787473.0 size=5651 md5digest=f712adf35b8a74755b3a93997b05793c \
        sha256digest=ed4e5855da200753eaf00cd584f017bef6910c09f70d72e4a642515312919804
        ./.INSTALL time=1651787473.0 size=808 md5digest=d96cc20315471e332a06c4261590b505 \
        sha256digest=96fc0c8b3aa4011de41c9dd1ba95e63bf2e9767daa801c14bea1d57359baf307
        ./.PKGINFO time=1651787473.0 size=1689 md5digest=76ff63a0094096fabe790fb35daadf79 \
        sha256digest=e15a57a4ddb0fa9feddbe410f395524b25be345d17f75f5f2ccc273034d388bc
        /set mode=755
        ./etc time=1651787473.0 type=dir
        ./etc/foo time=1651787473.0 type=dir
        ./etc/foo/foo.conf time=1651787473.0 mode=644 size=2761 md5digest=c6e1c562468738e93335f2e2ce314e8b \
        sha256digest=87d2b2075fbb24eb1108fed7ef9f2971d7954ae0894b1405425a04ff9e1df49e
        ./etc/foo/bar.conf time=1651787473.0 mode=44 size=2761 md5digest=c6e1c562468738e93335f2e2ce314e8b \
        sha256digest=87d2b2075fbb24eb1108fed7ef9f2971d7954ae0894b1405425a04ff9e1df49e
        /set time=1651787473.0
        ./etc/foo.conf.d type=dir
        ./usr type=dir
        ./usr/share type=dir
        ./usr/share/foo type=dir
        ./usr/share/foo/conf type=dir
        ./usr/share/foo/conf/override.conf time=1651787476.0 mode=777 type=link link=/etc/foo.conf.d/override.conf
        /set mode=66
        ./usr/share/foo/conf/foo.conf size=2761 md5digest=c6e1c562468738e93335f2e2ce314e8b \
        sha256digest=87d2b2075fbb24eb1108fed7ef9f2971d7954ae0894b1405425a04ff9e1df49e
        ./usr/share/foo/conf/bar.conf size=2761 md5digest=c6e1c562468738e93335f2e2ce314e8b \
        sha256digest=87d2b2075fbb24eb1108fed7ef9f2971d7954ae0894b1405425a04ff9e1df49e
        """

    yield StringIO(initial_value=dedent(mtree_contents).strip())


@fixture(
    scope="function",
    params=[
        (
            """
            #mtree
            /set type=file uid=0 gid=2000 mode=644
            ./.BUILDINFO time=1651787473.0 size=5651 md5digest=f712adf35b8a74755b3a93997b05793c \
                    sha256digest=ed4e5855da200753eaf00cd584f017bef6910c09f70d72e4a642515312919804
            """
        ),
        (
            """
            #mtree
            /set type=file uid=0 gid=0 mode=644
            ./.BUILDINFO time=1651787473.0 mode=777 type=link link=/.PKGINFÖ
            """
        ),
        (
            """
            #mtree
            /set type=file uid=0 gid=0 mode=644
            ./.BUILDINFO time=1651787473.0 size=5651 md5digest=df35b8a74755b3a93997b05793c \
                    sha256digest=ed4e5855da200753eaf00cd584f017bef6910c09f70d72e4a642515312919804
            """
        ),
        (
            """
            #mtree
            /set type=file uid=0 gid=0 mode=79878
            ./.BUILDINFO time=1651787473.0 size=5651 md5digest=f712adf35b8a74755b3a93997b05793c \
                    sha256digest=ed4e5855da200753eaf00cd584f017bef6910c09f70d72e4a642515312919804
            """
        ),
        (
            """
            #mtree
            /set type=file uid=0 gid=0 mode=644
            ./.BUILDINFÖ time=1651787473.0 size=5651 md5digest=f712adf35b8a74755b3a93997b05793c \
                    sha256digest=ed4e5855da200753eaf00cd584f017bef6910c09f70d72e4a642515312919804
            """
        ),
        (
            """
            #mtree
            /set type=file uid=0 gid=0 mode=644
            ./.BUILDINFO time=1651787473.0 size=5651 md5digest=f712adf35b8a74755b3a93997b05793c \
                    sha256digest=ed4e5855da200753eaf00cd584f017bef6910c09f70d72e4a6425153129
            """
        ),
        (
            """
            #mtree
            /set type=file uid=0 gid=0 mode=644
            ./.BUILDINFO time=1651787473.0 size=-1 md5digest=f712adf35b8a74755b3a93997b05793c \
                sha256digest=ed4e5855da200753eaf00cd584f017bef6910c09f70d72e4a642515312919804
            """
        ),
        (
            """
            #mtree
            /set type=file uid=0 gid=0 mode=644
            ./.BUILDINFO time=-1 size=5651 md5digest=f712adf35b8a74755b3a93997b05793c \
                sha256digest=ed4e5855da200753eaf00cd584f017bef6910c09f70d72e4a642515312919804
            """
        ),
        (
            """
            #mtree
            /set type=foo uid=0 gid=0 mode=644
            ./.BUILDINFO time=1651787473.0 size=5651 md5digest=f712adf35b8a74755b3a93997b05793c \
                sha256digest=ed4e5855da200753eaf00cd584f017bef6910c09f70d72e4a642515312919804
            """
        ),
        (
            """
            #mtree
            /set type=file uid=2000 gid=0 mode=644
            ./.BUILDINFO time=1651787473.0 size=5651 md5digest=f712adf35b8a74755b3a93997b05793c \
                sha256digest=ed4e5855da200753eaf00cd584f017bef6910c09f70d72e4a642515312919804
            """
        ),
    ],
    ids=[
        "invalid_gid",
        "invalid_link",
        "invalid_md5",
        "invalid_mode",
        "invalid_name",
        "invalid_sha256",
        "invalid_size",
        "invalid_time",
        "invalid_type",
        "invalid_uid",
    ],
)
def invalid_mtreeentryv1_stringio(request: Any) -> Generator[StringIO, None, None]:
    """Yield invalid MTreeEntryV1 in a StringIO function-wide from a set of invalid string inputs."""
    entry = dedent(request.param).strip()
    print(entry)
    yield StringIO(initial_value=entry)


@fixture(scope="function")
def mtreeentryv1_internals() -> Generator[list[MTreeEntryV1], None, None]:
    """Yield list of MTreeEntryV1 representing the required internal package files."""
    base = {
        "gid": 0,
        "link": None,
        "md5": "".join(choice("abcdef" + digits) for x in range(32)),  # nosec: B311
        "mode": "0644",
        "sha256": "".join(choice("abcdef" + digits) for x in range(64)),  # nosec: B311
        "time": 1000,
        "type_": "file",
        "uid": 0,
    }

    yield [
        MTreeEntryV1(name=name, **base)  # type: ignore[arg-type]
        for name in ["/.BUILDINFO", "/.INSTALL", "/.MTREE", "/.PKGINFO"]
    ]


@fixture(scope="function")
def mtreeentryv1_dir(md5sum: str, sha256sum: str) -> Generator[MTreeEntryV1, None, None]:
    """Yield an MTreeEntryV1 function-wide representing a directory."""
    yield MTreeEntryV1(
        gid=0,
        link=None,
        md5=md5sum,
        mode="0755",
        name="/foo/dir",
        sha256=sha256sum,
        time=1000,
        type_="dir",
        uid=0,
    )


@fixture(scope="function")
def mtreeentryv1_file(md5sum: str, sha256sum: str) -> Generator[MTreeEntryV1, None, None]:
    """Yield an MTreeEntryV1 function-wide representing a file."""
    yield MTreeEntryV1(
        gid=0,
        link=None,
        md5=md5sum,
        mode="0644",
        name="/foo/file",
        sha256=sha256sum,
        time=1000,
        type_="file",
        uid=0,
    )


@fixture(scope="function")
def mtreeentryv1_link(md5sum: str, sha256sum: str) -> Generator[MTreeEntryV1, None, None]:
    """Yield an MTreeEntryV1 function-wide representing a symlink."""
    yield MTreeEntryV1(
        gid=0,
        link="/foo/target",
        md5=md5sum,
        mode="0777",
        name="/foo/link",
        sha256=sha256sum,
        time=1000,
        type_="link",
        uid=0,
    )


@fixture(scope="function")
def valid_mtree(
    mtreeentryv1_dir: MTreeEntryV1,
    mtreeentryv1_file: MTreeEntryV1,
    mtreeentryv1_link: MTreeEntryV1,
    mtreeentryv1_internals: list[MTreeEntryV1],
) -> Generator[MTree, None, None]:
    """Yield an MTree function-wide representing a set of files and directories."""
    yield MTree(
        entries=[  # type: ignore[arg-type]
            mtreeentryv1_dir,
            mtreeentryv1_file,
            mtreeentryv1_link,
        ]
        + mtreeentryv1_internals,
    )


@fixture(scope="function")
def valid_mtree_file(mtreeentryv1_stringio: StringIO, tmp_path: Path) -> Generator[Path, None, None]:
    """Yield the Path to an mtree file function-wide."""
    with NamedTemporaryFile(prefix="mtree_", dir=tmp_path, delete=False) as mtree_file:
        with gzip.open(filename=mtree_file.name, mode="wt") as gzip_mtree:
            gzip_mtree.write(mtreeentryv1_stringio.getvalue())

    yield Path(mtree_file.name)


@fixture(scope="function")
def valid_mtree_bytesio(valid_mtree_file: Path) -> Generator[IO[bytes], None, None]:
    """Yield a bytes stream function-wide representing MTree data."""
    with open(valid_mtree_file, mode="rb") as gzip_mtree:
        yield BytesIO(gzip_mtree.read())


@fixture(scope="function")
def packagev1(
    default_filename: str,
    md5sum: str,
    sha256sum: str,
    valid_buildinfov1: BuildInfo,
    valid_mtree: MTree,
    valid_pkginfov1: PkgInfo,
) -> PackageV1:
    """Return a PackageV1 using BuildInfoV1 and PkgInfoV1."""
    return PackageV1(
        buildinfo=valid_buildinfov1,
        csize=1,
        filename=default_filename,
        md5sum=md5sum,
        mtree=valid_mtree,
        pkginfo=valid_pkginfov1,
        sha256sum=sha256sum,
    )


@fixture(scope="function")
def packagev2(
    default_filename: str,
    sha256sum: str,
    valid_buildinfov1: BuildInfo,
    valid_mtree: MTree,
    valid_pkginfov1: PkgInfo,
) -> PackageV2:
    """Return a PackageV2 using BuildInfoV1 and PkgInfoV1."""
    return PackageV2(
        buildinfo=valid_buildinfov1,
        csize=1,
        filename=default_filename,
        mtree=valid_mtree,
        pkginfo=valid_pkginfov1,
        sha256sum=sha256sum,
    )


@fixture(scope="function")
def packagev1_pkginfov2(
    default_filename: str,
    md5sum: str,
    sha256sum: str,
    valid_buildinfov1: BuildInfo,
    valid_mtree: MTree,
    valid_pkginfov2: PkgInfo,
) -> PackageV1:
    """Return a PackageV1 using BuildInfoV1 and PkgInfoV2."""
    return PackageV1(
        buildinfo=valid_buildinfov1,
        csize=1,
        filename=default_filename,
        md5sum=md5sum,
        mtree=valid_mtree,
        pkginfo=valid_pkginfov2,
        sha256sum=sha256sum,
    )


@fixture(scope="function")
def text_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Yield the Path to a dummy text file function-wide."""
    with NamedTemporaryFile(prefix="pkg_content_", dir=tmp_path, suffix=".txt", delete=False) as temp_file:
        with open(temp_file.name, "w") as f:
            print("foo", file=f)

    yield Path(temp_file.name)


@fixture(scope="function")
def bz2_file(text_file: Path) -> Generator[Path, None, None]:
    """Yield the Path to a bzip2 compressed file containing a dummy text file function-wide."""
    with TemporaryDirectory() as tmp_path:
        with NamedTemporaryFile(dir=tmp_path, suffix=".bz2", delete=False) as tarfile:
            with tarfile_open(tarfile.name, mode="w:bz2") as compressed_tarfile:
                compressed_tarfile.add(text_file.parent)
                compressed_tarfile.add(text_file)

        yield Path(tarfile.name)


@fixture(scope="function")
def gz_file(text_file: Path) -> Generator[Path, None, None]:
    """Yield the Path to a gzip compressed file containing a dummy text file function-wide."""
    with TemporaryDirectory() as tmp_path:
        with NamedTemporaryFile(dir=tmp_path, suffix=".gz", delete=False) as tarfile:
            with tarfile_open(tarfile.name, mode="w:gz") as compressed_tarfile:
                compressed_tarfile.add(text_file.parent)
                compressed_tarfile.add(text_file)

        yield Path(tarfile.name)


@fixture(scope="function")
def tar_file(text_file: Path) -> Generator[Path, None, None]:
    """Yield the Path to a tar bundled file containing a dummy text file function-wide."""
    with TemporaryDirectory() as tmp_path:
        with NamedTemporaryFile(dir=tmp_path, suffix=".tar", delete=False) as tarfile:
            with tarfile_open(tarfile.name, mode="w:") as uncompressed_tarfile:
                uncompressed_tarfile.add(text_file.parent)
                uncompressed_tarfile.add(text_file)

        yield Path(tarfile.name)


@fixture(scope="function")
def xz_file(text_file: Path) -> Generator[Path, None, None]:
    """Yield the Path to a xz compressed file containing a dummy text file function-wide."""
    with TemporaryDirectory() as tmp_path:
        with NamedTemporaryFile(dir=tmp_path, suffix=".xz", delete=False) as tarfile:
            with tarfile_open(tarfile.name, mode="w:xz") as compressed_tarfile:
                compressed_tarfile.add(text_file.parent)
                compressed_tarfile.add(text_file)

        yield Path(tarfile.name)


@fixture(scope="function")
def zst_file(text_file: Path) -> Generator[Path, None, None]:
    """Yield the Path to a zstd compressed file containing a dummy text file function-wide."""
    with TemporaryDirectory() as tmp_path:
        with NamedTemporaryFile(dir=tmp_path, suffix=".zst", delete=False) as tarfile:
            with ZstdTarFile(tarfile.name, mode="w") as compressed_tarfile:
                compressed_tarfile.add(text_file.parent)
                compressed_tarfile.add(text_file)

        yield Path(tarfile.name)


@fixture(scope="session")
def epoch_version_pkgrel(epoch: str, version: str, pkgrel: str) -> str:
    """Return a version string session-wide, representing all valid permutations of epoch, pkgver and pkgrel."""
    return f"{epoch}{version}-{pkgrel}"


@fixture(scope="session")
def invalid_epoch_version_pkgrel(invalid_epoch: str, invalid_version: str, invalid_pkgrel: str) -> str:
    """Return a version string session-wide, representing all invalid permutations of epoch, pkgver and pkgrel."""
    return f"{invalid_epoch}{invalid_version}-{invalid_pkgrel}"


@fixture(scope="function")
def buildinfov1_stringio(
    default_packager: str,
    sha256sum: str,
) -> Generator[StringIO, None, None]:
    """Yield a StringIO function-wide representing valid BuildInfoV1 data."""
    buildinfov1_contents = f"""format = 1
        pkgname = foo
        pkgbase = bar
        pkgver = 1:1.0.0-1
        pkgarch = any
        pkgbuild_sha256sum = {sha256sum}
        packager = {default_packager}
        builddate = 1
        builddir = /build
        buildenv = check
        buildenv = color
        options = debug
        options = strip
        installed = baz-1:1.0.1-1-any
        installed = beh-1:1.0.1-1-any
        """

    yield StringIO(initial_value=dedent(buildinfov1_contents).strip())


@fixture(scope="function")
def buildinfov2_stringio(
    default_packager: str,
    sha256sum: str,
) -> Generator[StringIO, None, None]:
    """Yield a StringIO function-wide representing valid BuildInfoV2 data."""
    buildinfov1_contents = f"""format = 2
        pkgname = foo
        pkgbase = bar
        pkgver = 1:1.0.0-1
        pkgarch = any
        pkgbuild_sha256sum = {sha256sum}
        packager = {default_packager}
        builddate = 1
        builddir = /build
        startdir = /startdir
        buildtool = buildtool
        buildtoolver = 1:1.0.1-1-any
        buildenv = check
        buildenv = color
        options = debug
        options = strip
        installed = baz-1:1.0.1-1-any
        installed = beh-1:1.0.1-1-any
        """

    yield StringIO(initial_value=dedent(buildinfov1_contents).strip())


@fixture(scope="function")
def valid_buildinfov1_file(buildinfov1_stringio: StringIO) -> Generator[Path, None, None]:
    """Yield the Path to a file function-wide representing valid BuildInfoV1 data."""
    with NamedTemporaryFile() as buildinfo_file:
        with open(buildinfo_file.name, mode="wt") as f:
            print(buildinfov1_stringio.getvalue(), file=f)

        yield Path(buildinfo_file.name)


@fixture(scope="function")
def valid_buildinfov2_file(buildinfov2_stringio: StringIO, tmp_path: Path) -> Generator[Path, None, None]:
    """Yield the Path to a file function-wide representing valid BuildInfoV2 data."""
    with NamedTemporaryFile(prefix="buildinfov2_", dir=tmp_path, delete=False) as buildinfo_file:
        with open(buildinfo_file.name, mode="wt") as f:
            print(buildinfov2_stringio.getvalue(), file=f)

    yield Path(buildinfo_file.name)


@fixture(scope="session")
def default_installed() -> list[str]:
    """Return a list of strings session-wide, representing repod.files.buildinfo.Installed entries."""
    return ["build_foo-1:1.0.1-1-any", "build_bar-1:1.0.1-1-any"]


@fixture(scope="session")
def valid_buildinfov1(
    default_arch: str,
    default_buildenv: str,
    default_full_version: str,
    default_installed: list[str],
    default_option: str,
    default_packager: str,
    sha256sum: str,
    url: str,
) -> BuildInfo:
    """Return a BuildInfoV1 session-wide."""
    return BuildInfoV1(
        builddate=1,
        builddir="/build",
        buildenv=[default_buildenv],
        installed=default_installed,
        options=[default_option],
        packager=default_packager,
        pkgarch=default_arch,
        pkgbase="foo",
        pkgbuild_sha256sum=sha256sum,
        pkgname="foo",
        pkgver=default_full_version,
        schema_version=1,
    )


@fixture(scope="session")
def valid_buildinfov2(
    default_arch: str,
    default_buildenv: str,
    default_full_version: str,
    default_installed: list[str],
    default_option: str,
    default_packager: str,
    sha256sum: str,
    url: str,
) -> BuildInfo:
    """Return a BuildInfoV2 session-wide."""
    return BuildInfoV2(
        builddate=1,
        builddir="/build",
        buildenv=[default_buildenv],
        buildtool="buildtool",
        buildtoolver=default_full_version,
        installed=default_installed,
        options=[default_option],
        packager=default_packager,
        pkgarch=default_arch,
        pkgbase="foo",
        pkgbuild_sha256sum=sha256sum,
        pkgname="foo",
        pkgver=default_full_version,
        schema_version=2,
        startdir="/startdir",
    )


@fixture(scope="function")
def pkginfov1_stringio(
    default_arch: str,
    default_description: str,
    default_full_version: str,
    default_license: str,
    default_package_name: str,
    default_packager: str,
    default_version: str,
    url: str,
) -> Generator[StringIO, None, None]:
    """Yield a StringIO function-wide representing PkgInfoV1 data."""
    file_data = f"""# Generated by makepkg {default_version}
        # using fakeroot version {default_version}
        pkgname = {default_package_name}
        pkgbase = {default_package_name}
        pkgver = {default_full_version}
        pkgdesc = {default_description}
        url = {url}
        builddate = 1
        packager = {default_packager}
        size = 1
        arch = {default_arch}
        license = {default_license}
        depend = foo
        depend = bar
        optdepend = foobar: descriptions with an equal = sign
        """

    yield StringIO(initial_value="\n".join([line.strip() for line in dedent(file_data).split("\n") if line]))


@fixture(scope="function")
def pkginfov2_stringio(
    default_arch: str,
    default_description: str,
    default_full_version: str,
    default_license: str,
    default_package_name: str,
    default_packager: str,
    default_pkgtype: str,
    default_version: str,
    url: str,
) -> Generator[StringIO, None, None]:
    """Yield a StringIO function-wide representing PkgInfoV2 data."""
    file_data = f"""# Generated by makepkg {default_version}
        # using fakeroot version {default_version}
        pkgname = {default_package_name}
        pkgbase = {default_package_name}
        xdata = pkgtype={default_pkgtype}
        xdata = url=bar
        pkgver = {default_full_version}
        pkgdesc = {default_description}
        url = {url}
        builddate = 1
        packager = {default_packager}
        size = 1
        arch = {default_arch}
        license = {default_license}
        depend = foo
        depend = bar
        optdepend = foobar: descriptions with an equal = sign
        """

    yield StringIO(initial_value="\n".join([line.strip() for line in dedent(file_data).split("\n") if line]))


@fixture(scope="function")
def debug_pkginfov2_stringio(
    default_arch: str,
    default_description: str,
    default_full_version: str,
    default_license: str,
    default_package_name: str,
    default_packager: str,
    default_version: str,
    url: str,
) -> Generator[StringIO, None, None]:
    """Yield a StringIO function-wide representing PkgInfoV2 data of a debug package."""
    file_data = f"""# Generated by makepkg {default_version}
        # using fakeroot version {default_version}
        pkgname = {default_package_name}-debug
        pkgbase = {default_package_name}
        xdata = pkgtype=debug
        xdata = url=bar
        pkgver = {default_full_version}
        pkgdesc = {default_description}
        url = {url}
        builddate = 1
        packager = {default_packager}
        size = 1
        arch = {default_arch}
        license = {default_license}
        depend = foo
        depend = bar
        """

    yield StringIO(initial_value="\n".join([line.strip() for line in dedent(file_data).split("\n") if line]))


@fixture(scope="function")
def valid_pkginfov1_file(pkginfov1_stringio: StringIO) -> Generator[Path, None, None]:
    """Yield a Path function-wide representing a PkgInfoV1 file."""
    with NamedTemporaryFile() as file:
        with open(file.name, mode="wt") as f:
            print(pkginfov1_stringio.getvalue(), file=f)

        yield Path(file.name)


@fixture(scope="function")
def valid_pkginfov2_file(pkginfov2_stringio: StringIO, tmp_path: Path) -> Generator[Path, None, None]:
    """Yield a Path function-wide representing a PkgInfoV2 file."""
    with NamedTemporaryFile(prefix="pkginfov2_", dir=tmp_path, delete=False) as file:
        with open(file.name, mode="wt") as f:
            print(pkginfov2_stringio.getvalue(), file=f)

    yield Path(file.name)


@fixture(scope="function")
def debug_pkginfov2_file(debug_pkginfov2_stringio: StringIO, tmp_path: Path) -> Generator[Path, None, None]:
    """Yield a Path function-wide representing a PkgInfoV2 file of a debug package."""
    with NamedTemporaryFile(prefix="pkginfov2_debug_", dir=tmp_path, delete=False) as file:
        with open(file.name, mode="wt") as f:
            print(debug_pkginfov2_stringio.getvalue(), file=f)

    yield Path(file.name)


@fixture(scope="session")
def valid_pkginfov1(
    default_arch: str,
    default_description: str,
    default_full_version: str,
    default_license: str,
    default_packager: str,
    default_version: str,
    url: str,
) -> PkgInfo:
    """Return a PkgInfoV1 session-wide."""
    return PkgInfoV1(
        arch=default_arch,
        backup=None,
        base="foo",
        builddate=1,
        checkdepends=None,
        conflicts=None,
        depends=None,
        desc=default_description,
        fakeroot_version=default_version,
        groups=None,
        isize=1,
        packager=default_packager,
        license=[default_license],
        makedepends=None,
        makepkg_version=default_version,
        name="foo",
        optdepends=None,
        provides=None,
        replaces=None,
        url=url,  # type: ignore[arg-type]
        version=default_full_version,
    )


@fixture(scope="session")
def valid_pkginfov2(
    default_arch: str,
    default_description: str,
    default_full_version: str,
    default_license: str,
    default_packager: str,
    default_pkgtype: str,
    default_version: str,
    url: str,
) -> PkgInfo:
    """Return a PkgInfoV2 session-wide."""
    return PkgInfoV2(
        arch=default_arch,
        backup=None,
        base="foo",
        builddate=1,
        checkdepends=None,
        conflicts=None,
        depends=None,
        desc=default_description,
        fakeroot_version=default_version,
        groups=None,
        isize=1,
        packager=default_packager,
        license=[default_license],
        makedepends=None,
        makepkg_version=default_version,
        name="foo",
        optdepends=None,
        provides=None,
        replaces=None,
        url=url,  # type: ignore[arg-type]
        version=default_full_version,
        xdata=[PkgType(pkgtype=default_pkgtype)],  # type: ignore[arg-type]
    )


@fixture(scope="function")
def filesv1() -> FilesV1:
    """Return a FilesV1 function-wide."""
    return FilesV1(files=["foo", "bar"])


@fixture(scope="function")
def outputpackagev1(
    base64_pgpsig: str,
    default_description: str,
    default_filename: str,
    default_license: str,
    filesv1: FilesV1,
    md5sum: str,
    sha256sum: str,
    url: str,
) -> OutputPackageV1:
    """Return an OutputPackageV1 function-wide."""
    return OutputPackageV1(
        arch="any",
        builddate=1,
        csize=1,
        desc=default_description,
        filename=default_filename,
        files=filesv1,
        isize=1,
        license=[default_license],
        md5sum=md5sum,
        name="foo",
        pgpsig=base64_pgpsig,
        sha256sum=sha256sum,
        url=url,  # type: ignore[arg-type]
    )


@fixture(scope="function")
def outputpackagebasev1(
    base64_pgpsig: str,
    default_description: str,
    default_filename: str,
    default_full_version: str,
    default_license: str,
    default_packager: str,
    filesv1: FilesV1,
    md5sum: str,
    outputpackagev1: OutputPackageV1,
    sha256sum: str,
    url: str,
    valid_buildinfov1: BuildInfo,
) -> OutputPackageBaseV1:
    """Return an OutputPackageBaseV1 function-wide."""
    outputpackage2 = deepcopy(outputpackagev1)
    outputpackage2.filename = outputpackage2.filename.replace("foo", "bar")
    outputpackage2.name = "bar"
    outputpackage2.files = FilesV1(files=["bar"])

    return OutputPackageBaseV1(
        base="foo",
        buildinfo=OutputBuildInfo.from_buildinfo(valid_buildinfov1),
        packager=default_packager,
        packages=[
            outputpackagev1,
            outputpackage2,
        ],
        version=default_full_version,
    )


@fixture(scope="function")
def packagedescv1(
    base64_pgpsig: str,
    default_description: str,
    default_filename: str,
    default_full_version: str,
    default_license: str,
    default_packager: str,
    md5sum: str,
    sha256sum: str,
    url: str,
) -> PackageDescV1:
    """Return a PackageDescV1 function-wide."""
    return PackageDescV1(
        arch="any",
        base="foo",
        builddate=1,
        csize=1,
        desc=default_description,
        filename=default_filename,
        isize=1,
        license=[default_license],
        md5sum=md5sum,
        name="foo",
        packager=default_packager,
        pgpsig=base64_pgpsig,
        sha256sum=sha256sum,
        url=url,  # type: ignore[arg-type]
        version=default_full_version,
    )


@fixture(scope="function")
def packagedescv2(
    default_description: str,
    default_filename: str,
    default_full_version: str,
    default_license: str,
    default_packager: str,
    md5sum: str,
    sha256sum: str,
    url: str,
) -> PackageDescV2:
    """Return a PackageDescV2 function-wide."""
    return PackageDescV2(
        arch="any",
        base="foo",
        builddate=1,
        csize=1,
        desc=default_description,
        filename=default_filename,
        isize=1,
        license=[default_license],
        name="foo",
        packager=default_packager,
        sha256sum=sha256sum,
        url=url,  # type: ignore[arg-type]
        version=default_full_version,
    )


@pytest_asyncio.fixture(
    scope="function",
    params=[
        CompressionTypeEnum.BZIP2,
        CompressionTypeEnum.GZIP,
        CompressionTypeEnum.LZMA,
        CompressionTypeEnum.ZSTANDARD,
    ],
    ids=[
        "default bzip2",
        "default gzip",
        "default lzma",
        "default zstandard",
    ],
)
async def default_sync_db_file(
    md5sum: str,
    outputpackagebasev1: OutputPackageBaseV1,
    request: Any,
    sha256sum: str,
    tmp_path: Path,
) -> AsyncGenerator[tuple[Path, Path], None]:
    """Yield a tuple of two Paths function-wide, representing a default repo sync db and its symlink."""
    compression = request.param
    suffix = ""
    match compression:
        case CompressionTypeEnum.BZIP2:
            suffix = ".bz2"
        case CompressionTypeEnum.GZIP:
            suffix = ".gz"
        case CompressionTypeEnum.LZMA:
            suffix = ".xz"
        case CompressionTypeEnum.ZSTANDARD:
            suffix = ".zst"

    tar_db_name = Path(f"test.db.tar{suffix}")
    symlink_db_name = Path("test.db")

    sync_db_tarfile = tmp_path / f"test.tar{compression}"
    sync_db_tarfile = tmp_path / tar_db_name
    sync_db_symlink = tmp_path / symlink_db_name
    sync_db = SyncDatabase(
        database=sync_db_tarfile,
        database_type=RepoDbTypeEnum.DEFAULT,
        compression_type=compression,
        desc_version=PackageDescVersionEnum.DEFAULT,
        files_version=FilesVersionEnum.DEFAULT,
    )
    await sync_db.add(model=outputpackagebasev1)

    chdir(tmp_path)
    symlink_db_name.symlink_to(sync_db_tarfile.name)
    yield (sync_db_tarfile, sync_db_symlink)


@pytest_asyncio.fixture(
    scope="function",
    params=[
        CompressionTypeEnum.BZIP2,
        CompressionTypeEnum.GZIP,
        CompressionTypeEnum.LZMA,
        CompressionTypeEnum.ZSTANDARD,
    ],
    ids=[
        "files bzip2",
        "files gzip",
        "files lzma",
        "files zstandard",
    ],
)
async def files_sync_db_file(
    md5sum: str,
    outputpackagebasev1: OutputPackageBaseV1,
    request: Any,
    sha256sum: str,
) -> AsyncGenerator[tuple[Path, Path], None]:
    """Yield a tuple of two Paths function-wide, representing a files repo sync db and its symlink."""
    compression = request.param
    suffix = ""
    match compression:
        case CompressionTypeEnum.BZIP2:
            suffix = ".bz2"
        case CompressionTypeEnum.GZIP:
            suffix = ".gz"
        case CompressionTypeEnum.LZMA:
            suffix = ".xz"
        case CompressionTypeEnum.ZSTANDARD:
            suffix = ".zst"

    tar_db_name = Path(f"test.files.tar{suffix}")
    symlink_db_name = Path("test.files")

    with TemporaryDirectory() as tmp_path:
        temp_path = Path(tmp_path)
        sync_db_tarfile = temp_path / tar_db_name
        sync_db_symlink = temp_path / symlink_db_name
        sync_db = SyncDatabase(
            database=sync_db_tarfile,
            database_type=RepoDbTypeEnum.FILES,
            compression_type=compression,
            desc_version=PackageDescVersionEnum.DEFAULT,
            files_version=FilesVersionEnum.DEFAULT,
        )
        await sync_db.add(model=outputpackagebasev1)

        chdir(temp_path)
        symlink_db_name.symlink_to(sync_db_tarfile.name)
        yield (sync_db_tarfile, sync_db_symlink)


@fixture(
    scope="function",
    params=[name for name in CompressionTypeEnum],
    ids=[name.value for name in CompressionTypeEnum],
)
def debug_package_file(
    default_arch: str,
    default_package_name: str,
    default_full_version: str,
    text_file: Path,
    tmp_path: Path,
    valid_mtree_file: Path,
    valid_buildinfov2_file: Path,
    debug_pkginfov2_file: Path,
    request: Any,
) -> tuple[Path, ...]:
    """Return a tuple of two Paths function-wide, representing a debug package file and its dummy signature."""
    compression = request.param
    suffix = "." + str(request.param.value) if request.param.value else ""
    pkg_name = Path(f"{default_package_name}-debug-{default_full_version}-{default_arch}.pkg.tar{suffix}")
    sig_name = Path(f"{default_package_name}-debug-{default_full_version}-{default_arch}.pkg.tar{suffix}.sig")
    pkg_path = tmp_path / pkg_name
    sig_path = tmp_path / sig_name
    text_file_symlink = text_file.parent / "debug_symlink_to_text_file"
    text_file_symlink.symlink_to("text_file")

    with open_tarfile(path=pkg_path, compression=compression, mode="x") as tarfile:
        tarfile.add(valid_buildinfov2_file, ".BUILDINFO")
        tarfile.add(valid_mtree_file, ".MTREE")
        tarfile.add(debug_pkginfov2_file, ".PKGINFO")
        tarfile.add(text_file, "text_file")
        tarfile.add(text_file_symlink, "text_file_symlink")
        tarfile.add(tmp_path, "empty_dir", recursive=False)

    with open(sig_path, "wb") as sig_file:
        sig_file.write(b"THIS IS NOT A VALID SIGNATURE")

    return (pkg_path, sig_path)


@fixture(
    scope="function",
    params=[name for name in CompressionTypeEnum],
    ids=[name.value for name in CompressionTypeEnum],
)
def default_package_file(
    default_arch: str,
    default_package_name: str,
    default_full_version: str,
    text_file: Path,
    tmp_path: Path,
    valid_mtree_file: Path,
    valid_buildinfov2_file: Path,
    valid_pkginfov2_file: Path,
    request: Any,
) -> tuple[Path, ...]:
    """Return a tuple of two Paths function-wide, representing a default package file and its dummy signature."""
    compression = request.param
    suffix = "." + str(request.param.value) if request.param.value else ""
    pkg_name = Path(f"{default_package_name}-{default_full_version}-{default_arch}.pkg.tar{suffix}")
    sig_name = Path(f"{default_package_name}-{default_full_version}-{default_arch}.pkg.tar{suffix}.sig")
    pkg_path = tmp_path / pkg_name
    sig_path = tmp_path / sig_name
    text_file_symlink = text_file.parent / "symlink_to_text_file"
    text_file_symlink.symlink_to("text_file")

    with open_tarfile(path=pkg_path, compression=compression, mode="x") as tarfile:
        tarfile.add(valid_buildinfov2_file, ".BUILDINFO")
        tarfile.add(valid_mtree_file, ".MTREE")
        tarfile.add(valid_pkginfov2_file, ".PKGINFO")
        tarfile.add(text_file, "text_file")
        tarfile.add(text_file_symlink, "text_file_symlink")
        tarfile.add(tmp_path, "empty_dir", recursive=False)

    with open(sig_path, "wb") as sig_file:
        sig_file.write(b"THIS IS NOT A VALID SIGNATURE")

    return (pkg_path, sig_path)


@fixture(scope="function")
def outputpackagebasev1_json_files_in_dir(
    tmp_path: Path,
    outputpackagebasev1: OutputPackageBase,
) -> Path:
    """Return a dir Path function-wide, representing a management repository layout with JSON files."""
    outputpackagebasev1.packages[0].files = None  # type: ignore[attr-defined]

    management_dir = tmp_path / "management"
    pkgnames_dir = management_dir / "pkgnames"
    pkgnames_dir.mkdir(parents=True)

    pkgbase_file = management_dir / f"{outputpackagebasev1.base}.json"  # type: ignore[attr-defined]
    with open(pkgbase_file, "wb") as output_file:
        output_file.write(
            orjson.dumps(
                outputpackagebasev1.model_dump(mode="json"),
                option=orjson.OPT_INDENT_2 | orjson.OPT_APPEND_NEWLINE | orjson.OPT_SORT_KEYS,
            )
        )

    for package in outputpackagebasev1.packages:  # type: ignore[attr-defined]
        symlink_path = pkgnames_dir / f"{package.name}.json"
        symlink_path.symlink_to(relative_to_shared_base(path_b=symlink_path, path_a=pkgbase_file))

    return management_dir


@fixture(scope="function")
def empty_dir(tmp_path: Path) -> Path:
    """Return a Path function-wide, representing an empty directory."""
    directory = tmp_path / "empty"
    directory.mkdir()
    return directory


@fixture(scope="function")
def empty_file(tmp_path: Path) -> Path:
    """Return a Path function-wide, representing an empty file."""
    file = NamedTemporaryFile(prefix="empty_", dir=tmp_path, delete=False)
    return Path(file.name)


@fixture(scope="function")
def empty_syncdbs(tmp_path: Path) -> list[Path]:
    """Return a list of Paths function-wide, representing empty default and files repo sync databases."""
    directory = tmp_path / "pacman/sync"
    files: list[Path] = [directory / "tmp.db", directory / "tmp.files"]

    directory.mkdir(parents=True)
    for file in files:
        file.touch()

    return files


@fixture(scope="function")
def broken_json_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Yield a Path function-wide, representing a broken JSON file."""
    with NamedTemporaryFile(prefix="broken_", suffix=".json", dir=tmp_path, delete=False) as json_file:
        json_file.write(b"garbage")
        path = Path(json_file.name)
    yield path


@fixture(scope="function")
def invalid_json_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Yield a Path function-wide, representing an invalid JSON file."""
    with NamedTemporaryFile(prefix="invalid_", suffix=".json", dir=tmp_path, delete=False) as json_file:
        json_file.write(b'{"foo": "bar"}')
        path = Path(json_file.name)
    yield path


@fixture(scope="function")
def empty_toml_file(tmp_path: Path) -> Path:
    """Yield a Path function-wide, representing an empty TOML file (with .conf suffix)."""
    return Path(NamedTemporaryFile(suffix=".conf", dir=tmp_path, delete=False).name)


@fixture(scope="function")
def empty_toml_files_in_dir(tmp_path: Path) -> Path:
    """Yield a Path function-wide, representing a directory containing empty TOML files (with .conf suffix)."""
    for i in range(5):
        NamedTemporaryFile(suffix=".conf", dir=tmp_path, delete=False)
    return tmp_path


def params_for_vercmp() -> list[bool]:
    """Create params for pyalpm_vercmp_fun."""
    if "linux" not in sys.platform:
        return [False]
    else:
        return [True, False]


@fixture(scope="session", params=params_for_vercmp())
def pyalpm_vercmp_fun(request: Any) -> bool:
    """Return a boolean value based on params_for_vercmp."""
    return bool(request.param)


@fixture(scope="function")
def packagerepo_in_tmp_path(tmp_path: Path, caplog: LogCaptureFixture) -> PackageRepo:
    """Return a PackageRepo function-wide."""
    caplog.set_level(DEBUG)

    management_repo_base = tmp_path / "management_repo_base"
    source_repo_base = tmp_path / "source_repo_base"
    source_pool_base = tmp_path / "source_pool_base"
    package_repo_base = tmp_path / "package_repo_base"
    package_pool_base = tmp_path / "package_pool_base"

    package_repo = PackageRepo(
        name=DEFAULT_NAME,  # type: ignore[arg-type]
        architecture=DEFAULT_ARCHITECTURE,
        archiving=None,
        database_compression=DEFAULT_DATABASE_COMPRESSION,
        management_repo=ManagementRepo(directory=(management_repo_base / DEFAULT_NAME)),
        package_pool=(package_pool_base / DEFAULT_NAME),
        source_pool=(source_pool_base / DEFAULT_NAME),
        debug=Path(f"{DEFAULT_NAME}-debug"),
        staging=Path(f"{DEFAULT_NAME}-staging"),
        staging_debug=Path(f"{DEFAULT_NAME}-staging-debug"),
        testing=Path(f"{DEFAULT_NAME}-testing"),
        testing_debug=Path(f"{DEFAULT_NAME}-testing-debug"),
    )

    package_repo._stable_management_repo_dir = management_repo_base / f"{DEFAULT_ARCHITECTURE.value}/{DEFAULT_NAME}"
    package_repo._stable_repo_dir = package_repo_base / f"{DEFAULT_NAME}/{DEFAULT_ARCHITECTURE.value}"
    package_repo._stable_source_repo_dir = source_repo_base / f"{DEFAULT_NAME}/{DEFAULT_ARCHITECTURE.value}"

    package_repo._debug_management_repo_dir = (
        management_repo_base / f"{DEFAULT_ARCHITECTURE.value}/{DEFAULT_NAME}-debug"
    )
    package_repo._debug_repo_dir = package_repo_base / Path(f"{DEFAULT_NAME}-debug/{DEFAULT_ARCHITECTURE.value}")
    package_repo._debug_source_repo_dir = source_repo_base / Path(f"{DEFAULT_NAME}-debug/{DEFAULT_ARCHITECTURE.value}")

    package_repo._staging_management_repo_dir = (
        management_repo_base / f"{DEFAULT_ARCHITECTURE.value}/{DEFAULT_NAME}-staging"
    )
    package_repo._staging_repo_dir = package_repo_base / Path(f"{DEFAULT_NAME}-staging/{DEFAULT_ARCHITECTURE.value}")
    package_repo._staging_source_repo_dir = source_repo_base / Path(
        f"{DEFAULT_NAME}-staging/{DEFAULT_ARCHITECTURE.value}"
    )

    package_repo._staging_debug_management_repo_dir = (
        management_repo_base / f"{DEFAULT_ARCHITECTURE.value}/{DEFAULT_NAME}-staging-debug"
    )
    package_repo._staging_debug_repo_dir = package_repo_base / Path(
        f"{DEFAULT_NAME}-staging-debug/{DEFAULT_ARCHITECTURE.value}"
    )
    package_repo._staging_debug_source_repo_dir = source_repo_base / Path(
        f"{DEFAULT_NAME}-staging-debug/{DEFAULT_ARCHITECTURE.value}"
    )

    package_repo._testing_management_repo_dir = (
        management_repo_base / f"{DEFAULT_ARCHITECTURE.value}/{DEFAULT_NAME}-testing"
    )
    package_repo._testing_repo_dir = package_repo_base / Path(f"{DEFAULT_NAME}-testing/{DEFAULT_ARCHITECTURE.value}")
    package_repo._testing_source_repo_dir = source_repo_base / Path(
        f"{DEFAULT_NAME}-testing/{DEFAULT_ARCHITECTURE.value}"
    )

    package_repo._testing_debug_management_repo_dir = (
        management_repo_base / f"{DEFAULT_ARCHITECTURE.value}/{DEFAULT_NAME}-testing-debug"
    )
    package_repo._testing_debug_repo_dir = package_repo_base / Path(
        f"{DEFAULT_NAME}-testing-debug/{DEFAULT_ARCHITECTURE.value}"
    )
    package_repo._testing_debug_source_repo_dir = source_repo_base / Path(
        f"{DEFAULT_NAME}-testing-debug/{DEFAULT_ARCHITECTURE.value}"
    )

    package_repo._package_pool_dir = package_pool_base / DEFAULT_NAME
    package_repo._source_pool_dir = source_pool_base / DEFAULT_NAME

    debug("Creating package repo fixture")
    debug(package_repo)
    return package_repo


@fixture(scope="function")
@patch("repod.config.settings.get_default_archive_settings")
def usersettings(
    get_default_archive_settings_mock: Mock,
    packagerepo_in_tmp_path: PackageRepo,
    empty_file: Path,
    tmp_path: Path,
    caplog: LogCaptureFixture,
) -> UserSettings:
    """Return a UserSettings function-wide."""
    caplog.set_level(DEBUG)
    tmp_dir_path = tmp_path / "usersettings"

    get_default_archive_settings_mock.return_value = ArchiveSettings(
        packages=tmp_dir_path / "archive/package",
        sources=tmp_dir_path / "archive/sources",
    )
    with patch("repod.config.settings.CUSTOM_CONFIG", empty_file):
        with patch("repod.config.settings.UserSettings._management_repo_base", tmp_dir_path / "management"):
            with patch("repod.config.settings.UserSettings._package_pool_base", tmp_dir_path / "data/pool/package"):
                with patch("repod.config.settings.UserSettings._package_repo_base", tmp_dir_path / "data/repo/package"):
                    with patch(
                        "repod.config.settings.UserSettings._source_pool_base", tmp_dir_path / "data/pool/source"
                    ):
                        with patch(
                            "repod.config.settings.UserSettings._source_repo_base",
                            tmp_dir_path / "data/repo/source",
                        ):
                            return UserSettings(
                                repositories=[packagerepo_in_tmp_path],
                            )


@fixture(scope="function")
def srcinfov1_single_stringio(
    default_arch: str,
    url: str,
    default_license: str,
    default_package_name: str,
    default_version: str,
    default_packager: str,
    sha256sum: str,
) -> Generator[StringIO, None, None]:
    """Yield a StringIO function-wide, representing SrcInfoV1 data of a single package."""
    buildinfov1_contents = f"""
        # foo
        pkgbase = {default_package_name}
        \tpkgdesc = description
        \tepoch = 1
        \tpkgver = {default_version}
        \tpkgrel = 1
        \turl = {url}
        \tarch = {default_arch}
        \tlicense = {default_license}
        \toptions = debug
        \toptions = strip

        pkgname = {default_package_name}
        """

    yield StringIO(initial_value=dedent(buildinfov1_contents).strip())


@fixture(scope="function")
def srcinfov1_split_stringio(
    default_arch: str,
    url: str,
    default_license: str,
    default_package_name: str,
    default_version: str,
    default_packager: str,
    sha256sum: str,
) -> Generator[StringIO, None, None]:
    """Yield a StringIO function-wide, representing SrcInfoV1 data of a split package."""
    buildinfov1_contents = f"""
        # foo
        pkgbase = {default_package_name}
        \tpkgdesc = description
        \tpkgver = {default_version}
        \tpkgrel = 1
        \turl = {url}
        \tarch = {default_arch}
        \tlicense = {default_license}
        \toptions = debug
        \toptions = strip

        pkgname = {default_package_name}
        \tpkgdesc = other description

        pkgname = {default_package_name}-b
        \tpkgdesc = other description
        """

    yield StringIO(initial_value=dedent(buildinfov1_contents).strip())


@fixture(scope="function")
def srcinfov1_single_file(srcinfov1_single_stringio: StringIO) -> Generator[Path, None, None]:
    """Yield a Path function-wide, representing a SrcInfoV1 file of a single package."""
    with NamedTemporaryFile(prefix="srcinfov1_single_") as buildinfo_file:
        with open(buildinfo_file.name, mode="wt") as f:
            print(srcinfov1_single_stringio.getvalue(), file=f)

        yield Path(buildinfo_file.name)


@fixture(scope="function")
def srcinfov1_split_file(srcinfov1_split_stringio: StringIO, tmp_path: Path) -> Generator[Path, None, None]:
    """Yield a Path function-wide, representing a SrcInfoV1 file of a split package."""
    with NamedTemporaryFile(prefix="srcinfov1_split_", dir=tmp_path, delete=False) as buildinfo_file:
        with open(buildinfo_file.name, mode="wt") as f:
            print(srcinfov1_split_stringio.getvalue(), file=f)

    yield Path(buildinfo_file.name)
