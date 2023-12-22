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
|| Toggle command | ``nvda+shift+e`` |

|| Option || Behaviour ||
| Enabled | behaviour of enabled |
| Disabled | behaviour of disabled |

This setting allows the feature of using functionality in a certain situation to be controlled in some way.
If necessary, a description of a common use case that is supported by each option.
```
