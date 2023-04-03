
## Browsing add-ons
TODO

### Filtering by add-on information

Add-ons can be filtered by display name, publisher and description.

1. Open the add-on store
1. Jump to the filter-by field (`alt+f`)
1. Search for a string, for example part of a publisher name, display name or description.
1. Ensure expected add-ons appear after the filter view refreshes.
1. Remove the filter-by string
1. Ensure the list of add-ons refreshes to all add-ons, unfiltered.

### Filtering where no add-ons are found

1. Open the add-on store
1. Jump to the filter-by field (`alt+f`)
1. Search for a string which yields no add-ons.
1. Ensure the add-on information dialog  states "no add-on selected".


## Installing add-ons

### Install add-on
1. Open the add-on store.
1. Select an add-on.
1. Navigate to and press the install button for the add-on.
1. Exit the dialog
1. Restart NVDA as prompted.
1. Confirm the add-on is listed in the add-ons manager.

### Overriding incompatible add-on from add-on store
TODO

### Overriding incompatible add-on from external install
TODO


## Updating add-ons

### Updating from add-on installed from add-on store
1. [Install an add-on from the add-on store](#install-add-on)
For example: "Clock".
1. Go to your NVDA user configuration folder:
  - For source: `.\source\userConfig`
  - For installed copies: `%APPDATA%\nvda`
1. To spoof an old release, we need to edit 2 files:
  1. Add-on store JSON metadata
    - Located in: `.\addonStore\addons\`.
    - Example: `source\userConfig\addonStore\addons\clock.json`
    - Edit "addonVersionNumber" and "addonVersionName": decrease the major release value number.
  1. Add-on manifest
    - Located in: `.\addons\`.
    - Example: `source\userConfig\addons\clock\manifest.ini`
    - Edit "version": decrease the major release value number to match earlier edits.
1. Open the add-on store
1. Ensure the same add-on you edited is available on the add-on store with the status "update".
1. Install the add-on again to test the "update" path.

### Updating from add-on installed externally with valid version
1. [Install an add-on from the add-on store](#install-add-on)
For example: "Clock".
1. Go to your NVDA user configuration folder:
  - For source: `.\source\userConfig`
  - For installed copies: `%APPDATA%\nvda`
1. To spoof an externally loaded older release, we need to edit 2 files:
  1. Add-on store JSON metadata
    - Located in: `.\addonStore\addons\`.
    - Example: `source\userConfig\addonStore\addons\clock.json`
    - Delete this file.
  1. Add-on manifest
    - Located in: `.\addons\`.
    - Example: `source\userConfig\addons\clock\manifest.ini`
    - Edit "version": decrease the major release value number to match earlier edits.
1. Open the add-on store
1. Ensure the same add-on you edited is available on the add-on store with the status "update".
1. Install the add-on again to test the "update" path.

### Migrating from add-on installed externally with invalid version
This tests a path where an add-on was previously installed, but we are uncertain of the version.
This means using the latest add-on store version might be a downgrade or sidegrade.

1. [Install an add-on from the add-on store](#install-add-on)
For example: "Clock".
1. Go to your NVDA user configuration folder:
  - For source: `.\source\userConfig`
  - For installed copies: `%APPDATA%\nvda`
1. To spoof an externally loaded release, with an invalid version, we need to edit 2 files:
  1. Add-on store JSON metadata
    - Located in: `.\addonStore\addons\`.
    - Example: `source\userConfig\addonStore\addons\clock.json`
    - Delete this file.
  1. Add-on manifest
    - Located in: `.\addons\`.
    - Example: `source\userConfig\addons\clock\manifest.ini`
    - Edit "version": to something invalid e.g. "foo".
1. Open the add-on store
1. Ensure the same add-on you edited is available on the add-on store with the status "Migrate to add-on store".
1. Install the add-on again to test the "migrate" path.

### Updating multiple add-ons
1. Use the steps for updating a single add-on, to create a scenario where multiple add-ons are ready for an update.
1. Press "Update All" (TODO)

### Automatic updating
TODO
