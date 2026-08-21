# Braille table metadata

NVDA exposes a curated subset of the braille translation tables that ship with [liblouis](https://liblouis.io/).
Metadata for these tables comes from two sources:

* The liblouis table files in `source/louis/tables` carry metadata in their headers, such as `display-name` and `contraction`.
* `source/brailleTables/tables.json` records which tables NVDA exposes and where NVDA's metadata diverges from liblouis metadata.

The `source/brailleTableUtil.py` script merges these sources.
It can generate a Python module of `brailleTables.addTable` calls and report differences between the two sources.
See [#11298](https://github.com/nvaccess/nvda/issues/11298) for the plan to generate the braille tables module this way at build time.

## The tables.json format

A table is exposed by NVDA when its file name is a key in `tables.json`.
The entry for a table only contains metadata that diverges from liblouis metadata:

* `displayName`: the name shown in the braille settings dialog, when it differs from or is absent in the liblouis `display-name` metadata.
* `contracted`: whether the table is contracted, when NVDA disagrees with the liblouis `contraction` metadata.
* `input` / `output`: whether the table is suitable for braille input or output.
Liblouis has no equivalent metadata; both default to true.
* `inputForLangs` / `outputForLangs`: the languages for which the table is the default input or output table.

An empty entry (`{}`) exposes a table entirely based on its liblouis metadata.
Table file names are matched against liblouis metadata case insensitively.

## The brailleTableUtil script

The script is not distributed in binary copies of NVDA; run it from source.
All commands are documented in its help output:

```cmd
uv run python source\brailleTableUtil.py --help
```

### Reporting differences

The `diff` command reports differences between `tables.json` and liblouis metadata as JSON:

```cmd
uv run python source\brailleTableUtil.py diff
```

The report contains three categories:

* `notOptedIn`: liblouis tables that NVDA does not expose.
Tables with the legacy `.tbl` extension are excluded; liblouis is phasing that extension out per table.
* `missingUpstream`: exposed tables without a liblouis table file.
* `unpinCandidates`: recorded divergences that match liblouis metadata again.
These entries can be removed from `tables.json`.

Run this after updating liblouis to find newly available tables and metadata improvements.

### Generating the tables module

The `generate` command generates a braille tables module from `tables.json` and liblouis metadata:

```cmd
uv run python source\brailleTableUtil.py generate tables.py
```

The generated module registers exactly the same tables as `source/brailleTables/__tables.py`.
A unit test asserts this equivalence.

### Dumping metadata

The `builtIn` and `liblouis` commands dump NVDA's braille table registry and liblouis table metadata to JSON:

```cmd
uv run python source\brailleTableUtil.py builtIn builtIn.json
uv run python source\brailleTableUtil.py liblouis liblouis.json
```

### Regenerating tables.json

The `bootstrapOverrides` command regenerates `tables.json` from the current registry and liblouis metadata:

```cmd
uv run python source\brailleTableUtil.py bootstrapOverrides source\brailleTables\tables.json
```

## Keeping the sources in sync

NVDA currently loads its braille tables from `source/brailleTables/__tables.py`.
Every change to that module must be mirrored in `tables.json`.
The `TestGeneratedTablesEquivalence` unit test in `tests/unit/test_brailleTableUtil.py` fails when the two are out of sync.
Run the unit tests to verify:

```cmd
rununittests
```

## Adding a new braille table

1. Run the `diff` command and find the table under `notOptedIn`.
1. Add an `addTable` call for it to `source/brailleTables/__tables.py`.
1. Add an entry for it to `tables.json`.
When the liblouis metadata is complete and matches the `addTable` call, an empty entry (`{}`) suffices.
1. Run the unit tests.
