
<a id='changelog-v0.1.0.5'></a>
# v0.1.0.5 — 2023-03-02

## Fixed

- `reload` method wasn't updating file so it doesnt work, now reload also reopens the source file

<a id='changelog-v0.1.0.4'></a>
# v0.1.0.4 — 2023-03-01

## Changed

- Migrate setup.cfg to pyproject.toml
- yapf and flake8 using another configuration
- now loads the file and then load the var, this should make easier for later loads directly a dict instead of a file
- tests fixtures changed to a specific file to clean test file a little

## Fixed

- logger.warn changed to logger.warning as DeprecationWarning warns

<a id='changelog-v0.1.0.3'></a>
# v0.1.0.3 -- 2022-12-15

## Changed

- Changed possible_config_file log level from critical to debug

<a id='changelog-v0.1.0.2'></a>
# v0.1.0.2 -- 2022-12-13

## Changed

- readme example was using wrong import

<a id='changelog-v0.1.0.1'></a>
# v0.1.0.1 -- 2022-12-13

## Added

- First version
