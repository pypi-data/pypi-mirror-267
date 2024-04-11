# sqlfluff-common-conventions

A plugin for rules that enforce common SQL conventions not available in SQLFluff, compatible with BigQuery SQL.

## Rules

- CC01: Start boolean columns with `is_` or `has_`.
- CC02: End datetime, time, and timestamp columns with `_at`.
- CC02: End date columns with `_date`.

## Future expansions

- Improve robustness of evaluation logic
- Make rules compatible with more SQL dialects