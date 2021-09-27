# Display model

The display model (part of NVDA Helper), is a legacy mechanism for scraping
information during the rendering of GUI applications.

For information on working in this area see the `NVDAHelper/readme.md` file.

## Testing GDI applications
To test:
- Use `NVDA+numPad 7` to enter screen review mode.
- Use the number pad to read lines (7, 8, 9), read words, (4, 5, 6), or characters (1, 2, 3).

Additionally
- Use `NVDA+shift+f` to report formatting.

Note:
- For color reporting enable the option (via Document formatting panel) _"report color"_.
- To report transparencies in color enable the option (via advanced settings panel) _"Report transparent color values"_.

There are several simple test applications available:
https://github.com/nvaccess/testDisplayModel
