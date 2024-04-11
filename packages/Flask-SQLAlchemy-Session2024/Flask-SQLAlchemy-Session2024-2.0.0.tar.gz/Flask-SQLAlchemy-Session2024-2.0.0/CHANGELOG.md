# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [2.0] - 2024-04-11

### Changed

- Fork package and rename due to inactive upstream.
- Rewrite class to stop using deprecated Flask API (`_app_ctx_stack`). Thanks to
  https://github.com/vincent-olivert-riera and https://github.com/schettino72
  for contributing PRs (in the original project) which inspired this rewrite.
- Reformat changelog.

### Removed

- Remove `__version__` as it used to contain a floating-point number. If you
  need the version at runtime then you can use something like
  `pkg_resources.get_distribution('Flask-SQLAlchemy-Session2024').version`
  (see https://stackoverflow.com/a/32965521).

## [1.1] - 2015-05-31

### Added

- Add support for Python 2.6-3.4, pypy, and SQL Alchemy 0.9-1.0.

## [1.0] - 2015-02-16

### Added

- First release.
