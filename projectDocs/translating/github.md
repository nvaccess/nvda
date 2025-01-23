# Translating Symbols, Character Descriptions and Gestures on GitHub

## Background

This guide provides technical steps on how to translate symbols and character descriptions, and localize gestures via GitHub.

For detailed information on the format of these files, please refer to the following pages in the developer guide:

- `characterDescriptions.dic`: [Translating Character Descriptions](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#characterDescriptions)
- `symbols.dic`: [Translating Symbols](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#symbolPronunciation)
- `gestures.ini`: [Translating Gestures](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#TranslatingGestures)

To keep these files up to date, translators must be concious of changes in NVDA.
For changes to `symbols.dic` and `characterDescriptions.dic`, please subscribe to the [nvda-l10n](https://groups.google.com/a/nvaccess.org/g/nvda-l10n) mailing list.
When changes to these files in English occur, you will be notified via this mailing list.
This allows you to consider adding equivalent descriptions to your localised file.

For changes to NVDA's input gestures, please refer to the [latest changes in NVDA](../../user_docs/en/changes.md).
New gestures will be announced there, and localisations can be added to `gestures.ini` if required.

## Process

1. Find the relevant file to edit in the GitHub directory
    - Visit [source/locale](https://github.com/nvaccess/nvda/tree/master/source/locale)
    - Open the directory with your language code
        - English example: <https://github.com/nvaccess/nvda/tree/master/source/locale/en>
        - Format (replace `{lang}`): `https://github.com/nvaccess/nvda/tree/master/source/locale/{lang}`
    - Find the relevant file:
        - `symbols.dic`, `characterDescriptions.dic` or `gestures.ini`
        - English example: <https://github.com/nvaccess/nvda/blob/master/source/locale/en/symbols.dic>
        - Format (replace `{lang}` and `{fileName}`): `https://github.com/nvaccess/nvda/blob/master/source/locale/{lang}/{fileName}`
1. If the relevant file doesn't exist yet, create a new one.
    - To create a new file use the "add file" button from your language's directory.
        - English example: <https://github.com/nvaccess/nvda/new/master/source/locale/en>
        - Format (replace `{lang}`): `https://github.com/nvaccess/nvda/new/master/source/locale/{lang}`
    - `characterDescriptions.dic`: Copy and paste desired contents from the [English example](https://raw.githubusercontent.com/nvaccess/nvda/refs/heads/master/source/locale/en/characterDescriptions.dic).
    Note you should translate all the content you copy.
    - `symbols.dic`: Copy and paste desired contents from the [English example](https://raw.githubusercontent.com/nvaccess/nvda/refs/heads/master/source/locale/en/symbols.dic).
    Note you should translate all the content you copy.
    - `gestures.ini`: This file doesn't require a base file, gestures can be added as needed.
1. Edit the relevant file
    - Tab to the "edit file" button to open the editor for the file.
    - English example: <https://github.com/nvaccess/nvda/edit/master/source/locale/en/symbols.dic>
    - Format (replace `{lang}` and `{fileName}`): `https://github.com/nvaccess/nvda/edit/master/source/locale/{lang}/{fileName}`
    - Refer to [background](#background) for more information on the format of the files
1. Submit your changes
    - Press the "commit changes" button.
    - Update the commit message to add your language to the end: "Update filename for language"
    - Press "Propose changes"
    - A new window should open proposing your changes
    - The proposal will contain a description with a large template.
    Feel free to ignore or delete it.
    - Press "Create pull request".
1. Await feedback from NV Access
    - NV Access will provide feedback if any further work is required.
    - You will receive a notification when your proposal is accepted - the request will be merged and closed.
    - After merging, the changes will become available in [alpha builds](https://www.nvaccess.org/files/nvda/snapshots/) for testing.
