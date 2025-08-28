# Translating with Crowdin

Crowdin is used to manage the translations of the main NVDA interface and user documentation.
NVDA's Crowdin project: <https://crowdin.com/project/nvda>.

This document covers setting up a Crowdin account, and translating the main interface and user documentation using either the Crowdin web interface or Poedit / nvdaL10nUtil.

## Creating a Crowdin account

1. Create a [Crowdin account](https://accounts.crowdin.com/register?continue=%2Fproject%2Fnvda).
1. Message the [translators mailing list](https://groups.io/g/nvda-translations) or <info@nvaccess.org> to request being added as a translator.
Please include your Crowdin username and the languages you wish to translate.

## Translation workflows

There are 2 common workflows for translating with Crowdin:

1. Translating strings directly via Crowdin's web interface. Or
1. Downloading a translation file from Crowdin, translating with Poedit, and uploading the file back to Crowdin.

### Translating via Crowdin's web interface

For instructions on how to translate strings using Crowdin's web interface, please read [Crowdin's documentation for translators](https://support.crowdin.com/for-translators/).

Note: If you are a screen reader user, you may find Crowdin's web interface inefficient or impossible to use.
Therefore you may choose to use the Poedit workflow instead.

#### Translation Reviews / Approvals

Due to accessibility issues and to be able to support the alternative workflow using Poedit, the translation approvals feature has been disabled in the NVDA project on Crowdin.
This means that all new strings are essentially auto approved.
However, to maintain quality control, only translators specifically added to the project can add or change strings.

### Translating with Poedit

Poedit is a desktop application which is commonly used to translate files.
It is fairly accessible and is used by many blind and vision impaired translators.

The workflow for translating with Poedit involves:

1. Downloading the translation file using NVDA's l10n utility
1. Opening the translation file in Poedit, translating one or more strings, and saving the file.
1. Uploading the translation file back to Crowdin.

Warning: Do not download / upload translation files via Crowdin's web interface, nor use Poedit's Crowdin cloud translation feature, as these methods have been found to corrupt xliff files.
Please instead use NvDA's l10n utility for download and upload.
NVDA's l10n utility will automatically use the appropriate Crowdin settings when downloading and uploading, and will detect and correct corruptions in xliff files.

#### Setting up PoEdit

It is recommended that you use the latest version of PoEdit and NVDA for translating.

PoEdit's homepage is: <http://www.poedit.net/>

1. Download the latest Windows PoEdit version at <https://poedit.net/download>
1. Install it by following the on-screen instructions, the default options should be sufficient.

#### Locating the NVDA l10n utility

The NVDA l10n utility is required for safely and efficiently downloading and uploading translation files from / to Crowdin when translating with Poedit.

This utility is included with all versions of NVDA from 2025.1beta1 onwards.

* For installed copies of NVDA, its path is: `c:\Program Files (x86)\nvda\l10nUtil.exe`
* For portable copies, it can be found as `l10nUtil.exe` in the root directory of the portable copy.

#### Downloading po / xliff files with NVDA's l10n utility

```sh
l10nUtil.exe downloadTranslationFile <language> <crowdinFilePath> [<localFilePath>]
```

E.g.

```sh
l10nUtil.exe downloadTranslationFile fr nvda.po
```

The first time you will be asked for an authorization token.
Please visit [your Crowdin settings API page](https://crowdin.com/settings#api-key) and create a Personal Access Token.
Ensure that it has at least the translations scope.
Then paste this into the user prompt.
This will be saved in ~/.nvda_crowdin for future use.

If your language team has more than one translator who may be downloading, translating and uploading at the same time, it is important that once you have downloaded the file, that you save a copy before you start translating with Poedit.
This then allows you to provide l10nUtil with this original file when uploading, so that it can just upload only what has changed, which will avoid accidentally overriding another translator's work.

#### Translating po / xliff files using Poedit

After opening a .po or .xliff file you have previously downloaded with NVDA's l10n utility, you will be placed on a list with all of the strings to translate.

You can read the status bar to see how many strings have already been translated, the number of untranslated messages, and how many are fuzzy.
A fuzzy string is a message which has been automatically translated, thus it may be wrong.
PoEdit will collect the new and fuzzy messages and presents them at the top of the already translated messages.

To insert or correct the translation for a string, first select it with the arrows, then tab to the blank edit field and type its translation.

NVDA will beep if you are on an untranslated or fuzzy message.
If you are using a braille display you'll see a star sign in-front of the messages you have to translate.

You may want to spell the original string to be aware of any punctuation mark, capital letters, etc.
To copy the original string into the "Translated text" control ready for further translation, you can press `control+b`.
You may then replace it with your translation as normal.

Press `control+s` at any moment to save your work.
Each time you press this key, PoEdit saves the po file, and if you check compile mo file checkbox in preferences, the .mo file will be re-generated.

NVDA provides additional shortcuts for PoEdit which are described in [the User Guide](https://download.nvaccess.org/documentation/userGuide.html#Poedit).

If you are unsure of the meaning of the original interface message, consult automatic comments (also called translator comments), by pressing `control+shift+a`.
Some comments provide an example output message to help you understand what NVDA will say when speaking or brailling such messages.

#### Uploading po / xliff files with NvDA's l10n utility

After translating the file with Poedit, upload the file back to Crowdin.

```
l10nUtil.exe uploadTranslationFile <language> <crowdinFilePath> [<localFilePath>]
```

E.g.

```
l10nUtil.exe uploadTranslationFile fr nvda.po
```

If you had previously saved a copy of the downloaded file before translation, then you will also want to include this in the command, so that l10nUtil only uploads the strings you have actually changed:
E.g.

```
l10nUtil.exe uploadTranslationFile fr nvda.po --old nvda_old.po
```

Where `nvda_old.po` was the saved copy.

## Translating NVDA's interface

* If translating via the Crowdin web interface, you can find these strings in the `NVDA interface messages` file.
* If translating via Poedit, you can download it as `nvda.po` using NVDA's l10n utility, e.g.

  ```sh
  l10nUtil.exe downloadTranslationFile fr nvda.po
  ```

### Messages with formatting strings

You will come across several messages that have additional characters or punctuation as part of the message, this section will explain how they should be treated.

* `%d`, digits
* `%s`, string
* `%.2f`, a number to 2 digits after the comma, for example 5.25
* `{keyword}`, the text around the keyword should be translated, but the word should be left as is.

#### Examples

* `%d percent`: this means that `%d` will be replaced by a number when the program is running, and you only need to translate the word `percent`.
* `subject: %s`: here `%s` means that another string will be substituted.
* `{color} on {backgroundColor}`: In this case, the word `on` should be translated.
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

* `with %s item`
* English plural form:
  * Multiple: `with %s items`
* Arabic plural forms:
  * Zero: `تتضمن %s من العناصر`
  * One: `تتضمّن %s من العناصر`
  * Two: `تتضمَّن عنصرين %s`
  * Few: `تتضمَّن %s عناصر`
  * Many: `تتضمَّن %s من العناصر`
  * Other: `تتضمَّن %s من العناصر`

In the [Crowdin web interface](https://support.crowdin.com/online-editor/), these can be set for each language using the "Form" section which replaces the standard translation edit box.

In PoEdit, the standard translation edit box has tabs for each plural form.
[Object navigation](https://download.nvaccess.org/documentation/userGuide.html#ObjectNavigation) is required to move focus to each tab button for the plural form.
You can do this by:

* By moving to the previous focus object from the edit box, you can cycle through each plural form tab button by continuing to more backward.
  * Desktop: `NVDA+numpad4`
  * Laptop: `NVDA+shift+leftArrow`
* Activate the current object once the desired tab button is reached.
  * Desktop: `NVDA+numpadEnter`
  * Laptop: `NVDA+enter`

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
    * `nvdadir`: the directory where NVDA has been installed
    * `langcode`: the ISO 639-1 language code for your language (e.g. en for English, es for Spanish, etc.)
1. Restart NVDA, then go to the NVDA menu, go to Preferences and choose General Settings, or press `NVDA+control+g` to open General Settings.
1. From the language list, select your language (if it is listed), press `enter` and say yes when you're asked to restart NVDA.
1. The messages you have translated should now be heard or brailled in your native language provided that the synthesizer you are using supports your language or a braille code for your language exists.

Whenever you add or update your interface translations, repeat the steps above (copying the updated .mo file and restarting NVDA) to test your updated translation messages.

## Translating User Documentation

Documentation available for translation includes:

* The NVDA user guide (userGuide.xliff)
* The NVDA What's New document (changes.xliff)

To translate any of these files either:

* locate the file in the Crowdin web interface and translate directly, or
* Download the file using NVDA's l10n utility, open the file in Poedit, translate and save, then upload the file with NVDA's l10n utility.

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
