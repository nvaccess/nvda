# Updating NVDA from 32-bit to 64-bit

## Objective

Ensure a smooth transition from the 32-bit version of NVDA to the 64-bit version.
Verify proper cleanup of the x86 directory and ensure 32-bit Windows systems do not receive update prompts for the 64-bit version.

## Additional Notes

* Ensure testing on various Windows versions (i.e. Windows 8.1, Windows 10 and Windows 11).
* Validate that user settings and configurations are preserved during the update process.

## Test Cases

### 1. Update on 64-bit Windows

#### Preconditions

* Install a 32-bit version of NVDA on a 64-bit Windows system.
* Consider testing both the last 32-bit version of NVDA and a significantly older 32-bit version of NVDA.

#### Steps

1. Trigger the update process to the 64-bit version of NVDA.
    1. Ensure the automatic update check returns the 64bit version.
    2. Test a manual update by downloading the installer manually.
2. Verify that the update completes successfully.
3. Check that the "Program Files (x86)/NVDA" directory is removed after the update.
4. Confirm that the 64-bit version of NVDA is installed and functional.

#### Expected Results

* The update completes without errors.
* The x86 directory is cleaned up.
* NVDA runs as a 64-bit application.

### 2. Update on 32-bit Windows

#### Preconditions

* Install the 32-bit version of NVDA on a 32-bit Windows system.

#### Steps

1. Check for updates via the automatic update check mechanism.
2. Verify that no prompt is shown to update to the 64-bit version.

#### Expected Results

* No update prompt is displayed for the 64-bit version.
* NVDA continues to function as a 32-bit application.

### 3. Manual Installation of 64-bit NVDA on 32-bit Windows

#### Preconditions

* Use a 32-bit Windows system.

#### Steps

1. Attempt to manually install the 64-bit version of NVDA.
2. Observe the behavior during the installation process.

#### Expected Results

* The installer prevents the installation of the 64-bit version on a 32-bit system.
* An appropriate error message is displayed.
