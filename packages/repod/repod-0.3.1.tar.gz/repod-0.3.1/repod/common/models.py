"""Pydantic models shared throughout the codebase."""

from __future__ import annotations

from pathlib import Path

from email_validator import EmailNotValidError, validate_email
from pydantic import (
    BaseModel,
    HttpUrl,
    NonNegativeInt,
    PositiveInt,
    conint,
    constr,
    field_validator,
)

from repod.common.regex import (
    ARCHITECTURE,
    BASE64,
    EPOCH,
    MD5,
    OPTIONS,
    PACKAGE_FILENAME,
    PACKAGE_NAME,
    PACKAGER_NAME,
    PKGREL,
    SHA256,
    VERSION,
)
from repod.version import alpm


class Arch(BaseModel):
    """A model describing a single 'arch' attribute.

    Attributes
    ----------
    arch: str
        The attribute can be used to describe the (required) data below an %ARCH% identifier in a 'desc' file, which
        identifies a package's architecture
    """

    arch: constr(pattern=f"^{ARCHITECTURE}$")  # type: ignore[valid-type]  # noqa: F722


class Backup(BaseModel):
    """A model describing a single 'backup' attribute.

    Attributes
    ----------
    backup: list[str] | None
        The attribute can be used to describe the (optional) data below a %BACKUP% identifier in a 'desc' file, which
        identifies which file(s) of a package pacman will create backups for
    """

    backup: list[str] | None = None

    @field_validator("backup")
    @classmethod
    def validate_backup(cls, backup: list[str] | None) -> list[str] | None:  # noqa: N805
        """Validate the backup attribute.

        The backup attribute may not contain strings that represent absolute Paths or Paths in the home directory

        Parameters
        ----------
        backup: list[str] | None
            An optional list of strings, representing paths to validate

        Returns
        -------
        list[str] | None
            None if backup is None, empty list if backup is empty list, or a validated list of strings
        """
        if backup:
            for file in backup:
                path = Path(file)
                if path.is_absolute():
                    raise ValueError(f"Absolute paths in a list of files are not valid: {path}")
                parts = path.parts
                if parts[0] == "home" and len(parts) > 1:
                    raise ValueError(
                        f"Files or directories in the home directory is not valid in a list of files: {path}"
                    )

        return backup


class Base(BaseModel):
    """A model describing a single 'base' attribute.

    Attributes
    ----------
    base: str
        The attribute can be used to describe the (required) data below a %BASE% identifier in a 'desc' file, which
        identifies a package's pkgbase
    """

    base: constr(pattern=f"^{PACKAGE_NAME}$")  # type: ignore[valid-type]  # noqa: F722


class BuildDate(BaseModel):
    """A model describing a single 'builddate' attribute.

    Attributes
    ----------
    builddate: int
        The attribute can be used to describe the (required) data below a %BUILDDATE% identifier in a 'desc' file,
        which identifies a package's build date (represented in seconds since the epoch)
    """

    builddate: NonNegativeInt


class CheckDepends(BaseModel):
    """A model describing a single 'checkdepends' attribute.

    Attributes
    ----------
    checkdepends: list[str] | None
        The attribute can be used to describe the (optional) data below a %CHECKDEPENDS% identifier in a 'desc' file,
        which identifies a package's checkdepends
    """

    checkdepends: list[str] | None = None


class Conflicts(BaseModel):
    """A model describing a single 'conflicts' attribute.

    Attributes
    ----------
    conflicts: list[str] | None
        The attribute can be used to describe the (optional) data below a %CONFLICTS% identifier in a 'desc' file, which
        identifies what other package(s) a package conflicts with
    """

    conflicts: list[str] | None = None


class CSize(BaseModel):
    """A model describing a single 'csize' attribute.

    Attributes
    ----------
    csize: int
        The attribute can be used to describe the (required) data below a %CSIZE% identifier in a 'desc' file, which
        identifies a package's size
    """

    csize: NonNegativeInt


class Depends(BaseModel):
    """A model describing a single 'depends' attribute.

    Attributes
    ----------
    depends: list[str] | None
        The attribute can be used to describe the (optional) data below a %DEPENDS% identifier in a 'desc' file, which
        identifies what other package(s) a package depends on
    """

    depends: list[str] | None = None


class Desc(BaseModel):
    """A model describing a single 'desc' attribute.

    Attributes
    ----------
    desc: str
        The attribute can be used to describe the (required) data below a %DESC% identifier in a 'desc' file, which
        identifies a package's description
    """

    desc: str


class FileName(BaseModel):
    """A model describing a single 'filename' attribute.

    Attributes
    ----------
    filename: str
        The attribute can be used to describe the (required) data below a %FILENAME% identifier in a 'desc' file, which
        identifies a package's file name
    """

    filename: constr(pattern=f"^{PACKAGE_FILENAME}$")  # type: ignore[valid-type]  # noqa: F722


class FileList(BaseModel):
    """A model describing an optional list of files.

    Attributes
    ----------
    files: list[str] | None
        The attribute can be used to describe the (optional) data below a %FILES% identifier in a 'files' file, which
        identifies which file(s) belong to a package
    """

    files: list[str] | None = None

    @field_validator("files")
    @classmethod
    def validate_files(cls, files: list[str] | None) -> list[str] | None:  # noqa: N805
        """Validate the files attribute.

        The files attribute may not contain strings that represent absolute Paths or Paths in the home directory

        Parameters
        ----------
        files: list[str] | None
            An optional list of strings, representing paths to validate

        Returns
        -------
        list[str] | None
            None if files is None, empty list if files is empty list, or a validated list of strings
        """
        if files:
            for file in files:
                path = Path(file)
                if path.is_absolute():
                    raise ValueError(f"Absolute paths in a list of files are not valid: {path}")
                parts = path.parts
                if parts[0] == "home" and len(parts) > 1:
                    raise ValueError(
                        f"Files or directories in the home directory is not valid in a list of files: {path}"
                    )

        return files


class Groups(BaseModel):
    """A model describing a single 'groups' attribute.

    Attributes
    ----------
    groups: list[str] | None
        The attribute can be used to describe the (optional) data below a %GROUPS% identifier in a 'desc' file, which
        identifies a package's groups
    """

    groups: list[constr(pattern=f"^{PACKAGE_NAME}$")] | None = None  # type: ignore[valid-type]  # noqa: F722


class ISize(BaseModel):
    """A model describing a single 'isize' attribute.

    Attributes
    ----------
    isize: int
        The attribute can be used to describe the (required) data below an %ISIZE% identifier in a 'desc' file, which
        identifies a package's installed size
    """

    isize: NonNegativeInt


class License(BaseModel):
    """A model describing a single 'license' attribute.

    Attributes
    ----------
    license: list[str]
        The attribute can be used to describe the (required) data below a %LICENSE% identifier in a 'desc' file, which
        identifies a package's license(s)
    """

    license: list[str]  # noqa: A003


class MakeDepends(BaseModel):
    """A model describing a single 'makedepends' attribute.

    Attributes
    ----------
    makedepends: list[str] | None
        The attribute can be used to describe the (optional) data below a %MAKEDEPENDS% identifier in a 'desc' file,
        which identifies a package's makedepends
    """

    makedepends: list[str] | None = None


class Md5Sum(BaseModel):
    """A model describing a single 'md5sum' attribute.

    Attributes
    ----------
    md5sum: str
        The attribute can be used to describe the (required) data below an %MD5SUM% identifier in a 'desc' file, which
        identifies a package's md5 checksum
    """

    md5sum: constr(pattern=MD5)  # type: ignore[valid-type]


class Name(BaseModel):
    """A model describing a single 'name' attribute.

    Attributes
    ----------
    name: str
        The attribute can be used to describe the (required) data below a %NAME% identifier in a 'desc' file, which
        identifies a package's name
    """

    name: constr(pattern=f"^{PACKAGE_NAME}$")  # type: ignore[valid-type]  # noqa: F722


class Options(BaseModel):
    """A list of makepkg.conf OPTIONS used during the creation of a package.

    For valid values refer to the OPTIONS subsection in https://man.archlinux.org/man/makepkg.conf.5#OPTIONS

    Attributes
    ----------
    options: list[str] | None
        An optional list of strings representing makepkg.conf OPTIONS used during the creation of a package
    """

    options: list[constr(pattern=rf"^{OPTIONS}$")] | None = None  # type: ignore[valid-type]  # noqa: F722


class Packager(BaseModel):
    """A model describing a single 'packager' attribute.

    Attributes
    ----------
    packager: str
        The attribute can be used to describe the (required) data below a %PACKAGER% identifier in a 'desc' file, which
        identifies a package's packager
    """

    packager: constr(pattern=(rf"^{PACKAGER_NAME}\s<(.*)>$"))  # type: ignore[valid-type]  # noqa: F722

    @field_validator("packager")
    @classmethod
    def validate_packager_has_valid_email(cls, packager: str) -> str:  # noqa: N805
        """Validate that Packager has an email in the UID.

        Parameters
        ----------
        packager: str
            The packager UID string

        Raises
        ------
        ValuError
            If no valid mail is found in packager

        Returns
        -------
        str
            A validated Packager UID string
        """
        email = packager.replace(">", "").split("<")[1]
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValueError(f"The packager email is not valid: {email}\n{e}") from e

        return packager


class PgpSig(BaseModel):
    """A model describing a single 'pgpsig' attribute.

    Attributes
    ----------
    pgpsig: str
        The attribute can be used to describe the (optional) data below a %PGPSIG% identifier in a 'desc' file, which
        identifies a package's PGP signature
    """

    pgpsig: constr(pattern=f"^{BASE64}$") | None = None  # type: ignore[valid-type]  # noqa: F722


class PkgBase(BaseModel):
    """A pkgbase for a package.

    Refer to https://man.archlinux.org/man/PKGBUILD.5.en#PACKAGE_SPLITTING for details on pkgbase

    Attributes
    ----------
    pkgbase: str
        A string representing the pkgbase of a package
    """

    pkgbase: constr(pattern=rf"^{PACKAGE_NAME}$")  # type: ignore[valid-type]  # noqa: F722


class PkgDesc(BaseModel):
    """A model describing a single pkgdesc attribute.

    Attributes
    ----------
    pkgdesc: str
        A string used as package description
    """

    pkgdesc: str


class PkgName(BaseModel):
    """A pkgname of a package.

    Refer to the pkgname section in https://man.archlinux.org/man/PKGBUILD.5.en#OPTIONS_AND_DIRECTIVES for details

    Attributes
    ----------
    pkgname: str
        A string representing the pkgname of a package
    """

    pkgname: constr(pattern=rf"^{PACKAGE_NAME}$")  # type: ignore[valid-type]  # noqa: F722


class Provides(BaseModel):
    """A model describing a single 'provides' attribute.

    Attributes
    ----------
    provides: list[str] | None
        The attribute can be used to describe the (optional) data below a %PROVIDES% identifier in a 'desc' file, which
        identifies what other package(s) a package provides
    """

    provides: list[str] | None = None


class Replaces(BaseModel):
    """A model describing a single 'replaces' attribute.

    Attributes
    ----------
    replaces: list[str] | None
        The attribute can be used to describe the (optional) data below a %REPLACES% identifier in a 'desc' file, which
        identifies what other package(s) a package replaces
    """

    replaces: list[str] | None = None


class SchemaVersionV1(BaseModel):
    """A model describing a schema version 1.

    Attributes
    ----------
    schema_version: PositiveInt
        A schema version - 1 - for a model
    """

    schema_version: conint(ge=1, le=1) = 1  # type: ignore[valid-type]


class SchemaVersionV2(BaseModel):
    """A model describing a schema version 2.

    Attributes
    ----------
    schema_version: PositiveInt
        A schema version - 2 - for a model
    """

    schema_version: conint(ge=2, le=2) = 2  # type: ignore[valid-type]


class Sha256Sum(BaseModel):
    """A model describing a single 'sha256sum' attribute.

    Attributes
    ----------
    sha256sum: str
        The attribute can be used to describe the (required) data below an %SHA256SUM% identifier in a 'desc' file,
        which identifies a package's sha256 checksum
    """

    sha256sum: constr(pattern=SHA256)  # type: ignore[valid-type]


class OptDepends(BaseModel):
    """A model describing a single 'optdepends' attribute.

    Attributes
    ----------
    optdepends: list[str] | None
        The attribute can be used to describe the (optional) data below a %OPTDEPENDS% identifier in a 'desc' file,
        which identifies what other package(s) a package optionally depends on
    """

    optdepends: list[str] | None = None


class Url(BaseModel):
    """A model describing a single 'url' attribute.

    Attributes
    ----------
    url: str
        The attribute can be used to describe the (required) data below a %URL% identifier in a 'desc' file, which
        identifies a package's URL
    """

    url: HttpUrl


class SourceUrl(BaseModel):
    """A URL pointing at sources.

    Attributes
    ----------
    source_url: HttpUrl | None
        An optional url that points at sources (defaults to None)
    """

    source_url: HttpUrl | None = None


class Epoch(BaseModel):
    """A model dscribing a single 'epoch' attribute.

    The epoch denotes a downgrade in version of a given package (a version with an epoch trumps one without)

    Attributes
    ----------
    epoch: PositiveInt | None
        An optional positive integer representing the epoch of a package
    """

    epoch: PositiveInt | None = None


class PkgRel(BaseModel):
    """A model dscribing a single 'pkgrel' attribute.

    The pkgrel denotes the build version of a given package

    Attributes
    ----------
    pkgrel: str
        A string representing the pkgrel (package release version) of a package
    """

    pkgrel: constr(pattern=rf"^{PKGREL}$")  # type: ignore[valid-type]  # noqa: F722


class PkgVer(BaseModel):
    """A model dscribing a single 'pkgver' attribute.

    The pkgver denotes the upstream version of a given package

    Attributes
    ----------
    pkgver: str
        A string representing the pkgver (upstream package version) of a package
    """

    pkgver: constr(pattern=rf"^({VERSION})$")  # type: ignore[valid-type]  # noqa: F722


class Version(BaseModel):
    """A model describing a single 'version' attribute.

    Attributes
    ----------
    version: str
        The attribute can be used to describe the (required) data below a %VERSION% identifier in a 'desc' file, which
        identifies a package's version (this is the accumulation of epoch, pkgver and pkgrel)
    """

    version: constr(pattern=rf"^({EPOCH}|){VERSION}-{PKGREL}$")  # type: ignore[valid-type]  # noqa: F722

    def get_epoch(self: Version) -> Epoch | None:
        """Return the epoch of the version.

        Returns
        -------
        int | None
            An optional string representing the epoch of the version
        """
        if ":" in self.version:
            return Epoch(epoch=self.version.split(":")[0])

        return None

    def get_pkgver(self: Version) -> PkgVer:
        """Return the pkgver of the version.

        Returns
        -------
        PkgVer
            A PkgVer representing the pkgver of the version
        """
        pkgver_pkgrel = self.version.split(":")[1] if ":" in self.version else self.version
        return PkgVer(pkgver=str(pkgver_pkgrel.split("-")[0]))

    def get_pkgrel(self: Version) -> PkgRel:
        """Return the pkgrel of the version.

        Returns
        -------
        PkgRel
            A PkgRel representing the pkgrel of the version
        """
        pkgver_pkgrel = self.version.split(":")[1] if ":" in self.version else self.version
        return PkgRel(pkgrel=str(pkgver_pkgrel.split("-")[1]))

    def vercmp(self: Version, version: Version) -> int:
        """Compare the version with another.

        The comparison algorithm is based on pyalpm's/ pacman's vercmp behavior.
        If PYALPM_VERCMP is True, pyalpm has been imported and its implementation of vercmp() is used.

        Returns
        -------
        int
            -1 if self.version is older than version
            0 if self.version is equal to version
            1 if self.version is newer than version
        """
        return alpm.pkg_vercmp(self.version, version.version)

    def is_older_than(self: Version, version: Version) -> bool:
        """Check whether the version is older than a provided version.

        Parameters
        ----------
        version: Version
            Another version to compare that of self to

        Returns
        -------
        True if self.version is older than the provided version, False otherwise.
        """
        return True if self.vercmp(version=version) < 0 else False

    def is_newer_than(self: Version, version: Version) -> bool:
        """Check whether the version is newer than a provided version.

        Parameters
        ----------
        version: Version
            Another version to compare that of self to

        Returns
        -------
        True if self.version is newer than the provided version, False otherwise.
        """
        return True if self.vercmp(version=version) > 0 else False
