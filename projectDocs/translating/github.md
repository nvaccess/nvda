# Translating Symbols, Character Descriptions and Gestures on GitHub

## Background

This guide provides technical steps on how to translate symbols and character descriptions, and localize gestures via GitHub.

For detailed information on the format of these files, please refer to the following sections in the developer guide:

- `characterDescriptions.dic`: [Translating Character Descriptions](https://download.nvaccess.org/documentation/developerGuide.html#characterDescriptions)
- `symbols.dic`: [Translating Symbols](https://download.nvaccess.org/documentation/developerGuide.html#symbolPronunciation)
- `gestures.ini`: [Translating Gestures](https://download.nvaccess.org/documentation/developerGuide.html#TranslatingGestures)

To keep these files up to date, translators must be concious of changes in NVDA.
For changes to `symbols.dic` and `characterDescriptions.dic`, please subscribe to the read-only [NVDA localisation mailing list](https://groups.google.com/a/nvaccess.org/g/nvda-l10n).
When changes to these files in English occur, you will be notified via this mailing list.
This allows you to consider adding equivalent descriptions to your localised file.

For changes to NVDA's input gestures, please refer to the [latest changes in NVDA](../../user_docs/en/changes.md).
New gestures will be announced there, and localisations can be added to `gestures.ini` if required.

## Process

1. Be notified of potential localisation changes:
    - For `gestures.ini`: Check the latest beta's changes for any new gestures added.
    - For `symbols.dic` and `characterDescriptions.dic`:
        - Receive a notification from the [NVDA localisation mailing list](https://groups.google.com/a/nvaccess.org/g/nvda-l10n)
        - This will occur when the first beta is being prepared.
        There may be subsequent notifications during the beta period.
        - Changes to these files are relatively infrequent, so the mailing list will be low traffic, many releases may go by without changes.
        - Sample email:
            - The lines prefixed with `+` refer to additions.
            - The lines prefixed with `-` refer to removals.
            - The lines prefixed with `@@` refer to the location of the changes:
                - The first number(s) corresponds to the original location of the line.
                The second number(s) corresponds to the new location in the file.
                This can be useful for finding where to make the changes when referencing the English file.
                - e.g. `@@ -2 +2 @@` means the 2nd line has changed, and remained in the same place in both files.
                - e.g. `@@ -13,0 +14,2 @@ complexSymbols:` means the 13th line has changed, originally there was 0 lines here, and 2 new lines have been added.
                You can find the 2 new lines in the new English file starting at line 14.
                The section header `complexSymbols` is included where possible to help give context.

            ```diff
            --- b/source/locale/en/symbols.dic
            +++ a/source/locale/en/symbols.dic
            @@ -2 +2 @@
            -# Copyright (c) 2011-2023 NVDA Contributors
            +# Copyright (c) 2011-2024 NVDA Contributors
            @@ -13,0 +14,2 @@ complexSymbols:
            +# Series of dots used for visual presentation, e.g. in table of contents
            +multiple .     \.{4,}
            @@ -27,0 +30 @@ symbols:
            +multiple .     multiple dots   all     always
            ```

1. Find the relevant file to edit in the GitHub directory
    - Visit [source/locale](https://github.com/nvaccess/nvda/tree/beta/source/locale)
    - Open the directory with your language code
        - English example: <https://github.com/nvaccess/nvda/tree/beta/source/locale/en>
        - Format (replace `{lang}`): `https://github.com/nvaccess/nvda/tree/beta/source/locale/{lang}`
    - Find the relevant file:
        - `symbols.dic`, `characterDescriptions.dic` or `gestures.ini`
        - English example: <https://github.com/nvaccess/nvda/blob/beta/source/locale/en/symbols.dic>
        - Format (replace `{lang}` and `{fileName}`): `https://github.com/nvaccess/nvda/blob/beta/source/locale/{lang}/{fileName}`
1. If the relevant file doesn't exist yet, create a new one.
    - To create a new file use the "add file" button from your language's directory.
        - English example: <https://github.com/nvaccess/nvda/new/beta/source/locale/en>
        - Format (replace `{lang}`): `https://github.com/nvaccess/nvda/new/beta/source/locale/{lang}`
    - `characterDescriptions.dic`: Copy and paste desired contents from the [English example](https://raw.githubusercontent.com/nvaccess/nvda/refs/heads/beta/source/locale/en/characterDescriptions.dic).
    Note you should translate all the content you copy.
    - `symbols.dic`: Copy and paste desired contents from the [English example](https://raw.githubusercontent.com/nvaccess/nvda/refs/heads/beta/source/locale/en/symbols.dic).
    Note you should translate all the content you copy.
    - `gestures.ini`: This file doesn't require a base file, gestures can be added as needed.
1. Edit the relevant file
    - Tab to the "edit file" button to open the editor for the file.
    - English example: <https://github.com/nvaccess/nvda/edit/beta/source/locale/en/symbols.dic>
    - Format (replace `{lang}` and `{fileName}`): `https://github.com/nvaccess/nvda/edit/beta/source/locale/{lang}/{fileName}`
    - Refer to [background](#background) for more information on the format of the files
1. Submit your changes
    - Press `control+s` or the "commit changes" button to open a dialog to save and propose the changes.
    - Update the commit message to add your language to the end: "Update filename for language"
    - Press "Propose changes"
    - A new window should open proposing your changes
    - The proposal will contain a description with a large template.
    Feel free to ignore or delete it.
    - Press "Create pull request".
1. Await feedback from NV Access
    - NV Access will provide feedback if any further work is required.
    - You will receive a notification when your proposal is accepted - the request will be merged and closed.
    - After merging, the changes will become available in [beta builds](https://download.nvaccess.org/snapshots/beta/) for testing.
    The changes will also be made available in the next [beta release](https://download.nvaccess.org/releases/beta/).
