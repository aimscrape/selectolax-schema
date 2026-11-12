# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

### Changed

### Fixed

### Removed

## [0.1.1] - 2026-11-12

### Added

- Memory lifecycle regression coverage for retained exceptions, recovered hooks,
  deeply nested HTML, and all four extraction entry points.
- Shared VS Code interpreter, Pylance, and Ruff development settings.

### Changed

- Release preprocessed HTML before evaluating fields and callbacks.
- Clear finished internal traceback locals on failed extraction while preserving
  exception identity, traceback locations, and user callback locals.

### Fixed

- Replace the recursive text collector with iterative traversal to eliminate
  closure reference cycles and Python recursion-limit failures.
- Release parser and DOM references on both successful and failed extraction,
  including callbacks and transforms that catch and retain an exception.
- Avoid retaining object-array nodes through comprehension frames on older Python
  versions and reject invalid top-level fields before constructing a DOM.

### Removed

## [0.1.0] - 2026-11-12

### Added

- Initial selectolax-backed implementation, compatible with the extraction,
  typed-spec, JSON Schema, callback, transform, and CLI behavior of
  `scrapling-schema` 1.1.3.
- Runtime and CLI version reporting derived from installed distribution metadata.
