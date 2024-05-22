# Character Descriptions

Sometimes it can be very difficult or even impossible to distinguish
one character from another.  For example, two characters might be
pronounced the same way, even though they are actually different
characters.  To help users when this occurs, character descriptions
can be provided which describe the character in a unique way.

Character descriptions can be provided for a locale in a file named characterDescriptions.dic in the directory for the locale.
This is a UTF-8 encoded text file.
Blank lines and lines beginning with a "#" character are ignored.
All other lines should contain a character, followed by a tab, then one or more descriptions separated by tabs.

For example:

        # This is a comment.
        a	alpha
        b	bravo

For a full example, please look at the English character descriptions.dic.

note for Manual process: this is found in "source\locale\en\"
