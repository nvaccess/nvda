# NVDA Translation and Localization

Thank you for considering to localize NVDA to your language, or improving an existing translation.
In order to support multiple languages/locales, NVDA must be translated and data specific to the locale must be provided.
There are several tasks to be done, and this document hopes to give you an overview and guide you through the process.


## Translation Mailing List
Translators should subscribe to the [NVDA translations mailing list](https://groups.io/g/nvda-translations)
hosted at Groups.IO.

It is an English low traffic list devoted for the discussion of translation. 
Important messages that relate to translators will also be sent here, i.e. before official NVDA releases, to remind translators to make sure their localization is up to date.

## Important Dates

Translators should ensure their translation is up to date during the beta period before each new release, in order for it to be included in the upcoming final release.  A reminder will be posted on the translation mailing list giving two weeks notice of the translation string freeze.  Work submitted after the translation string freeze date will not be included in the upcoming release.  For further information please see the [ReleaseProcess page](https://github.com/nvaccess/nvda/wiki/ReleaseProcess).

## Translation Status

Status for existing NVDA localizations are provided below. If you would like to improve or would like to work on a new language, please write to the [NVDA translations mailing list](https://groups.io/g/nvda-translations).
Information updated as of August 2021 (2021.1).
When 2021.1 is listed in the last updated column, it means that the localization is fully up to date and is ready for the current release. For the purposes of the information below, "up to date" refers to interface translation of at least 98%.

Note (2023): We are currently working on a more streamlined process to update this page.  In the meantime, if you would like information on a particular language, you can also contact [NV Access](mailto:info@nvaccess.org).  The process for contributing to language translations is unchanged.


| Language | Status | Last updated |
|------------|----------|----------------|
| af_ZA: Afrikaans | out of date, maintainer needed, barely translated. | Oct 2009 |
| am: Amharic | out of date, maintainer needed, barely translated. | Jul 2012 |
| an: Aragonese | up to date. | 2021.1 |
| ar: Arabic | Up to date. | 2021.1 |
| bg: Bulgarian | Up to date. | 2021.1 |
| CA: Catalan | Work in progress. | 2018.4 |
| CKB: Central Kurdish | Maintainer needed, hasn't begun. | n.a. |
| cs: Czech |  Up to date, Documentation incomplete (Sept 2017). | 2021.1 | 
| da: Danish | Up to date. | 2021.1 | 
| de: German | Up to date. | 2021.1 | 
| de_CH: Swiss German | work in progress. | 2018.3 | 
| el: Greek | Up to date, Documentation incomplete (Sep 2017). | 2021.1 |
| es: Spanish | Up to date. | 2021.1 | 
| es_CO: Spanish (Columbia) | translation Out of date, maintainer needed. | Jun 2020 |
| Et: Estonian | started translation of interface | Apr 2021 |
| fa: Farsi | Up to date | 2021.1 |
| fi: Finnish | Up to date. | 2021.1 | 
| fr: French | Up to date. | 2021.1 | 
| ga: Gaeilge (Ireland) | work in progress. | Jun 2021 |
| gl: Galician | Up to date. | 2021.1 | 
| he: Hebrew | Up to date. Documentation incomplete (Oct 2018). | 2021.1 |
| hi: Hindi | Work in progress, documentation missing. | Mar 2021 |
| hr: Croatian | Up to date. | 2021.1 |
| hu: Hungarian | Work in progress. | 2020.4 |
| is: Icelandic | out of date, maintainer needed. | Apr 2013 |
| it: Italian | Up to date. | 2021.1 | 
| ja: Japanese | Up to date. | 2021.1 | 
| ka: Georgian | out of date, maintainer needed. | May 2015 |
| kk: Kazakh | out of date, maintainer needed, barely translated. | n/a |
| kmr: Northern Kurdish | Out of date, maintainer needed. | Dec 2018 |
| kn: Kannada | Out of date, maintainer needed. | Sept 2015 |
| ko: Korean | Up to date, | 2021.1 |
| ky: Kyrgyz | Work in progress. | 2018.3 |
| lt: Lithuanian | Out of date, maintainer needed. | 2016 |
| lv: Latvian | Out of date, maintainer needed. | 2016 |
| mk: Macedonian | Interface: Up to date. Documentation: Work in progress.. | 2021.1 |
| mn: Mongolian | Work in progress. | Jul 2019 |
| my: Burmese | Work in Progress. | August 2018 |
| nb_NO: Norwegian | Out of date. | 2015 |
| ne: Nepali  | Out of date, maintainer needed. | 2016 |
| nl: Dutch | Up to date. | 2021.1 |
| Pa: Punjabi | Out of date, maintainer needed. | Nov 2014 |
| pl: Polish | Up to date. | 2021.1 |
| pt_BR: Portuguese (Brazil) | Up to date. | 2021.1 |
| pt_PT: Portuguese (Portugal) | Up to date. | 2021.1 |
| ro: Romanian | Up to date. | 2021.1 |
| ru: Russian | Up to date. | 2021.1 |
| sk: Slovak | Up to date. | 2021.1 |
| sl: Slovenian | Up to date. | 2021.1 |
| so: somali | Out of Date, maintainer needed. | Feb 2019 |
| sr: Serbian | Up to date. | 2021.1 |
| sv: Swedish | out of date, maintainer needed. | May 2015 |
| ta: Tamil | Up to date. | 2021.1 |
| th: Tai | Out of date, maintainer needed, barely translated. | Feb 2011 |
| tr: Turkish | Up to date. | 2021.1 |
| uk: Ukranian | Up to date. | 2021.1 |
| ur: Urdu | Out of date, maintainer needed, barely translated.| 2016 |
| vi: Vietnamese | Up to date. | 2021.1 |
| zh_CN: Simplified Chinese | Up to date. | 2021.1 |
| zh_HK: Traditional Chinese Hong Kong | Up to date, Documentation missing. | 2021.1 |
| zh_TW: Traditional Chinese Taiwan | Up to date. | 2021.1 |
| kh: Traditional Khmer Cambodia | Starting, no files submitted | 2020.1 |

## New Localization
Start by subscribing to the translation list above, so that you can get help and advice.

It is recommended that you use our new more automated workflow, which will allow you to focus only on translation. See [the automated workflow section](#advantages-of-the-automatic-workflow-process ) below.

If you still wish to go through the manual process, then follow the instructions on the [[TranslatingUsingManualProcess]] page after first reading [Files to be Localized](#files-to-be-localized) below.

## Improving an Existing Localization
You should contact the existing maintainer of your language, and discuss your suggestions and changes. Together you should be able to agree on the best translation and terms to be used, and the necessary changes can be made.

You can send an email to the translation mailing list to find out the correct person. 

If your language is no longer maintained, you can request to be the new maintainer for the language.

## Files to be Localized
These files are listed in order of importance.

- nvda.po: NVDA's interface messages, see [[TranslatingTheInterface]] page for more info.
- characterDescriptions.dic: names of characters in your language, see [[TranslatingCharacterDescriptions]] for more info.
- symbols.dic: names of symbols and punctuation in your language, see [[TranslatingSymbols]] for more information.
- gestures.ini: remapping of gestures for your language, see [[TranslatingGestures]] for more information.
- userGuide.t2t: the User Guide, see [[TranslatingUserGuide]] for more information.
- locale.t2tconf: the locale txt2tags configuration file, see [[Translating-the-locale-txt2tags-configuration-file-(locale.t2tconf)]] for more information; this file is needed when translating userGuide.t2t or changes.t2t.
- changes.t2t (optional): a list of changes between releases, see [[TranslatingChanges]] for more information.
- Add-ons (optional): a set of optional features that users can install, see [[TranslatingAddons]] for more information.

## Advantages of the Automatic Workflow Process
- No need of a full NVDA development environment.
- You will be sent an email or twitter message when your po file needs updating.
- You will be sent an email or twitter message when your userGuide or changes file needs to be updated.
- Automatic generation of html from t2t files, so that you can check the correctness of your t2t markup.
- Automatically generated difference and word difference between previous and new versions, to help you quickly find the changes.
- A higher quality User Guide since the difference files encourage you to keep the English and your localization closely updated.
- Translation becomes many small tasks instead a big rush near a deadline. Maybe 10 minutes per week on average.
- It is easier to contribute, since each work unit is self contained.
- Your translation is regularly and automatically included into NVDA snapshots.
- Instead of following nvda-dev mailing list emails, you can just subscribe to nvda translations and important messages related to translation will be sent there.
- Auto generated structure difference between the English and your localized user guide, to quickly spot missing paragraphs, tables and lists.
- Automatic checking of po files, making sure that there are no mistakes that could cause any runtime errors.

If you want to follow the automatic workflow process, visit the [[TranslatingUsingAutomaticProcess]] page.

## Missing information
Please feel free to update this or any subsequent page with any tips or hints that you feel may be of use to other translators.
