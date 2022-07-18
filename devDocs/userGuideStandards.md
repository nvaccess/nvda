# User Guide Standards
This document aims to create a standard style guide for writing documentation in the User Guide.

The principles outlined in ["The Documentation System" guide for reference materials](https://documentation.divio.com/reference/) are encouraged when working on the User Guide and this document.

## General standards
- Key commands should be lowerCamelCase and encapsulated in monospace code-block formatting.
  - e.g. ` ``NVDA+control+upArrow`` `

## Feature flags

Feature flags should be included using the following format.

```text2tags
==== The name of a feature ====[FeatureDescriptionAnchor]
: Default
  Enabled
: ``NVDA+o``
  Toggle this feature
:

This setting allows the feature of using functionality in a certain situation to be controlled in some way.
If necessary, a description of a common use case that is supported by each option.
```