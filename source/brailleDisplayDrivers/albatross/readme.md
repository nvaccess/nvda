## Albatross

This module contains driver for Caiku Albatross 46 and 80 braille displays.

### Files

- `__init.py__`
- `constants.py`
- `threads.py`

`constants.py` contains various constants.

`threads.py` contains two classes for threads:

`ReadThread` detects when there is something to read (key presses or new connection init packets) and connection loss.

`RepeatedTimer` defines timer which is used to send data to display
periodically so that display does not fall back in "wait for connection" state.

`__init__.py` contains code to communicate with display, default key mapping, and stuff to interpret and forward its key presses.
