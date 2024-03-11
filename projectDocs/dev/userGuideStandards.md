# User Guide Standards
This document aims to create a standard style guide for writing documentation in the User Guide.

The principles outlined in ["The Documentation System" guide for reference materials](https://documentation.divio.com/reference.html) are encouraged when working on the User Guide and this document.

## General standards
- Key commands (e.g. ` ``NVDA+control+upArrow`` `):
  - should be written in lowerCamelCase
  - encapsulated in monospace code-block formatting
  - NVDA should be capitalized
- When referring to Windows terminology, follow the [Windows style guide](https://docs.microsoft.com/en-us/style-guide/welcome/).
  - For instance, instead of "system tray" refer to "notification area"

## Feature settings

Feature flags, comboboxes and checkboxes should be included using the following format.

`FeatureDescriptionAnchor` should not include the settings category.
Once the anchor is set it cannot be updated, while settings may move categories.

```t2t
==== The name of a feature ====[FeatureDescriptionAnchor]

|| Options | Default (Enabled), Enabled, Disabled |
|| Default | Enabled |
|| Toggle command | ``NVDA+shift+e`` |

|| Option || Behaviour ||
| Enabled | behaviour of enabled |
| Disabled | behaviour of disabled |

This setting allows the feature of using functionality in a certain situation to be controlled in some way.
If necessary, a description of a common use case that is supported by each option.
```

## Generation of Key Commands
Generation of the Key Commands document requires certain commands to be included in the User Guide.
These commands must begin at the start of the line and take the form:

```t2t
%kc:command: arg
```

The title command must appear first.
The other commands are used to select content containing key commands to be included into the key commands document.
Appropriate headings from the User Guide will be included implicitly.

### Specifying the title
The `kc:title` command must appear first and specifies the title of the Key Commands document.

For example:
```t2t
%kc:title: NVDA Key Commands
```

### Selecting blocks

The `kc:beginInclude` command begins a block of text which should be included verbatim.
The block ends at the `kc:endInclude` command.

For example:

```t2t
%kc:beginInclude
|| Name | Desktop command | Laptop command | Description |
...
%kc:endInclude
```

### Headers for settings sections

The `kc:settingsSection` command indicates the beginning of a section documenting individual settings.
It specifies the header row for a table summarising the settings indicated by the `kc:setting` command (see below).
In order, it must consist of a name column, a column for each keyboard layout and a description column.

For example:
```t2t
%kc:settingsSection: || Name | Desktop command | Laptop command | Description |
```

### Including a setting

The `kc:setting` command indicates a section for an individual setting.

It must be followed by:

* A heading containing the name of the setting;
* A table row for each keyboard layout, or if the key is common to all layouts, a single line of text specifying the key after a colon;
* A blank line; and
* A line describing the setting.

For example:
```t2t
%kc:setting
==== Braille Tethered To ====
| Desktop command | ``NVDA+control+t`` |
| Laptop Command | ``NVDA+control+t`` |
This option allows you to choose whether the braille display will follow the system focus, or whether it follows the navigator object / review cursor.
```
