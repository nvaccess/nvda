# User Guide Standards
This document aims to create a standard style guide for writing documentation in the User Guide.

The principles outlined in ["The Documentation System" guide for reference materials](https://documentation.divio.com/reference/) are encouraged when working on the User Guide and this document.

## General standards
- Key commands (e.g. ` ``NVDA+control+upArrow`` `):
  - should be written in lowerCamelCase
  - encapsulated in monospace code-block formatting
  - NVDA should be capitalized
- When referring to Windows terminology, follow the [Windows style guide](https://docs.microsoft.com/en-us/style-guide/welcome/).
  - For instance, instead of "system tray" refer to "notification area"

## Feature settings

Feature flags should be included using the following format.

`FeatureDescriptionAnchor` should not include the settings category.
Once the anchor is set it cannot be updated, while settings may move categories.

```text2tags
==== The name of a feature ====[FeatureDescriptionAnchor]
: Default
  Enabled
: Options
  Default (Enabled), Enabled, Disabled
:

This setting allows the feature of using functionality in a certain situation to be controlled in some way.
If necessary, a description of a common use case that is supported by each option.
```

## Raw HTML inclusion

Including raw HTML may be done by placing it in a "raw area mark", or on a "raw line mark"..
Then, replace each `<` character with `{{`, and each `>` character with `}}`.
More information can be found [in this Txt2Tags tip](https://txt2tags.org/tips.html#html-custom-tags).

Example 1:

```text2tags
""" {{div id="my_div"}}
Something to appear in the div.

""" {{/div}}
```

Example 2:

```text2tags
"""
{{div id="my_other_div"}}
{{p}}something to appear{{br}}
on two lines{{/p}}
{{/div}}
"""
```
