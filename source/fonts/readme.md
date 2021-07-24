## Fonts

This folder contains fonts (and their projects files) used by NVDA.

### FreeMono-FixedBraille.ttf

This font is based on the `FreeMono.ttf` font in the `freefont-20100919-ttf` folder.
Its fontforge project is `freeMono-fixedBraille.sfd`

Many of the braille characters in `FreeMono.ttf` were offset (in different directions).
This meant that the characters appeared to jump around when they were updated, such as when displaying the caret
position.
This font, `FreeMono-FixedBraille.ttf`, adjusts all braille characters to a common position.
The dot positions are based on the final 8 dot braille character, ⣿ (all pins up) `U+28FF`.

### Editing

The free outline font editor, George Williams's FontForge
https://github.com/fontforge/fontforge/releases is used for editing the fonts via the `*.sfd` file.

