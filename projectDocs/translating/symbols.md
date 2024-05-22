# Symbol Pronunciation

It is often useful to hear punctuation and other symbols pronounced as words when reading text, particularly when moving by character.
Unfortunately, the pronunciation of symbols is inconsistent between speech synthesisers and many synthesisers do not speak many symbols and/or do not allow control over what symbols are spoken.
Therefore, NVDA allows information about symbol pronunciation to be provided.

This is done for a locale by providing a file named symbols.dic in the directory for the locale.
This is a UTF-8 encoded text file.
Blank lines and lines beginning with a "#" character are ignored.
All locales implicitly inherit the symbol information for English, though any of this information can be overridden.

The file contains two sections.

## Defining Complex Symbols
The first section is optional and defines regular expression patterns for complex symbols.
Complex symbols are symbols which aren't simply a character or sequence of characters, but instead require a more complicated match.
An example is the full stop (.) sentence ending in English.
The "." is used for multiple purposes, so a more complicated check is required to determine whether this refers to the end of a sentence.

The complex symbols section begins with the line:

        complexSymbols:

Subsequent lines contain a textual identifier used to identify the symbol, a tab and the regular expression pattern for that symbol.
For example:

        . sentence ending	(?<=[^\s.])\.(?=[\"')\s]|$)

Again, the English symbols are inherited by all other locales, so you need not include any complex symbols already defined for English.

## Defining Symbol Information
The second section provides information about when and how to pronounce all symbols.
It begins with the line:

        symbols:

Subsequent lines should contain several fields separated by tabs.
The only mandatory fields are the identifier and replacement.
The default will be used for omitted fields.
The fields are as follows:
- identifier: The identifier of the symbol.
 In most cases, this is just the character or characters of the symbol.
 However, it can also be the identifier of a complex symbol.
 Certain characters cannot be typed into the file, so the following special sequences can be used:
  - \0: null
  - \t: tab
  - \n: line feed
  - \r: carriage return
  - \f: form feed
  - \\#: # character (needed because # at the start of a line denotes a comment)
- replacement: The text which should be spoken for the symbol.
- level: The symbol level at which the symbol should be spoken.
 The symbol level is configured by the user and specifies the amount of symbols that should be spoken.
 This field should contain one of the levels "none", "some", "most", "all" or "char", or "-" to use the default.
 "char" means that the symbol should only be pronounced when moving by character.
 The default is to inherit the value or "all" if there is nothing to inherit.
- preserve: Whether the symbol itself should be preserved to facilitate correct pronunciation by the synthesiser.
 For example, symbols which cause pauses or inflection (such as the comma in English) should be preserved.
 This field should be one of the following:
 - never: Never preserve the symbol.
 - always: Always preserve the symbol.
 - norep: Only preserve the symbol if it is not being replaced; i.e. the user has set symbol level lower than the level of this symbol.
 - -: Use the default.
 The default is to inherit the value or "never" if there is nothing to inherit.
Finally, a display name for the symbol can be provided in a comment after a tab at the end of the line.
This will be shown to users when editing the symbol information and is especially useful for translators to define translated names for English complex symbols.

Here are some examples:

        (	left paren	most
This means that the "(" character should be spoken as "left paren" only when the symbol level is set to most or higher; i.e. most or all.

        ,	comma	all	always
This means that the "," character should be spoken as "comma" when the symbol level is set to all and that the character itself should always be preserved so that the synthesiser will pause appropriately.

        . sentence ending	point	# . fin de phrase
This line appears in the French symbols.dic file.
It means that the ". sentence ending" complex symbol should be spoken as "point".
Level and preserve are not specified, so they will be taken from English.
A display name is provided so that French users will know what the symbol represents.

## Notes

### Where to Find the English Symbols
For the manual process: Please see the file locale\en\symbols.dic for the English definitions which are inherited for all locales.

For the automatic process: a copy of the english symbols.dic is found in your working area.

### Thousands Separator
If your language uses a thousands separator such as a full stop (.) which is handled incorrectly due to other rules, you will need to define a complex symbol pattern for it. For example, if your language uses a comma (,) as its thousands separator, you would include the following in the complex symbols section:

        thousands separator	(?<=\d)\,(?=\d)
You would also include something like the following in the main symbols section:

        thousands separator	comma	all	norep
