# NVDA Translation and Localization

Thank you for considering to localize NVDA to your language, or improving an existing translation.
In order to support multiple languages/locales, NVDA must be translated and data specific to the locale must be provided.
There are several tasks to be done, and this document hopes to give you an overview and guide you through the process.

## Translation Mailing List
Translators should subscribe to the [NVDA translations mailing list](https://groups.io/g/nvda-translations) hosted at Groups.IO.

It is an English low traffic list devoted for the discussion of translation. 
Important messages that relate to translators will also be sent here, e.g. before official NVDA releases, to remind translators to make sure their localization is up to date.

## Important Dates

Translators should ensure their translation is up to date during the beta period before each new release, in order for it to be included in the upcoming final release.
A reminder will be posted on the translation mailing list giving two weeks notice of the translation string freeze.
Work submitted after the translation string freeze date will not be included in the upcoming release.
For further information please see the [Release Process page](https://github.com/nvaccess/nvda/blob/master/projectDocs/community/releaseProcess.md).

## Translation Status

You can view [Crowdin](https://crowdin.com/project/nvda) for an up to date report on the status of translating the NVDA interface.
If you would like to improve or would like to work on a new language, please write to the [NVDA translations mailing list](https://groups.io/g/nvda-translations).

The translation status of user documentation (User Guide and Changes) can only be checked by translators.

## New Localization
Start by subscribing to the translation list above, so that you can get help and advice.

The current process for translation is split between multiple processes:
- Crowdin for the NVDA interface
- The legacy SVN translation system for the User Guide and Changes files
- GitHub for Character Descriptions, Symbols and Gestures

Read [Files to be Localized](#files-to-be-localized) to learn the translation for process for these.

## Improving an Existing Localization
You should contact the existing maintainer of your language, and discuss your suggestions and changes.
Together you should be able to agree on the best translation and terms to be used, and the necessary changes can be made.

You can send an email to the translation mailing list to find out the correct person. 

If your language is no longer maintained, you can request to be the new maintainer for the language via the [NVDA translations mailing list](https://groups.io/g/nvda-translations).

## Files to be Localized
These files are listed in order of importance.
Note that linked guides may be out of date, as the translation system is undergoing the process of migration.

- nvda.po: NVDA's interface messages, see [Translating The Interface](https://github.com/nvaccess/nvda/wiki/TranslatingTheInterface) page for more info.
- characterDescriptions.dic: names of characters in your language, see [Translating Character Descriptions](https://github.com/nvaccess/nvda/wiki/TranslatingCharacterDescriptions) for more info.
- symbols.dic: names of symbols and punctuation in your language, see [Translating Symbols](https://github.com/nvaccess/nvda/wiki/TranslatingSymbols) for more information.
- gestures.ini: remapping of gestures for your language, see [Translating Gestures](https://github.com/nvaccess/nvda/wiki/TranslatingGestures) for more information.
- userGuide.md: the User Guide, see [Translating the User Guide](https://github.com/nvaccess/nvda/wiki/TranslatingUserGuide) for more information.
- changes.md (optional): a list of changes between releases, see [Translating Changes](https://github.com/nvaccess/nvda/wiki/TranslatingChanges) for more information.
- Add-ons (optional): a set of optional features that users can install, see [Translating Addons](https://github.com/nvaccess/nvda/wiki/TranslatingAddons) for more information.
