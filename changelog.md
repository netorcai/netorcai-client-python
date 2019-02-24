# Changelog
All notable changes to this project will be documented in this file.  
The format is based on [Keep a Changelog][changelog].

netorcai-client-python adheres to [Semantic Versioning][semver].  
Its public API includes:
- the API of the public functions of the netorcai-client Python library.
- modifications due to netorcai's metaprotocol.

[//]: =========================================================================
## [Unreleased]

[//]: =========================================================================
## [2.0.0] - 2019-02-24 - [netorcai-2.0.0]
### Changed
- Message header is now 32-bit (netorcai metaprotocol update).
- License is now LGPL-3.0 — goal is to allow client programs to be non-GPL.

### Added
- Support for special players (netorcai metaprotocol update).

### Fixed
- `TCP_NODELAY` was not set, which caused a very high latency (x200 locally).

[//]: =========================================================================
## [1.0.1] - 2019-01-02
### Fixed
- Multi-part TCP messages were not read/sent correctly.
  These operations should now be more robust.

[//]: =========================================================================
## 1.0.0 - 2018-12-29
- Initial release.

[//]: =========================================================================
[changelog]: http://keepachangelog.com/en/1.0.0/
[semver]: http://semver.org/spec/v2.0.0.html

[Unreleased]: https://github.com/netorcai/netorcai-client-python/compare/v2.0.0...master
[2.0.0]: https://github.com/netorcai/netorcai-client-python/compare/v1.0.1...v2.0.0
[1.0.1]: https://github.com/netorcai/netorcai-client-python/compare/v1.0.0...v1.0.1

[netorcai-2.0.0]: https://netorcai.readthedocs.io/en/latest/changelog.html#v2-0-0
