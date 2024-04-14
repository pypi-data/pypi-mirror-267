"""Handling of package files and their contents."""

from __future__ import annotations

from base64 import b64encode
from hashlib import md5, sha256
from logging import debug, info
from pathlib import Path
from typing import Any

from orjson import OPT_APPEND_NEWLINE, OPT_INDENT_2, OPT_SORT_KEYS, dumps
from pydantic import BaseModel, SerializeAsAny

from repod.common.models import CSize, FileName, Md5Sum, PgpSig, Sha256Sum
from repod.errors import RepoManagementFileError
from repod.files.buildinfo import BuildInfo
from repod.files.common import extract_file_from_tarfile, names_in_tarfile, open_tarfile
from repod.files.mtree import MTree
from repod.files.pkginfo import PkgInfo

PACKAGE_VERSIONS = {
    1: {
        "required": {".BUILDINFO", ".MTREE", ".PKGINFO"},
    },
    2: {
        "required": {".BUILDINFO", ".MTREE", ".PKGINFO"},
    },
}


class Package(BaseModel):
    """Package representation.

    This is a template class and (apart from its class methods) should not be used directly. Instead instatiate one of
    the classes derived from it.
    """

    @classmethod
    async def from_file(cls, package: Path, signature: Path | None = None) -> Package:
        """Create a Package from a package file and an optional signature.

        Parameters
        ----------
        package: Path
            The path to a package file
        signature: Path | None
            The optional path to a signature file for package

        Raises
        ------
        RepoManagementFileError
            If the signature file does not match the package file.
            If the signature file does not exist.

        Returns
        -------
        Package
            A Package representing the metadata contained in package and the optional signature file
        """
        package_version = 0
        package_md5sum = ""
        package_sha256sum = ""
        pgpsig: str | None = None

        if signature:
            debug(f"Opening signature file {signature} for reading...")
            if not Path(str(package) + ".sig") == signature:
                raise RepoManagementFileError(
                    f"The signature file for {package} should be {str(package) + '.sig'}, but {signature} is provided!"
                )
            if not signature.exists():
                raise RepoManagementFileError(f"The signature file {signature} does not exist!")

            with open(signature, "rb") as signature_file:
                pgpsig = b64encode(signature_file.read()).decode("utf-8")
                debug(f"Created pgpsig: {pgpsig}")
        else:
            info(f"No signature file for package {package} provided, commencing without...")

        debug(f"Creating checksums for package {package}...")
        with open(package, "rb") as package_file:
            package_bytes = package_file.read()
            # NOTE: MD5 sums are still part of the PackageV1 API
            package_md5sum = md5(package_bytes).hexdigest()  # nosec: B324
            package_sha256sum = sha256(package_bytes).hexdigest()

        debug(f"Opening package file {package} for reading...")
        with open_tarfile(package) as tarfile:
            for version in range(len(PACKAGE_VERSIONS), 0, -1):
                debug(f"Testing data against Package version {version}...")
                if names_in_tarfile(tarfile=tarfile, names=PACKAGE_VERSIONS[version]["required"]):
                    debug(f"Package version {version} matches provided data!")
                    package_version = version
                    break

            match package_version:
                case 1:
                    return PackageV1(
                        buildinfo=BuildInfo.from_file(
                            data=await extract_file_from_tarfile(  # type: ignore[arg-type]
                                tarfile=tarfile,
                                file=".BUILDINFO",
                                as_stringio=True,
                            )
                        ),
                        csize=package.stat().st_size,
                        filename=package.name,
                        md5sum=package_md5sum,
                        mtree=MTree.from_file(
                            data=await extract_file_from_tarfile(  # type: ignore[arg-type]
                                tarfile=tarfile,
                                file=".MTREE",
                                as_stringio=True,
                                gzip_compressed=True,
                            ),
                        ),
                        pgpsig=pgpsig,
                        pkginfo=PkgInfo.from_file(
                            data=await extract_file_from_tarfile(  # type: ignore[arg-type]
                                tarfile=tarfile,
                                file=".PKGINFO",
                                as_stringio=True,
                            ),
                        ),
                        sha256sum=package_sha256sum,
                    )
                case 2:
                    return PackageV2(
                        buildinfo=BuildInfo.from_file(
                            data=await extract_file_from_tarfile(  # type: ignore[arg-type]
                                tarfile=tarfile,
                                file=".BUILDINFO",
                                as_stringio=True,
                            )
                        ),
                        csize=package.stat().st_size,
                        filename=package.name,
                        mtree=MTree.from_file(
                            data=await extract_file_from_tarfile(  # type: ignore[arg-type]
                                tarfile=tarfile,
                                file=".MTREE",
                                as_stringio=True,
                                gzip_compressed=True,
                            ),
                        ),
                        pgpsig=pgpsig,
                        pkginfo=PkgInfo.from_file(
                            data=await extract_file_from_tarfile(  # type: ignore[arg-type]
                                tarfile=tarfile,
                                file=".PKGINFO",
                                as_stringio=True,
                            ),
                        ),
                        sha256sum=package_sha256sum,
                    )
                case _:
                    raise RepoManagementFileError(
                        f"The provided file {package} does not match any known package versions!"
                    )

    def top_level_dict(self) -> dict[str, Any]:
        """Flatten the keys and values tracked by Package (one level deep) and return them in a dict.

        NOTE: Duplicate entries are merged!

        Returns
        -------
        dict[str, Any]
            A flattened dict representation of Package
        """
        top_level: dict[str, Any] = {}
        for key, value in self.model_dump(mode="python").items():
            if isinstance(value, dict):
                top_level.update(value)
            else:
                top_level.update({key: value})

        return top_level


class PackageV1(CSize, FileName, Md5Sum, Package, PgpSig, Sha256Sum):
    """Package representation version 1.

    Attributes
    ----------
    buildinfo: BuildInfo
        A .BUILDINFO file representation
    csize: CSize
        The file size of the Package
    filename: FileName
        The filename of the Package
    md5sum: str
        An MD5 checksum for the package
    mtree: MTree
        An .MTREE file representation
    pgpsig: str | None
        An optional PGP signature (in base64 representation) for the package
    pkginfo: PkgInfo
        A .PKGINFO file representation
    sha256sum: str
        A SHA256 checksum for the package
    """

    buildinfo: SerializeAsAny[BuildInfo]
    mtree: SerializeAsAny[MTree]
    pkginfo: SerializeAsAny[PkgInfo]


class PackageV2(CSize, FileName, Package, PgpSig, Sha256Sum):
    """Package representation version 2.

    Attributes
    ----------
    buildinfo: BuildInfo
        A .BUILDINFO file representation
    csize: CSize
        The file size of the Package
    filename: FileName
        The filename of the Package
    mtree: MTree
        An .MTREE file representation
    pgpsig: str | None
        An optional PGP signature (in base64 representation) for the package
    pkginfo: PkgInfo
        A .PKGINFO file representation
    sha256sum: str
        A SHA256 checksum for the package
    """

    buildinfo: SerializeAsAny[BuildInfo]
    mtree: SerializeAsAny[MTree]
    pkginfo: SerializeAsAny[PkgInfo]


def export_schemas(output: Path | str) -> None:
    """Export the JSON schema of selected pydantic models to an output directory.

    Parameters
    ----------
    output: Path
        A path to which to output the JSON schema files

    Raises
    ------
    RuntimeError
        If output is not an existing directory
    """
    classes = [PackageV1, PackageV2]

    if isinstance(output, str):
        output = Path(output)

    if not output.exists():
        raise RuntimeError(f"The output directory {output} must exist!")

    for class_ in classes:
        with open(output / f"{class_.__name__}.json", "wb") as f:
            f.write(
                dumps(
                    class_.model_json_schema(),  # type: ignore[attr-defined]
                    option=OPT_INDENT_2 | OPT_APPEND_NEWLINE | OPT_SORT_KEYS,
                )
            )
