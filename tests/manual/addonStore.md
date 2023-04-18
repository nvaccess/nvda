
## Browsing add-ons

### Browse add-ons by status
Add-ons can be filtered by status.

1. Open the add-on store
1. Jump to the filter-by status field (`alt+s`)
1. Filter by each status, ensure expected add-ons are displayed.
    - all add-ons: should include all add-ons, installed and available for install
    - installed
    - updatable: should include installed add-ons which can be updated or replaced by an add-on store version
    - disabled: should include manually disabled add-ons and add-ons disabled due to incompatibility
    - available: should include add-ons available for install

### Filtering by add-on information
Add-ons can be filtered by display name, publisher and description.

1. Open the add-on store
1. Jump to the filter-by text field (`alt+f`)
1. Search for a string, for example part of a publisher name, display name or description.
1. Ensure expected add-ons appear after the filter view refreshes.
1. Remove the filter-by string
1. Ensure the list of add-ons refreshes to all add-ons, unfiltered.

### Filtering where no add-ons are found
1. Open the add-on store
1. Jump to the filter-by text field (`alt+f`)
1. Search for a string which yields no add-ons.
1. Ensure the add-on information dialog  states "no add-on selected".


## Installing add-ons

### Install add-on from add-on store
1. Open the add-on store.
1. Select an add-on.
1. Navigate to and press the install button for the add-on.
1. Exit the dialog
1. Restart NVDA as prompted.
1. Confirm the add-on is listed in the add-ons manager.

### Install add-on from external source in add-on store
1. Open the add-on store.
1. Jump to the install from external source button (`alt+i`)
1. Find an `*.nvda-addon` file, and open it
1. Proceed with the installation

### Install and override incompatible add-on from add-on store
1. Open the add-on store.
1. Find an add-on listed as "incompatible" for download.
1. Navigate to and press the "install (override compatibility)" button for the add-on.
1. Confirm the warning message about add-on compatibility.
1. Proceed with the installation.

### Install and override incompatible add-on from external source
1. Start the install of an incompatible add-on bundle.
You can do this by:
    - opening an `.nvda-addon` file while NVDA is running
    - using the "install from external source" button
1. Confirm the warning message about add-on compatibility.
1. Proceed with the installation.

### Enable and override compatibility for an installed add-on
1. Browse incompatible disabled add-ons in the add-on store
1. Press enable on a disabled add-on
1. Confirm the warning message about add-on compatibility.
1. Exit the add-on store dialog
1. You should be prompted for restart, restart NVDA
1. Confirm the add-on is enabled in the add-ons manager


## Updating add-ons

### Updating from add-on installed from add-on store
1. [Install an add-on from the add-on store](#install-add-on)
For example: "Clock".
1. Go to your NVDA user configuration folder:
    - For source: `.\source\userConfig`
    - For installed copies: `%APPDATA%\nvda`
1. To spoof an old release, we need to edit 2 files:
    - Add-on store JSON metadata
        - Located in: `.\addonStore\addons\`.
        - Example: `source\userConfig\addonStore\addons\clock.json`
        - Edit "addonVersionNumber" and "addonVersionName": decrease the major release value number.
    - Add-on manifest
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
    - Add-on store JSON metadata
        - Located in: `.\addonStore\addons\`.
        - Example: `source\userConfig\addonStore\addons\clock.json`
      - Delete this file.
    - Add-on manifest
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
    - Add-on store JSON metadata
        - Located in: `.\addonStore\addons\`.
        - Example: `source\userConfig\addonStore\addons\clock.json`
        - Delete this file.
    - Add-on manifest
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


## Other add-on actions

### Disabling an add-on
1. Find a running add-on in the add-on store
1. Press the disable button
1. Exit the add-on store dialog
1. You should be prompted for restart, restart NVDA
1. Confirm the add-on is disabled in the add-ons manager

### Enabling an add-on
1. Find a disabled add-on in the add-on store
1. Press the enable button
1. Exit the add-on store dialog
1. You should be prompted for restart, restart NVDA
1. Confirm the add-on is disabled in the add-ons manager

### Removing an add-on
1. Find an installed add-on in the add-on store
1. Press the remove button
1. Exit the add-on store dialog
1. You should be prompted for restart, restart NVDA
1. Confirm the add-on is removed in the add-ons manager

### Browse an add-ons help
1. Find an installed add-on in the add-on store
1. Press the "add-on help" button
1. A window should open with the help documentation
