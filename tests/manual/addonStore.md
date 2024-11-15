
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

### Sorting the add-ons list by column
1. Open the Add-on Store
1. Sort by column:
   1. Using the combo-box:
     1. Jump to the sort by column field (`alt+m`)
     1. Select different columns (ascending or descending order)
   1. Alternatively, perform a left mouse click on different columns
1. Ensure that the add-ons list is sorted accordingly
1. Change to different tabs, and repeat the previous steps.

### Failure to fetch add-ons available for download
1. Disable your internet connection
1. Go to your [NVDA user configuration folder](#editing-user-configuration)
1. To delete the current cache of available add-on store add-ons, delete the file: `addonStore\_cachedCompatibleAddons.json`
1. Open the Add-on Store
1. Ensure a warning is displayed: "Unable to fetch latest compatible add-ons"
1. Ensure installed add-ons are still available in the add-on store.


## Installing add-ons

### Install add-on

1. Open the add-on store.
1. Navigate to the available add-ons tab.
1. Select an add-on.
1. Using the context menu, install the add-on.
1. Exit the dialog
1. Restart NVDA as prompted.
1. Confirm the add-ons are listed in the installed add-ons tab of the add-ons store.

### Batch install add-ons

1. Open the add-on store.
1. Navigate to the available add-ons tab.
1. Select multiple add-ons using `shift` and `ctrl`.
1. Using the context menu, install the add-ons.
1. Exit the dialog
1. Restart NVDA as prompted.
1. Confirm the add-ons are listed in the installed add-ons tab of the add-ons store.

### Install add-on from external source

1. Open the add-on store.
1. Jump to the install from external source button (`alt+x`)
1. Find an `*.nvda-addon` file, and open it
1. Proceed with the installation

### Install and override incompatible add-on

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

### Simulate creating an updatable add-on

Without having an installed add-on which has an update pending, it is hard to test updatable add-ons.
This process allows you to mock an update for an add-on.

#### Manual process

1. [Install an add-on from the Add-on Store](#install-add-on)
For example: "Clock".
1. Go to the "addons" folder in your [NVDA user configuration folder](#editing-user-configuration)
1. To mock an old release, we need to edit 2 files:
    - Add-on Store JSON metadata
        - Example: `source\userConfig\addons\clock.json`
        - Edit "addonVersionNumber" and "addonVersionName": decrease the major release value number.
    - Add-on manifest
        - Example: `source\userConfig\addons\clock\manifest.ini`
        - Edit "version": decrease the major release value number to match earlier edits.

#### Using a script
1. [Install an add-on from the Add-on Store](#install-add-on)
For example: "Clock".
1. From PowerShell, call the following script to make the add-on updatable.
  - `tests\manual\createUpdatableAddons.ps1 $addonName $configPath`
  - Replace `$configPath` with your [NVDA user configuration folder](#editing-user-configuration).
  This script defaults to using the installed user config folder in `%APPDATA%`.
  - Example when running from source: `tests\manual\createUpdatableAddons.ps1 clock source\userConfig`
  - Example when running an installed copy: `tests\manual\createUpdatableAddons.ps1 clock`
  - Note this script sets the add-on version to 0.0.0.

### Updating from add-on originally installed via Add-on Store

1. [Simulate creating an updatable add-on](#simulate-creating-an-updatable-add-on)
1. Open the Add-on Store
1. Ensure the same add-on you edited is available on the Add-on Store with the status "update available".
1. Install the add-on again to test the "update" path.

### Updating from add-on installed externally with valid version

1. [Install an add-on from the Add-on Store](#install-add-on)
For example: "Clock".
1. Go to the "addons" folder in your [NVDA user configuration folder](#editing-user-configuration)
1. To mock an externally loaded older release, we need to edit 2 files:
    - Add-on Store JSON metadata
        - Example: `source\userConfig\addons\clock.json`
      - Delete this file.
    - Add-on manifest
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
1. Go to the "addons" folder in your [NVDA user configuration folder](#editing-user-configuration)
1. To mock an externally loaded release, with an invalid version, we need to edit 2 files:
    - Add-on Store JSON metadata
        - Example: `source\userConfig\addons\clock.json`
        - Delete this file.
    - Add-on manifest
        - Example: `source\userConfig\addons\clock\manifest.ini`
        - Edit "version": to something invalid e.g. "foo".
1. Open the add-on store
1. Ensure the same add-on you edited is available on the add-on store with the status "Migrate to add-on store".
1. Install the add-on again to test the "migrate" path.

### Updating multiple add-ons

1. Repeatedly [create updatable add-ons](#simulate-creating-an-updatable-add-on).
1. Open the Add-on Store
1. Ensure the same add-on you edited is available on the Add-on Store with the status "update available".
1. Select multiple add-ons using `shift` and `ctrl`.
1. Using the context menu, install the add-ons.
1. Exit the dialog
1. Restart NVDA when prompted.
1. Confirm the up-to-date add-ons are listed in the installed add-ons tab of the Add-ons Store.

### Automatic update notifications

1. Repeatedly [create updatable add-ons](#simulate-creating-an-updatable-add-on).
1. Start NVDA
1. Ensure Automatic update notifications are enabled in the Add-on Store panel
1. Trigger the update notification manually, or alternatively wait for the notification to occur
    1. From the NVDA Python console, find the scheduled thread
        ```py
        import schedule
        schedule.jobs
        ```
    1. Replace `i` with the index of the scheduled thread to find the job
        ```py
        schedule.jobs[i].run()
        ```
1. Test various buttons:
    - Press "Update All": Ensure NVDA installs the add-ons.
    - Press "Close": Ensure that NVDA prompts for restart if any add-ons have been installed, enabled, disabled or removed
    - Press "Open Add-on Store": Ensure NVDA opens to the Updatable tab in the Add-on Store

### Automatic updating

Full automatic updating is not currently supported.

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

## Using accelerator keys in the GUI

### Add-on list accelerator

1. Select installed add-ons tab
1. Check visually that "a" is underlined in the add-ons list label.
1. Tab to another control and check that `alt+a` allows to move the focus back to the add-ons list.
1. From the "Search" field, tab to the add-ons list and check that "alt+a" is reported
1. When an add-on is focused in the add-on list, check that moving up the navigator object reports the list's name and its shortcut key `alt+a`.
1. Write a non-matching string in "Search" field to empty the list, tab to the list and check that `shift+numpad2` reports the shortcut key.
1. Perform the same tests selecting successively the three other possible tabs (Updatable add-ons, Available add-ons and Incompatible installed add-ons)

### Accelerators for other GUI items

For "Action" button and "Other details" text field controls:
1. Check visually that the letter indicating an accelerator key is underlined on the control's label.
1. Tab to another control and check that `alt+<letter>` allows to move the focus back to the control.
1. From another control tab to the control and check that `alt+<letter>` is reported.
1. In the control, check that `shift+numpad2` reports the shortcut key.

## Updating NVDA

### Updating NVDA with incompatible add-ons

There are several scenarios which need to be tested for updating NVDA with incompatible add-ons.
This is an advanced test scenario which requires 3 versions of NVDA to test with.
Typically, this requires a contributor creating 3 different versions of the same patch of NVDA, with different versions of `addonAPIVersion.CURRENT` and `addonAPIVersion.BACK_COMPAT_TO`
- X.1 e.g `CURRENT=2023.1`, `BACK_COMPAT_TO=2023.1`
- X.2 e.g `CURRENT=2023.2`, `BACK_COMPAT_TO=2023.1`
- (X+1).1 e.g `CURRENT=2024.1`, `BACK_COMPAT_TO=2024.1`


| Test Name | Upgrade from | Upgrade to | Test notes |
|---|---|---|---|
| Upgrade to different NVDA version in the same API breaking release cycle | X.1 | X.1 | Add-ons which remain incompatible are listed as incompatible on upgrading. Preserves state of enabled incompatible add-ons |
| Upgrade to a different but compatible API version | X.1 | X.2 | Add-ons which remain incompatible are listed as incompatible on upgrading. Preserves state of enabled incompatible add-ons |
| Downgrade to a different but compatible API version | X.2 | X.1 | Add-ons which remain incompatible are listed as incompatible on upgrading. Preserves state of enabled incompatible add-ons |
| Upgrade to an API breaking version | X.1 | (X+1).1 | All incompatible add-ons are listed as incompatible on upgrading, overridden compatibility is reset. |
| Downgrade to an API breaking version | (X+1).1 | X.1 | Add-ons which remain incompatible listed as incompatible on upgrading. Preserves state of enabled incompatible add-ons. Add-ons which are now compatible are re-enabled. |

## Miscellaneous

## Editing User Configuration

Where you can find your NVDA user configuration folder:
- For installed copies: `%APPDATA%\nvda`
- For source copies: `source\userConfig`
- Inside a portable copy directory: `userConfig`
