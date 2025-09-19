# Creating new issues on the NVDA project

This page is meant to serve as an explanation for how to fill out our [GitHub issues](https://github.com/nvaccess/nvda/issues/new/choose).

**Warning**: In all but exceptional circumstances we require one of these templates to be completed.
Your issue will likely be closed if a template has not been followed.

We currently have the following templates:

* For [bug reports](https://github.com/nvaccess/nvda/issues/new?template=1-bug_report.yaml)
* For [feature requests](https://github.com/nvaccess/nvda/issues/new?template=2-feature_request.yaml)
* For [special case issues](https://github.com/nvaccess/nvda/issues/new?template=3-special_case_issue.yaml)
  * Issues that cannot easily be categorised as either a bug report or a feature request
* For [developer facing changes](https://github.com/nvaccess/nvda/issues/new?template=4-developer_facing_changes.yaml):
  * This template is intended for developers to document improvements or maintenance to NVDA's code base that do not have user facing changes.
  * This may include API changes, technical debt removal, refactoring and maintenance tasks.
  * Note there is no further guide for this - it is expected that developers can use the template appropriately.
* For [security vulnerabilities](https://github.com/nvaccess/nvda/security/advisories/new)
  * Please note that these are reported differently, for more information refer to our [disclosure policy/procedure](https://github.com/nvaccess/nvda/blob/master/security.md)

These are a fillable form that guides you through the process of providing the necessary information for your issue.
The "Advanced" version of these templates listed when [choosing templates for new issues](https://github.com/nvaccess/nvda/issues/new/choose) asks for the same information, but in a more free-form manner, with less supporting information.

## Help

If you have trouble following this template, or with the initial investigation that is required, please politely ask for assistance from the fantastic community of people on the [NVDA users mailing list](https://groups.google.com/a/nvaccess.org/g/nvda-users).

## Tips

* Read through the template first in Browse mode before filling it out, to ensure you don't skip over contextual text between form fields.
* The template uses GitHub markdown in multi-line edit controls, to provide formatting for headings, lists, quotes etc.
If you are not familiar, please take some time to learn about [Github markdown](https://guides.github.com/features/mastering-markdown/).
* In multi-line edit boxes, consider switching to the preview tab in order to read through the details and confirm the formatting reads as expected.

## Attachments / Images

It's important to include any files that are required to reproduce an issue.
This might be a required file for an office suite, or a link to a code playground such as CodePen or JSFiddle, or perhaps a standalone HTML file.
Github does not allow all [file types to be attached](https://help.github.com/articles/file-attachments-on-issues-and-pull-requests/), however, zip files are allowed, so you can always zip your file and attach that instead.

### Logs

In most cases an NVDA log file is incredibly helpful when trying to understand/fix an issue, please remember to attach one.
More [instructions are available on the wiki](https://github.com/nvaccess/nvda/wiki/LogFilesAndCrashDumps).
If you are getting a crash dump file (nvda_crash.dmp) please also include it.

### Screenshots

While we welcome **images/screenshots** to help explain a problem, be aware that many of the developers of NVDA are blind and will greatly appreciate this image being described in text.
Most tools allow you to copy text out of them.
