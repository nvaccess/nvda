
## Browsing add-ons

### Filter add-ons by channel
Add-ons can be filtered by channel: e.g. stable, beta, dev, external.

1. Open the add-on store
1. Jump to the filter-by channel field (`alt+n`)
1. Filter by each channel grouping, ensure expected add-ons are displayed.

### Filtering by add-on information
Add-ons can be filtered by display name, publisher and description.

1. Open the add-on store
1. Jump to the search text field (`alt+s`)
1. Search for a string, for example part of a publisher name, display name or description.
1. Ensure expected add-ons appear after the filter view refreshes.
1. Remove the filter-by string
1. Ensure the list of add-ons refreshes to all add-ons, unfiltered.

### Filtering where no add-ons are found
1. Open the add-on store
1. Jump to the search text field (`alt+s`)
1. Search for a string which yields no add-ons.
1. Ensure the add-on information dialog  states "no add-on selected".

### Browsing incompatible add-ons available for download
1. Open the Add-on Store
1. Change to the "Available add-ons" tab
1. Enable the "Include incompatible add-ons" filter
1. Ensure add-ons with status "incompatible" are included in the list with the available add-ons.

### Failure to fetch add-ons available for download
1. Disable your internet connection
1. Go to your NVDA user configuration folder:
    - For source: `.\source\userConfig`
    - For installed copies: `%APPDATA%\nvda`
1. To delete the current cache of available add-on store add-ons, delete the file: `addonStore\_cachedCompatibleAddons.json`
1. Open the Add-on Store
1. Ensure a warning is displayed: "Unable to fetch latest compatible add-ons"
1. Ensure installed add-ons are still available in the add-on store.


## Installing add-ons

### Install add-on from add-on store
1. Open the add-on store.
1. Select an add-on.
1. Navigate to and press the install button for the add-on.
1. Exit the dialog
1. Restart NVDA as prompted.
1. Confirm the add-on is listed in the add-ons store.

### Install add-on from external source in add-on store
1. Open the add-on store.
1. Jump to the install from external source button (`alt+x`)
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
1. Confirm the add-on is enabled in the add-ons store

### Failure to download add-on
1. Open the Add-on Store
1. Filter by available add-ons.
1. Disable your internet connection
1. Press install on a cached add-on
1. Ensure a warning is displayed: "Unable download add-on"


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
Updating multiple add-ons at once is currently unsupported.

### Automatic updating
Automatic updating of add-ons is currently unsupported.

## Other add-on actions

### Disabling an add-on
1. Find a running add-on in the add-on store
1. Press the disable button
1. Exit the add-on store dialog
1. You should be prompted for restart, restart NVDA
1. Confirm the add-on is disabled in the add-ons store

### Enabling an add-on
1. Find a disabled add-on in the add-on store
1. Press the enable button
1. Exit the add-on store dialog
1. You should be prompted for restart, restart NVDA
1. Confirm the add-on is disabled in the add-ons store

### Removing an add-on
1. Find an installed add-on in the add-on store
1. Press the remove button
1. Exit the add-on store dialog
1. You should be prompted for restart, restart NVDA
1. Confirm the add-on is removed in the add-ons store

### Browse an add-ons help
1. Find an installed add-on in the add-on store
1. Press the "add-on help" button
1. A window should open with the help documentation
