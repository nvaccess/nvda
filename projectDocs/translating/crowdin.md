# Translating using Crowdin

Crowdin is used to translate the main NVDA interface and user documentation.
NVDA's Crowdin project: <https://crowdin.com/project/nvda>.

This document covers setting up a Crowdin account, connecting it with PoEdit, and translating the main interface and user documentation using Crowdin and PoEdit.

## Setup

### Create Crowdin account

1. Create a [Crowdin account](https://accounts.crowdin.com/register?continue=%2Fproject%2Fnvda).
1. Message the [translators mailing list](https://groups.io/g/nvda-translations) or <info@nvaccess.org> to request being added as a translator.
Please include your Crowdin username and the languages you wish to translate.

### Setup PoEdit

It is recommended that you use the latest version of PoEdit and NVDA for translating.
Alternatively, you can use the [Crowdin web interface](https://support.crowdin.com/online-editor/) directly.
As PoEdit only supports viewing approved strings, large translator teams need to co-ordinate submitting unapproved strings to prevent conflicts.
Using Crowdin's interface avoids this problem.

PoEdit's homepage is: <http://www.poedit.net/>

1. Download the latest Windows PoEdit version at <https://poedit.net/download>
1. Install it by following the on-screen instructions, the default options should be sufficient.

### Translation reviews
Due to accessibility issues, for now translation approvals have been disabled on Crowdin.
Any translation uploaded to Crowdin is automatically available in the project.
However, joining the project as a translator is by invitation only.

## Translation workflows

There are 2 common workflows for translating with Crowdin:

1. Translating strings directly via Crowdin's interface. Or
1. Downloading from Crowdin, translating with Poedit and uploading again.

## Translating using PoEdit

After opening a .po or .xliff file you will be placed on a list with all of the strings to translate.

You can read the status bar to see how many strings have already been translated, the number of untranslated messages, and how many are fuzzy.
A fuzzy string is a message which has been automatically translated, thus it may be wrong.
PoEdit will collect the new and fuzzy messages and presents them at the top of the already translated messages.

To insert or correct the translation for a string, first select it with the arrows, then tab to the blank edit field and type its translation.

NVDA will beep if you are on an untranslated or fuzzy message.
If you are using a braille display you'll see a star sign in-front of the messages you have to translate.

You may want to spell the original string to be aware of any punctuation mark, capital letters, etc.
PoEdit has a keystroke you may press while on an original string, `alt+c`, that copies the original string to the edit field when pressed.
You may then replace it with your translation as normal.

Press `control+s` at any moment to save your work.
Each time you press this key, PoEdit saves the po file, and if you check compile mo file checkbox in preferences, the .mo file will be re-generated.

NVDA provides additional shortcuts for PoEdit which are described in [the User Guide](https://download.nvaccess.org/documentation/userGuide.html#Poedit).

If you are unsure of the meaning of the original interface message, consult automatic comments (also called translator comments), by pressing `control+shift+a`.
Some comments provide an example output message to help you understand what NVDA will say when speaking or brailling such messages.

## Translating NVDA's interface

* Download the po file for your language from  Crowdin using NVA's l10nUtil.exe:
```
l10nUtil.exe downloadTranslationFile <language> <crowdinFilePath> [<localFilePath>]
```
E.g.
```
l10nUtil.exe downloadTranslationFile fr nvda.po
```
The first time you will be asked for an authorization token.
Please visit [your Crowdin settings API page](https://crowdin.com/settings#api-key) and create a Personal Access Token.
Ensure that it has at least the translations scope.
Then paste this into the user prompt.
This will be saved in ~/.nvda_crowdin for future use.
* Open the xliff file in Poedit, translate, and save the file.
* Upload the translated file using l10nUtil
```
l10nUtil.exe uploadTranslationFile <language> <crowdinFilePath> [<localFilePath>]
```
E.g.
```
l10nUtil.exe uploadTranslationFile fr nvda.po
```

Alternatively, you can use the [Crowdin interface directly](https://support.crowdin.com/online-editor/).

### Messages with formatting strings

You will come across several messages that have additional characters or punctuation as part of the message, this section will explain how they should be treated.

- `%d`, digits
- `%s`, string
- `%.2f`, a number to 2 digits after the comma, for example 5.25
- `{keyword}`, the text around the keyword should be translated, but the word should be left as is.

#### Examples

- `%d percent`: this means that `%d` will be replaced by a number when the program is running, and you only need to translate the word `percent`.
- `subject: %s`: here `%s` means that another string will be substituted.
- `{color} on {backgroundColor}`: In this case, the word `on` should be translated.
The rest should be left alone or rearranged in order to suit the language.
This will be presented as "black on white", "yellow on black", etc.

### Messages with ampersands - shortcut keys

Example: `&Rate`

The letter following the ampersand sign can be used as a shortcut key.
So when you translate, you can put the ampersand wherever in the translated message, and the letter that follows it will be used as the shortcut for your language.
When you have completed all other translation work, you may want to review the shortcut keys, since they provide many users a fast way of jumping to particular items in dialogs, such as specific checkboxes or combo-boxes.
It is best to try not to have duplicated keys.

### Plural forms

Languages can have any number of plural forms.
Strings can have multiple versions depending on the plural form of the subject.

Example:

- `with %s item`
- English plural form:
  - Multiple: `with %s items`
- Arabic plural forms:
  - Zero: `تتضمن %s من العناصر`
  - One: `تتضمّن %s من العناصر`
  - Two: `تتضمَّن عنصرين %s`
  - Few: `تتضمَّن %s عناصر`
  - Many: `تتضمَّن %s من العناصر`
  - Other: `تتضمَّن %s من العناصر`

In the [Crowdin web interface](https://support.crowdin.com/online-editor/), these can be set for each language using the "Form" section which replaces the standard translation edit box.

In PoEdit, the standard translation edit box has tabs for each plural form.
[Object navigation](https://download.nvaccess.org/documentation/userGuide.html#ObjectNavigation) is required to move focus to each tab button for the plural form.
You can do this by:

- By moving to the previous focus object from the edit box, you can cycle through each plural form tab button by continuing to more backward.
  - Desktop: `NVDA+numpad4`
  - Laptop: `NVDA+shift+leftArrow`
- Activate the current object once the desired tab button is reached.
  - Desktop: `NVDA+numpadEnter`
  - Laptop: `NVDA+enter`

If the number of plural forms for your language is incorrect please message the [translators mailing list](https://groups.io/g/nvda-translations) or <info@nvaccess.org>.

### String groupings

Translators may wish to provide two different translations for the same English string depending on the context.
Translation strings can be grouped by a tag to differentiate contexts.
Translator comments provide additional context information.

The string `none` is defined three times:
* without any context to report a lack of background pattern in Microsoft Excel
* with the context tag `symbolLevel`
* with the context tag `espeakVarient`

In PoEdit, these tags are at the start of each translation string list item.
In Crowdin, this information appears at the end of the context section.

### Testing the interface translation

1. To test the current interface messages, save the current nvda.po file in Poedit, and copy the nvda.mo file to the following location: `nvdadir/locale/langcode/LC_MESSAGES`
    - `nvdadir`: the directory where NVDA has been installed
    - `langcode`: the ISO 639-1 language code for your language (e.g. en for English, es for Spanish, etc.)
1. Restart NVDA, then go to the NVDA menu, go to Preferences and choose General Settings, or press `NVDA+control+g` to open General Settings.
1. From the language list, select your language (if it is listed), press `enter` and say yes when you're asked to restart NVDA.
1. The messages you have translated should now be heard or brailled in your native language provided that the synthesizer you are using supports your language or a braille code for your language exists.

Whenever you add or update your interface translations, repeat the steps above (copying the updated .mo file and restarting NVDA) to test your updated translation messages.

## Translating User Documentation

Documentation available for translation includes:

* The NVDA user guide (userGuide.xliff)
* The NVDA What's New document (changes.xliff)

To translate any of these files:

* Download the xliff file for your language from  Crowdin using NVA's l10nUtil.exe:
```
l10nUtil.exe downloadTranslationFile <language> <crowdinFilePath> [<localFilePath>]
```
E.g.
```
l10nUtil.exe downloadTranslationFile fr userGuide.xliff
```
The first time you will be asked for an authorization token.
Please visit [your Crowdin settings API page](https://crowdin.com/settings#api-key) and create a Personal Access Token.
Ensure that it has at least the translations scope.
Then paste this into the user prompt.
This will be saved in ~/.nvda_crowdin for future use.
* Make a copy of the downloaded file.
* Open the xliff file in Poedit, translate, and save the file.
* Upload the translated file using l10nUtil
```
l10nUtil.exe uploadTranslationFile <language> <crowdinFilePath> [<localFilePath>] [--old <oldLocalFilepath>]
```
E.g.
```
l10nUtil.exe uploadTranslationFile fr userGuide.xliff --old userGuide_backup.xliff
```
This will only upload added / changed translations since you downloaded the file.

Alternatively, you can use the [Crowdin interface directly](https://support.crowdin.com/online-editor/).

### Translating markdown

The English NVDA user documentation is written in markdown syntax.
The xliff file you are directly translating has been generated from that markdown file.
It contains the content of any line that requires translation, shown in the order it appears in the original markdown file.

Structural lines that do not contain any translatable content (such as blank lines, hidden table header rows, table header body separator lines etc) are not included here.

Structural syntax from the beginning and end of lines (such as heading prefix like `###`, heading anchors like `{#Introduction}`, and initial and final vertical bars on table rows) has been removed from the content to translate, but is available to view in the translator notes for that line.
Content may still however contain inline markdown syntax such as links, inline code fences (``` `` ```), and table column separators (`|`).
This syntax must be kept intact when translating.

All strings for translation contain translator notes which include:
* Line: the original line number in the markdown file.
* prefix: any structural markdown on the line before this content.
* Suffix: any structural markdown on the line after this content.

### Verifying your translation

When ever you have saved the xliff file with Poedit, you can use the NVDA l10nUtil program to generate the html version of the documentation file. E.g.
```
l10nUtil.exe xliff2html -t [userGuide|changes|keyCommands] <xliff file> <output html file>
```
