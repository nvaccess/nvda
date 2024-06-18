# Translating the interface nvda.po

It is recommended that you use PoEdit, since it will ensure that the file is saved correctly, and is correctly formatted.

## PoEdit

### Installing and running PoEdit

PoEdit's homepage is: http://www.poedit.net/

You can always download the latest Windows PoEdit version at: https://poedit.net/download

Install it by following the on-screen instructions, the default options should be sufficient.

When you run PoEdit for the first time, the first screen is where you choose the default PoEdit interface language, this is the language for the program menus, windows and options. It probably will default to your system language. In what follows, we will refer to PoEdit menus and options by their English names.

The next step is to enter your name and e-mail for PoEdit 
which will be included in the strings catalog file (nvda.po), to identify you as the last translator.
It is now ok to close the preferences window, the default values for the other options are fine.

### Translating using PoEdit

Assuming you went through the initial steps above, and you have now opened nvda.po using poedit, 
you will be placed on a list with all of NVDA's interface messages.

You can read the status bar to see how many strings have already been
translated, the number of untranslated messages, and how many are
fuzzy. A fuzzy string is a message which has been automatically
translated, thus it may be wrong. Poedit will collect the new and fuzzy messages and presents them at the top of the allready translated messages.

To insert or correct the translation
for a string, first select it with the arrows, then tab to the blank
edit field and type its translation.

NVDA will Beep if you are on a untranslated or fuzzy message. If you are using a Braille Display you'll see a star sign infront of the messages you have to translate.

You may want to spell the original string to be aware of any
punctuation mark, capital letters, etc. PoEdit has a keystroke you
may press while on an original string, alt+C, that copies the original
string to the edit field when pressed. You may then replace it with
your translation as normal.

Press control+s at any moment to save your work. Each time you press
this key, PoEdit saves NVDA.po and also re-compiles NVDA.mo (the .mo file will be generated if you check compile mo file checkbox in preferences).

NVDA provides two additional shortcut keys that will help you with translation.
- ctrl+shift+c, reads any comments that you or another translator have added as a note for this message.
- control+shift+a, reads automaticly extracted comments from code, that have been added by developers to help you in correctly translating this message.

If you are unsure of meaning of the original interface message, consult automatic comments (also called translator comments). Some comments provide an example output message to help you understand what NVDA will say when speaking or brailling such messages.

## Translating using a text editor

nvda.po is a plain utf8 without bom text file which contains all
of the specified strings to be translated.

Each line beginning with "msgid" contains an original English message
surrounded by quotes. Each line beginning with "msgstr" contains empty
quotes which should be filled in with the translation that corresponds
to the original English message at the above line or lines.  You
should also fill in the first lines of the file, which hold the
program's title, author, translator, language, etc.

In addition, don't forget to specify UTF-8 in the charset field and
8bit in the Content-Transfer-Encoding field.

The recommended editor is notepad++ because it can save directly into utf8 text.

## Messages with formatting strings

You will come across several messages that have additional characters
or punctuation as part of the message, this section will explain how
they should be treated.

- %d, digits
- %s, string
- %.2f, a number to 2 digits after the comma, for example 5.25
- {keyword}, the text around the keyword should be translated, but the word should be left as is.


### Examples
`%d percent`

this means that `%d` will be replaced by a number when the program
is running, and you only need to translate the word `percent`.

`subject: %s`
here `%s` means that another string will be substituted.

`on {backgroundColor`}

In this case, the word on should be translated, and the rest should be left alone.
This will be presented as "black on white", "yellow on black", etc.

## messages with ampersands

`&Rate`

The letter following the ampersand sign can be used as a mnemonic
(shortcut key).  So when you translate, you can put the ampersand
wherever in the translated message, and the letter that follows it
will be used as the shortcut for your language.  When you have
completed all other translation work, you may want to review the
mnemonics, since they provide many users a fast way of jumping to
particular items in dialogs, such as specific checkboxes or combo
boxes, and therefore it is best to try not to have duplicated keys.

## Testing the interface translation

To test the current interface messages, save the current nvda.po file, then copy the nvda.mo file (if one has been generated) to the following location:
nvdadir/locale/langcode/LC_MESSAGES
where nvdadir is the directory where NVDA has been installed and langcode is the ISO 639-1 language code for your language (e.g. en for English, es for Spanish, etc.). Restart NVDA, then go to NVDA menu, go to Preferences and choose General Settings; or press CTRL+NVDA+G to open General Settings. From the language list, select your language (if it is listed), press ENTER and say yes when you're asked to restart NVDA. The messages you have translated should now be heard or brailled in your native language provided that the synthesizer you are using supports your language or a braille code for your language exists.

Whenever you add or update your interface translations, repeat the steps above (copying the updated .mo file and restarting NVDA) to test your updated translation messages.

## Missing information

Please add any missing information on translating NVDA's interface.
