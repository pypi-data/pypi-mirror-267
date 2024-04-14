.. _changelog:

=========
Changelog
=========

All notable changes to this project should be documented here.
For more detailed information have a look at the |git log|.

.. _version unreleased:

[Unreleased]
------------

[0.3.1] - 2024-04-13
--------------------

Changed
^^^^^^^

* The test dependency on ``pytest-lazy-fixture`` has been replaced with
  ``pytest-lazy-fixtures``.

Fixed
^^^^^

* The code has been adapted to changes in metadata files in pacman 6.1. Most
  notably, the ``md5sum`` field in repository sync database ``desc`` files has
  been removed, while the ``pgpsig`` field has been made optional. This change
  made the introduction of ``PackageV2``, ``OutputPackageV2`` necessary, while
  ``PackageDescV2`` has been adapted accordingly.
* Various typing related issues have been addressed, that would lead to errors
  in future versions of ``pydantic``.

[0.3.0] - 2023-07-17
--------------------

Added
^^^^^

* A section in the documentation now provides a high-level introduction to how
  repod works as well as examples on how to add packages, write sync databases
  and use a repository with pacman.
* Classes to allow transactional tasks with pre and post checks.
* Write sync databases as part of a transaction.
* The command ``repod-file repo importpkg`` now automatically creates symlinks
  in a subdirectory of a repository's management repository from each package
  name to their respective ``pkgbase``. This allows for easier search by
  package name.
* Checks now ensure that when adding packages (update or new additions) their
  versions will be greater than already existing packages. The checks also
  consider changes to the pkgbase of a package (e.g. ensuring, that a
  previously existing pkgbase providing a package must be updated if a
  package's pkgbase changes).
* Validation of source URLs per ``pkgbase`` against one or several allowed URLs
  is now possible per repository and can be configured using ``repod.conf``.
* The command ``repod-file repo importpkg`` learned a new parameter (``-u``/
  ``--source-url``) with which users may provide lists of ``pkgbase=url``
  strings, that - if matching - are combined with the data gained from consumed
  packages and is used for source URL validation.
* The ``repod.conf`` man page now features information on how to configure
  debug repositories.
* Symlinks in package and managment repositories, that belong to the previous
  versions of packages are now removed when updating packages.
* When adding packages to a stability layer of a repository (e.g. stable,
  testing or staging), the layers above and below are checked, so that pkgbases
  in lower layers do not have a higher version and pkgbases in higher layer do
  not have lower versions than the one being added.
* Checks now ensure that when adding packages the filename of the package and
  the package's info name are the same.
* By default ``repod-file`` now also creates an archive of all packages added
  to a repository. The archiving locations are configurable globally and per
  repository.
* The existence of build requirements of added packages are checked by default
  now (in the archive, the target repository and amongst the added packages),
  unless ``build_requirements_exist`` is set to ``false`` in ``repod.conf``.
  This check fails on missing requirements and thus ensures that added packages
  are fully reproducible.
* Repositories can now be grouped together in the configuration, by assigning
  the same positive integer to them. Packages in grouped repositories are
  unique in the group (no duplicate ``pkgbase`` or ``pkgname`` is allowed).
  Furthermore grouped repositories share the same parent directory for all of
  their management repository directories, the same grandparent directory for
  all of their package repository directories, the same parent directory for
  all of their package pool directories and the same parent directory for all
  of their source pool directories.
* A parser for ``.SRCINFO`` files can now be used to retrieve and validate data
  of these files. This is useful when validating data of packages against the
  data from their source repositories.
* Documentation for tests now provide more context about the various helper
  functions and fixtures. A ``pydocstyle`` based linting of in-code
  documentation now ensures, that documentation follows a common style.
* A logo for repod has been created by Safi @ http://betriebsbuero.com, which
  is licensed under the terms of the CC-BY-SA-4.0.
* A ``Makefile`` can now be used to build and install repod system-wide.

Changed
^^^^^^^

* The command ``repod-file repo importpkg`` now uses transactional tasks, that
  are chained into an atomic action, which automatically reverts itself if any
  of the tasks fail.
* The command ``repod-file repo importpkg`` is now able to import packages of
  differing ``pkgbase``.
* The command ``repod-file repo importpkg`` now automatically also writes the
  sync databases of the repository after adding packages.
* The command ``repod-file repo writedb`` now writes the sync databases in a
  transaction.
* The CLI now automatically checks whether all consumed packages match the
  target repository's CPU architecture.
* Type hints now use generics for the standard containers ``dict``, ``list``,
  ``set`` and ``tuple`` instead of the imports from ``typing``.
* Type hints now use the union operator ``|`` instead of ``Union`` and
  ``Optional``.
* The validation for package and signature filenames relied on regular
  expressions which proved too cumbersome to maintain and extend. The
  validation now relies on regular expressions only for the actual filenames
  and validation for absolute vs. relative paths relies on ``pathlib.Path``.
* The command ``repod-file repo writedb`` now allows writing empty sync databases
  from empty management repositories.
* The definition of workflows (e.g. adding packages, writing sync databases) is
  now done in a separate module and is decoupled from the CLI.
* The ``repod.conf`` man page now covers the ``management_repo`` configuration
  in greater detail.
* The ``format`` field in ``.BUILDINFO`` files maps to a ``SchemaVersionV1`` or
  ``SchemaVersionV2`` rather than a ``FormatV1`` or ``FormatV2``. This provides
  a uniform approach to versioning objects across object types.
* The configuration file now understands ``staging_debug`` and
  ``testing_debug`` options per package repository. Analogous to setting the
  ``debug`` repository name for the stable repository, identified by ``name``,
  the new options are used to set the debug repository names for ``staging``
  and ``testing`` repositories.
* The configuration file now requires, that all directories except the
  ``package_pool`` and ``source_pool`` directories must be unique.
* Use ``tomllib`` on Python 3.11+.
* Use ``pydantic`` version 2.

Fixed
^^^^^

* The parser for mtree files did not zerofill retrieved file modes and as mtree
  may return strings shorter than three chars as a file mode, this led to
  ValidationErrors when initializing MTree objects.
* In the ``repod.conf`` man page, TOML inline tables had been used falsely as
  tables.
* The library (magic) used for detecting the file type of a package file does
  not always return the correct type as its first match, this caused importing
  to fail, if the type was misdetected. All the detected types of the package
  file is now checked for a match.

Removed
^^^^^^^

* The ``justfile`` has been removed in favor of a ``Makefile``.

[0.2.2] - 2022-08-29
--------------------

Fixed
^^^^^

* The implementation of ``PkgInfoV2`` was based on an early patch series
  towards pacman that had been superseded since. Instead of a top-level
  ``pkgtype`` attribute, ``PkgInfoV2`` now tracks an optional set of extended/
  extra data (``xdata``), which is in line with the implementation in pacman.

Changed
^^^^^^^

* Return help strings instead of raising ``RuntimeError`` if no commands are
  provided to ``repod-file`` or any of its subcommands.

[0.2.1] - 2022-08-23
--------------------

Fixed
^^^^^

* The ``justfile`` is now contained in the sdist tarball and fixed to install
  using a destination directory (destdir).

[0.2.0] - 2022-08-22
--------------------

Added
^^^^^

* Man page for ``repod.conf``.
* Per repository debug repository handling in configuration layer and CLI.
* Package verification based on ``pacman-key`` may be configured by setting the
  global configuration option ``package_verification`` to ``pacman-key``.
* A ``PackageDescV2`` which removes the ``%PGPSIG%`` identifier in the ``desc``
  files rendered from it. The default is still ``PackageDescV1`` (which
  provides the ``%PGPSIG%`` identifier), but users may already try the new
  functionality using the ``syncdb_settings.desc_version`` option in
  ``repod.conf`` (see ``man 5 repod.conf``).
* The ``repod.repo.package.repofile`` module provides functionality for file
  operations on repository files (e.g. package files or package signature
  files). The ``RepoFile`` class allows moving, copying, symlinking and
  removing of files.
* The ``repod-file repo importpkg`` subcommand which supersedes ``repod-file
  package import``, while also implementing the addition of package files (and
  optionally their signatures) to a given repository's package pool directory
  and creating the symlinks for them in the repository's package repository
  directory.
* A justfile for installing directories required for system mode and man pages.
* The ``repod-file repo importdb``, ``repod-file repo importpkg`` and
  ``repod-file repo writedb`` commands now accept a ``-a``/ ``--architecture``
  flag to define the target repository architecture, if repositories of the
  same name but differing CPU architectures exist.

Changed
^^^^^^^

* Configuration layer is now used in the CLI and required directories for
  repositories and data are automatically created upon launching it. The
  configuration layer distinguishes between system-wide and per-user locations.
* Extend ``OutputPackageBaseV1`` with optional ``.BUILDINFO`` data retrieved
  from packages using the new ``OutputBuildInfo`` (and child classes). This
  adds a relevant subset of ``.BUILDINFO`` files to the management repository.
* The ``repod-file`` subcommand ``management`` is renamed to ``repo`` and its
  subsubcommands ``import`` and ``export`` are renamed to ``importdb`` and
  ``writedb`` (respectively).
  The ``repod-file repo writedb`` command only accepts the name of the target
  repository and no target file anymore, as the repository sync database files
  are written to the binary package directory of the target repository.
* The email validation done for the ``Packager`` model does not by default
  check for deliverability anymore. In the future this is supposed to become
  configurable.
* The database compression of repositories can now only be set in the
  configuration file.

Fixed
^^^^^

* ``.PKGINFO`` values with equal signs are now handled correctly (e.g., equal
  signs in descriptions of ``optdepends`` entries).
* The ``usersettings`` fixture no longer leaks test state into the user system.
* The calculation of ``SHA-256`` checksums for packages in
  ``repod.file.package.Package.from_file`` were not done correctly, because
  after a previous ``MD5`` checksum calculation the package file was not read
  in its entirety.
* Fix file mode validation for ``.MTREE`` files.
* Fix path validation for ``.MTREE`` files.
* The conversion of special characters in octal representation in the ``mtree``
  files did not work for non-English unicode characters (e.g. cyrillic) and
  attempting to import packages that contain file names with such characters
  would fail.
* Some of the online documentation did not reflect the current state of the CLI
  anymore, so all information for the ``repod-file`` has been consolidated with
  its man page.

Removed
^^^^^^^

* The ``repod-file`` subcommand ``syncdb`` is removed due to being the reverse
  pendant to the ``management`` command.
* The ``repod-file package import`` subcommand as it is superseded by
  ``repod-file repo importpkg``.

[0.1.0] - 2022-07-02
--------------------

Changed
^^^^^^^

* Documentation on installation and dependencies.

[0.1.0-alpha1] - 2022-07-01
---------------------------

Added
^^^^^

* Functionality to validate package files in accordance with current versions
  of ``.BUILDINFO``, ``.MTREE`` and ``.PKGINFO`` files.
* Functionality to validate repository sync databases in accordance with
  current versions of ``desc`` and ``files`` files found in the default and
  files sync databases.
* Functionality to describe the contents of repository sync databases in the
  context of a management repository consisting of JSON files per ``pkgbase``.
* Functionality to export JSON schema which can be used to validate existing
  functionality and data formats.
* A self-validating configuration layer which will be used in upcoming versions
  of the project to allow configuration of a ``repod`` service.
* The commandline utility ``repod-file`` to expose existing functionality for
  package inspection, data transformation and JSON schema export.
* Documentation on internals of the project and the ``repod-file`` commandline
  utility.
* Manual page for ``repod-file``.

.. |git log| raw:: html

  <a target="blank" href="https://man.archlinux.org/man/git-log.1">git log</a>
