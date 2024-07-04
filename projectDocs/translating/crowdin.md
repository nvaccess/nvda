# Translating using Crowdin

Crowdin is used to translate the main NVDA interface.
NVDA's Crowdin project: <https://crowdin.com/project/nvda>.

This document covers setting up a Crowdin account, connecting it with PoEdit, and translating the main interface using Crowdin and PoEdit.

## Setup

### Create Crowdin account

1. Create a [Crowdin account](https://accounts.crowdin.com/register?continue=%2Fproject%2Fnvda).
1. Message the [translators mailing list](https://groups.io/g/nvda-translations) or <info@nvaccess.org> to request being added as a translator.
Please include your Crowdin username and the languages you wish to translate.

### Setup PoEdit

It is recommended that you use the latest version of PoEdit and NVDA for translating.
Alternatively, you can use the [Crowdin web interface](https://support.crowdin.com/online-editor/) directly.
As PoEdit only supports viewing approved strings, large translators team need to co-ordinate submitting unapproved strings to prevent conflicts.
Using Crowdin's interface avoids this problem.

PoEdit supports connecting with Crowdin directly.
PoEdit's homepage is: <http://www.poedit.net/>

1. Download the latest Windows PoEdit version at <https://poedit.net/download>
1. Install it by following the on-screen instructions, the default options should be sufficient.
1. When launching PoEdit:
    1. Choose "Translate cloud project"
    1. Connect your Crowdin account
    1. Select NVDA and the language you wish to translate

### Translation reviews

Translated strings will need to be reviewed and approved by a proofreader before being included in NVDA.
A proofreader is required for each language.
Proofreader status is granted on a case-by-case basis by messaging the [translators mailing list](https://groups.io/g/nvda-translations) or <info@nvaccess.org>

Proofreaders approve strings using the [Crowdin web interface](https://support.crowdin.com/online-editor/).
PoEdit does not support viewing unapproved strings from other translators.
When manually uploading to Crowdin from PoEdit, proofreaders are able to auto-approve all submitted strings.

## Translation workflows

There are 3 common workflows for translating with Crowdin:

1. Only on Crowdin's web interface, either with:
    - only one proofreader approving their own translations,
    - or with many translators making suggestions and a proofreader approving them.
1. Multiple translators translating on PoEdit.
    - Using Crowdin cloud synchronization.
    - Proofreaders approve the translations on Crowdin's web interface.
1. Translating on PoEdit without cloud synchronization and performing manual uploads to Crowdin.
    - Translators with proofreader status can upload strings manually with automatic approval.
    As such, this may be a preference for single or small-team translators using PoEdit.
    - Manual uploads without cloud synchronization means conflicts can occur, translator teams must be co-ordinated if following this approach.

## Translating using PoEdit

After opening a .po file you will be placed on a list with all of the strings to translate.

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

NVDA provides additional shortcuts for PoEdit which are described in [the User Guide](https://www.nvaccess.org/files/nvda/documentation/userGuide.html#Poedit).

If you are unsure of meaning of the original interface message, consult automatic comments (also called translator comments), by pressing `control+shift+a`.
Some comments provide an example output message to help you understand what NVDA will say when speaking or brailling such messages.

## Translating the interface

Open "nvda.po" for the language you want to translate in PoEdit.
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
[Object navigation](https://www.nvaccess.org/files/nvda/documentation/userGuide.html#ObjectNavigation) is required to move focus to each tab button for the plural form.
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

1. To test the current interface messages, save the current nvda.po file, and copy the nvda.mo file to the following location: `nvdadir/locale/langcode/LC_MESSAGES`
    - `nvdadir`: the directory where NVDA has been installed
    - `langcode`: the ISO 639-1 language code for your language (e.g. en for English, es for Spanish, etc.)
1. Restart NVDA, then go to the NVDA menu, go to Preferences and choose General Settings, or press `NVDA+control+g` to open General Settings.
1. From the language list, select your language (if it is listed), press `enter` and say yes when you're asked to restart NVDA.
1. The messages you have translated should now be heard or brailled in your native language provided that the synthesizer you are using supports your language or a braille code for your language exists.

Whenever you add or update your interface translations, repeat the steps above (copying the updated .mo file and restarting NVDA) to test your updated translation messages.
