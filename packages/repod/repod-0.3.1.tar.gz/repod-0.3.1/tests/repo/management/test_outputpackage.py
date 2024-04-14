from contextlib import nullcontext as does_not_raise
from copy import deepcopy
from logging import DEBUG
from pathlib import Path
from typing import Any, ContextManager
from unittest.mock import Mock, patch

from pytest import LogCaptureFixture, mark, raises

from repod.common.enums import (
    FilesVersionEnum,
    OutputPackageVersionEnum,
    PackageDescVersionEnum,
    PkgTypeEnum,
)
from repod.errors import RepoManagementFileError, RepoManagementValidationError
from repod.files.buildinfo import BuildInfo
from repod.files.package import Package
from repod.files.pkginfo import PkgType
from repod.repo.management import outputpackage
from repod.repo.package import syncdb
from tests.conftest import (
    BuildInfoV9999,
    OutputPackageBaseV9999,
    create_base64_pgpsig,
    create_default_filename,
    create_default_full_version,
    create_default_packager,
    create_md5sum,
    create_sha256sum,
    create_url,
)


def test_outputpackage_from_packagev1(packagev1: Package) -> None:
    override: dict[int, dict[str, set[str]]] = {
        1: {
            "required": {
                "arch",
                "builddate",
                "csize",
                "desc",
                "filename",
                "isize",
                "license",
                "md5sum",
                "name",
                "sha256sum",
                "url",
            },
            "optional": {
                "backup",
                "checkdepends",
                "conflicts",
                "depends",
                "files",
                "groups",
                "optdepends",
                "pgpsig",
                "provides",
                "replaces",
            },
        },
    }
    with patch("repod.repo.management.outputpackage.OUTPUT_PACKAGE_VERSIONS", override):
        outputpackage.OutputPackage.from_package(package=packagev1)


def test_outputpackage_from_packagev2(packagev2: Package) -> None:
    outputpackage.OutputPackage.from_package(package=packagev2)


def test_outputpackage_from_package() -> None:
    with raises(RuntimeError):
        outputpackage.OutputPackage.from_package(package=Package())


@mark.parametrize(
    "outputpackagebase_version, packagedesc_version, files_version, expectation",
    [
        (1, PackageDescVersionEnum.ONE, FilesVersionEnum.ONE, does_not_raise()),
        (1, PackageDescVersionEnum.TWO, FilesVersionEnum.ONE, does_not_raise()),
        (None, PackageDescVersionEnum.ONE, FilesVersionEnum.ONE, raises(RuntimeError)),
        (9999, PackageDescVersionEnum.ONE, FilesVersionEnum.ONE, raises(RuntimeError)),
    ],
)
@mark.asyncio
async def test_output_package_base_v1_get_packages_as_models(
    packagedescv1: outputpackage.PackageDescV1,
    packagedescv2: outputpackage.PackageDescV2,
    filesv1: syncdb.FilesV1,
    outputpackagebasev1: outputpackage.OutputPackageBase,
    outputpackagebase_version: int | None,
    packagedesc_version: PackageDescVersionEnum,
    files_version: FilesVersionEnum,
    expectation: ContextManager[str],
) -> None:
    packagedesc: syncdb.PackageDesc
    match packagedesc_version:
        case PackageDescVersionEnum.ONE:
            packagedesc = packagedescv1
        case PackageDescVersionEnum.TWO:
            packagedesc = packagedescv2

    files: syncdb.Files
    match files_version:
        case FilesVersionEnum.ONE:
            files = filesv1

    match outputpackagebase_version:
        case None:
            output_package_base = outputpackage.OutputPackageBase()
        case 1:
            output_package_base = outputpackagebasev1
            # remove all but the first package
            output_package_base.packages = output_package_base.packages[0:1]  # type: ignore[attr-defined]
        case 9999:
            output_package_base = OutputPackageBaseV9999()

    with expectation:
        assert [(packagedesc, files)] == await output_package_base.get_packages_as_models(  # nosec: B101
            packagedesc_version=packagedesc_version,
            files_version=files_version,
        )


@mark.parametrize(
    "output_package_version, data, expectation",
    [
        (
            OutputPackageVersionEnum.ONE,
            {
                "base": "foo",
                "makedepends": ["bar"],
                "packager": "someone",
                "packages": [],
                "version": create_default_full_version(),
            },
            raises(RepoManagementValidationError),
        ),
        (
            OutputPackageVersionEnum.ONE,
            {
                "base": "foo",
                "makedepends": ["bar"],
                "packager": create_default_packager(),
                "packages": [],
                "schema_version": 1,
                "version": create_default_full_version(),
            },
            does_not_raise(),
        ),
        (
            OutputPackageVersionEnum.ONE,
            {
                "base": "foo",
                "makedepends": ["bar"],
                "packager": create_default_packager(),
                "packages": [],
                "schema_version": 0,
                "version": create_default_full_version(),
            },
            does_not_raise(),
        ),
        (
            OutputPackageVersionEnum.ONE,
            {
                "base": "foo",
                "makedepends": ["bar"],
                "packager": create_default_packager(),
                "packages": [],
                "schema_version": 9999,
                "version": create_default_full_version(),
            },
            raises(RepoManagementValidationError),
        ),
        (
            OutputPackageVersionEnum.ONE,
            {
                "base": "foo",
                "makedepends": ["bar"],
                "packager": create_default_packager(),
                "packages": [
                    {
                        "arch": "any",
                        "backup": ["foo"],
                        "builddate": 1,
                        "checkdepends": [],
                        "conflicts": [],
                        "csize": 1,
                        "depends": ["bar"],
                        "desc": "something",
                        "filename": create_default_filename(),
                        "files": {"files": ["foo", "bar"]},
                        "groups": [],
                        "isize": 1,
                        "license": ["GPL"],
                        "md5sum": create_md5sum(),
                        "name": "foo",
                        "optdepends": [],
                        "pgpsig": create_base64_pgpsig(),
                        "provides": [],
                        "replaces": [],
                        "schema_version": 1,
                        "sha256sum": create_sha256sum(),
                        "url": create_url(),
                    },
                ],
                "schema_version": 1,
                "version": create_default_full_version(),
            },
            does_not_raise(),
        ),
        (
            OutputPackageVersionEnum.ONE,
            {
                "base": "foo",
                "makedepends": ["bar"],
                "packager": create_default_packager(),
                "packages": [
                    {
                        "arch": "any",
                        "backup": ["foo"],
                        "builddate": 1,
                        "checkdepends": [],
                        "conflicts": [],
                        "csize": 1,
                        "depends": ["bar"],
                        "desc": "something",
                        "filename": create_default_filename(),
                        "files": {"files": [], "schema_version": 1},
                        "groups": [],
                        "isize": 1,
                        "license": ["GPL"],
                        "md5sum": create_md5sum(),
                        "name": "foo",
                        "optdepends": [],
                        "pgpsig": create_base64_pgpsig(),
                        "provides": [],
                        "replaces": [],
                        "schema_version": 1,
                        "sha256sum": create_sha256sum(),
                        "url": create_url(),
                    },
                ],
                "schema_version": 1,
                "version": create_default_full_version(),
            },
            does_not_raise(),
        ),
        (
            OutputPackageVersionEnum.ONE,
            {
                "base": "foo",
                "makedepends": ["bar"],
                "packager": create_default_packager(),
                "packages": [
                    {
                        "arch": "any",
                        "backup": ["foo"],
                        "builddate": 1,
                        "checkdepends": [],
                        "conflicts": [],
                        "csize": 1,
                        "depends": ["bar"],
                        "desc": "something",
                        "filename": create_default_filename(),
                        "files": None,
                        "groups": [],
                        "isize": 1,
                        "license": ["GPL"],
                        "md5sum": create_md5sum(),
                        "name": "foo",
                        "optdepends": [],
                        "pgpsig": create_base64_pgpsig(),
                        "provides": [],
                        "replaces": [],
                        "schema_version": 1,
                        "sha256sum": create_sha256sum(),
                        "url": create_url(),
                    },
                ],
                "schema_version": 1,
                "version": create_default_full_version(),
            },
            does_not_raise(),
        ),
        (
            OutputPackageVersionEnum.TWO,
            {
                "base": "foo",
                "makedepends": ["bar"],
                "packager": create_default_packager(),
                "packages": [
                    {
                        "arch": "any",
                        "backup": ["foo"],
                        "builddate": 1,
                        "checkdepends": [],
                        "conflicts": [],
                        "csize": 1,
                        "depends": ["bar"],
                        "desc": "something",
                        "filename": create_default_filename(),
                        "files": {"files": ["foo", "bar"]},
                        "groups": [],
                        "isize": 1,
                        "license": ["GPL"],
                        "name": "foo",
                        "optdepends": [],
                        "pgpsig": create_base64_pgpsig(),
                        "provides": [],
                        "replaces": [],
                        "schema_version": 2,
                        "sha256sum": create_sha256sum(),
                        "url": create_url(),
                    },
                ],
                "schema_version": 1,
                "version": create_default_full_version(),
            },
            does_not_raise(),
        ),
        (
            OutputPackageVersionEnum.ONE,
            {
                "base": "foo",
                "makedepends": ["bar"],
                "packager": create_default_packager(),
                "packages": "foo",
                "schema_version": 1,
                "version": create_default_full_version(),
            },
            raises(RepoManagementValidationError),
        ),
    ],
    ids=[
        "no schema version",
        "schema version 1, no packages",
        "schema version 0, no packages",
        "schema version 9999, no packages",
        "schema version 1, 1 version 1 package",
        "schema version 1, 1 version 1 package, filesv1",
        "schema version 1, 1 version 1 package, no files",
        "schema version 1, 1 version 2 package",
        "schema version 1, package is string",
    ],
)
@patch("repod.repo.management.outputpackage.OutputPackageVersionEnum")
def test_outputpackagebase_from_dict(
    outputput_package_version_enum_mock: Mock,
    output_package_version: OutputPackageVersionEnum,
    data: dict[str, Any | list[Any]],
    expectation: ContextManager[str],
) -> None:
    outputput_package_version_enum_mock.DEFAULT = output_package_version
    with expectation:
        assert isinstance(  # nosec: B101
            outputpackage.OutputPackageBase.from_dict(data=data), outputpackage.OutputPackageBase
        )


@mark.asyncio
async def test_outputpackagebase_from_file(broken_json_file: Path, invalid_json_file: Path) -> None:
    with raises(RepoManagementFileError):
        await outputpackage.OutputPackageBase.from_file(path=broken_json_file)
    with raises(RepoManagementValidationError):
        await outputpackage.OutputPackageBase.from_file(path=invalid_json_file)


def test_outputpackagebase_from_package() -> None:
    with raises(RuntimeError):
        outputpackage.OutputPackageBase.from_package(packages=[Package()])


def test_outputpackagebase_from_packagev1(packagev1: Package) -> None:
    assert outputpackage.OutputPackageBase.from_package(packages=[packagev1])  # nosec: B101


def test_outputpackagebase_from_package_raise_on_no_package() -> None:
    with raises(ValueError):
        assert outputpackage.OutputPackageBase.from_package(packages=[])  # nosec: B101


def test_outputpackagebase_from_packagev1_raise_on_multiple_pkgbases(packagev1: Package) -> None:
    package_b = deepcopy(packagev1)
    package_b.buildinfo.pkgbase = "wrong"  # type: ignore[attr-defined]
    with raises(ValueError):
        outputpackage.OutputPackageBase.from_package(packages=[packagev1, package_b])


def test_outputpackagebase_from_packagev1_raise_on_duplicate_names(packagev1: Package) -> None:
    package_b = deepcopy(packagev1)
    with raises(ValueError):
        outputpackage.OutputPackageBase.from_package(packages=[packagev1, package_b])


def test_outputpackagebase_from_packagev1_raise_on_version_mismatch(
    packagev1: Package, caplog: LogCaptureFixture
) -> None:
    caplog.set_level(DEBUG)
    package_b = deepcopy(packagev1)
    package_b.pkginfo.name = "different"  # type: ignore[attr-defined]
    package_b.pkginfo.version = "wrong"  # type: ignore[attr-defined]
    with raises(ValueError):
        outputpackage.OutputPackageBase.from_package(packages=[packagev1, package_b])


def test_outputpackagebase_from_packagev1_raise_on_pkgtype_mismatch(
    packagev1_pkginfov2: Package,
    caplog: LogCaptureFixture,
) -> None:
    caplog.set_level(DEBUG)

    package_b = deepcopy(packagev1_pkginfov2)
    package_b.pkginfo.name = "different"  # type: ignore[attr-defined]
    package_b.pkginfo.xdata = [PkgType(pkgtype=PkgTypeEnum.DEBUG)]  # type: ignore[attr-defined]
    with raises(ValueError):
        outputpackage.OutputPackageBase.from_package(packages=[packagev1_pkginfov2, package_b])


@mark.parametrize(
    "output_package_base_type, expectation",
    [
        ("1", does_not_raise()),
        ("base", raises(RuntimeError)),
    ],
)
def test_outputpackagebase_add_packages(
    outputpackagebasev1: outputpackage.OutputPackageBaseV1,
    outputpackagev1: outputpackage.OutputPackageV1,
    output_package_base_type: str,
    expectation: ContextManager[str],
) -> None:
    match output_package_base_type:
        case "base":
            model = outputpackage.OutputPackageBase()
            input_ = outputpackage.OutputPackage()
        case "1":
            model = outputpackagebasev1
            input_ = outputpackagev1

    with expectation:
        model.add_packages(packages=[input_])


def test_outputpackagebase_get_version() -> None:
    model = outputpackage.OutputPackageBase()
    with raises(RuntimeError):
        model.get_version()


def test_export_schemas(tmp_path: Path) -> None:
    outputpackage.export_schemas(output=str(tmp_path))
    outputpackage.export_schemas(output=tmp_path)

    with raises(RuntimeError):
        outputpackage.export_schemas(output="/foobar")

    with raises(RuntimeError):
        outputpackage.export_schemas(output=Path("/foobar"))


@mark.parametrize(
    "buildinfo_version, expectation",
    [
        (1, does_not_raise()),
        (2, does_not_raise()),
        (9999, raises(RuntimeError)),
    ],
)
def test_outputbuildinfo_from_buildinfo(
    buildinfo_version: int,
    expectation: ContextManager[str],
    valid_buildinfov1: BuildInfo,
    valid_buildinfov2: BuildInfo,
) -> None:
    match buildinfo_version:
        case 1:
            buildinfo = valid_buildinfov1
        case 2:
            buildinfo = valid_buildinfov2
        case 9999:
            buildinfo = BuildInfoV9999()

    with expectation:
        outputbuildinfo = outputpackage.OutputBuildInfo.from_buildinfo(buildinfo=buildinfo)

        match buildinfo_version:
            case 1:
                assert isinstance(outputbuildinfo, outputpackage.OutputBuildInfoV1)  # nosec: B101
            case 2:
                assert isinstance(outputbuildinfo, outputpackage.OutputBuildInfoV2)  # nosec: B101
