# Config Import/Export Implementation Plan

## Goal

Add the ability to import and export NVDA's configuration as a `.nvda-config` zip bundle, including optional add-on inclusion. The system must be forward-compatible via a versioned manifest.

## Key Design Decisions

* **Zip-based format** with a JSON manifest at the root.
* **Allowlist approach**: explicitly include known config paths rather than excluding unwanted ones. Unknown files are ignored, making the format forward-compatible by default.
* **Add-ons are included as their extracted directories** (not `.nvda-addon` bundles, since those aren't retained post-install). Add-on metadata is recorded in the manifest for potential future re-download-from-store support.
* **Config and add-on settings are exported together** — there's no practical way to separate add-on settings from core settings in `nvda.ini`/profiles. NVDA already handles missing synths/drivers via fallback, so orphan settings are inert.
* **`addonsState.json` is sanitized on import**: keep `disabledAddons` and `overrideCompatibility`, strip all pending/transient categories (`pendingInstallsSet`, `pendingRemovesSet`, `pendingEnableSet`, `pendingDisableSet`, `PENDING_OVERRIDE_COMPATIBILITY`, `blocked`).

## Manifest Format (`manifest.json`)

```json
{
  "formatVersion": 1,
  "createdAt": "2026-04-14T10:30:00+00:00",
  "nvdaVersion": "2026.2",
  "configSchemaVersion": 22,
  "contents": {
    "config": true,
    "addons": true,
    "speechDicts": true
  },
  "addons": [
    {
      "id": "exampleAddon",
      "version": "1.2.0",
      "channel": "stable",
      "sideloaded": false
    }
  ]
}
```

* `formatVersion`: integer, bundle format version. Importers refuse versions they don't understand.
* `createdAt`: ISO 8601 with timezone.
* `nvdaVersion`: from `buildVersion.version`, informational only.
* `configSchemaVersion`: from `configSpec.latestSchemaVersion`. Allows compatibility check without parsing `nvda.ini`.
* `contents`: map of component names to booleans. Old importers ignore unknown keys.
* `addons`: metadata list from installed add-on manifests. `sideloaded` flag supports future re-download logic.

## Bundle Structure

```
manifest.json
config/
  nvda.ini
  gestures.ini
  profileTriggers.ini
  profiles/
    *.ini
speechDicts/
  default.dic
  voiceDicts.v1/
    *.dic
symbols/
  symbols-*.dic
addons/
  addonName/
    manifest.ini
    ...
addonsState.json
```

## Allowlist (included)

* `nvda.ini` — core config
* `profiles/*.ini` — configuration profiles
* `gestures.ini` — custom gesture bindings
* `profileTriggers.ini` — profile-to-app mappings
* `speechDicts/` — user speech dictionaries
* `symbols-*.dic` — custom symbol pronunciation
* `addons/` tree — installed add-ons (optional)
* `addonsState.json` — add-on state (sanitized)

## Excluded

* `updateCheckState.pickle` — machine-specific update state
* `guiState.ini` — window positions, machine-specific
* `addonStore/` — cache/download temp data
* `updates/` — pending NVDA update files
* `remoteAccess/` — TLS certs/keys, security-sensitive
* `scratchpad/` — developer tool, not user config
* `addonsState.pickle` — legacy format
* `__pycache__/` — compiled bytecode

## Implementation Phases

### Phase 1: Format Definition

New module `source/config/portConfig/`:

* `manifest.py` — dataclass/TypedDict for manifest schema, `FORMAT_VERSION = 1`, file extension constant, JSON serialization/validation.
* `_allowlist.py` — included paths/globs, single source of truth for bundle contents.

### Phase 2: Export (`export.py`)

1. Collect allowlisted files from config directory.
2. Build `addons` manifest entries from installed add-on manifests; determine sideloaded status.
3. Build full manifest dict.
4. Write into `zipfile.ZipFile` (ZIP_DEFLATED), manifest first.
5. Skip add-ons pending removal. Skip `__pycache__/` in add-on trees.
6. Accept output path and optional include-addons flag.

### Phase 3: Import (`import_.py`)

1. Validate zip: no path traversal (`..`), no symlinks, reasonable uncompressed size.
2. Read/validate `manifest.json`: refuse if `formatVersion > FORMAT_VERSION`.
3. Check `configSchemaVersion` against `configSpec.latestSchemaVersion`; warn if higher.
4. Extract config files into config directory (back up current files first).
5. Sanitize `addonsState.json` (strip pending categories).
6. Extract add-on directories; mark newly imported add-ons as pending install.
7. Prompt for restart.

### Phase 4: GUI

* Export: menu item (Tools or new submenu), save-file dialog with `.nvda-config`, checkbox for include-addons, progress indication.
* Import: menu item, open-file dialog, validation summary with confirmation, restart prompt.
* Register `.nvda-config` extension in `config/registry.py` alongside `.nvda-addon`.

### Phase 5: Testing

* Unit: manifest serialization/validation, allowlist logic, zip validation (path traversal, oversize, missing manifest), `addonsState.json` sanitization.
* Integration: round-trip export/import, importing higher `formatVersion` (refuse), importing older `configSchemaVersion` (upgrade).
