## Albatross

This module contains driver for Caiku Albatross 46 and 80 braille displays.

### General

Different to many other displays, Albatross models do not wait for the driver
to send a query of their presence to the device. Instead, the device continuously sends
initialization packets until driver requests to them quit, as the connection has been
established.

These displays also expect regular data packets, with frequency of at least one every
2 seconds. Otherwise they fall back to "wait for connection" state and
start sending the initialization packets until the driver sends a quit packet.

Similarly, if the user enters the device internal menu, after exiting, initialization packets
are continuously sent until driver sends quit packet.

Init packets are also sent when device is powered off and then on.

Display init packets consist of two bytes: the first one is \xff which tells
that this is an init packet. The second one is a settings byte which contains
display settings like length of display and number of status cells.
The most meaningful setting is the length of display. Other settings
contained by settings byte can be regarded as notes to screenreader, and it
is screenreader or driver job to use them when applicable. For example,
there are no separate status cells in the device but if screenreader
supports using status cells, it can be notified to use them by settings byte.

The settings byte can be anything between \x00 and \xff. Thus it could be the
same as init byte.

It is possible that settings byte may have same value with any display buttons.
Because init packets may be sent also during session (user exits display
internal menu for example), it is essential to know if byte is button press
or part of init packet.

When display is in "wait for connection" state, it sends init packets continuously.
As such, there may be hundreds of bytes to handle. There are several
rx buffers between device and driver which seems to cause situation that all
data cannot be read with one read operation. It cannot be known when all data
has been read. This is the case with init packets but also with key
combinations.

There are other devices with same PID&VID. When automatic braille display
detection is used, other displays with same PID&VID are tried before Albatross.
Those drivers try to send queries to the port to detect their own displays.
These queries may cause Albatross to send unexpected init packets which in
turn could disturb this driver - it could get inappropriate settings byte.
This is tried to prevent by resetting I/O buffers so that strange packets
would be discarded.

If however, there are still strange init packets, Albatross should be
manually selected from the display list.

To reduce complexity of data handling this driver accepts only settings bytes
<= \xfe. From user perspective this means that with 80 model user can ask
screenreader to use at most 14 status cells when without limitation user
could ask 15. Limitation is applied only if user has switched all other
settings to values that cause value of byte to be \xff. From settings byte
for status cells there are reserved the most right 4 bits. Limitation does
not affect on 46 cells model because the most left bit of byte defines the
length of display (0 for 46 and 1 for 80 cells model).

Note: This driver ignores status cells related settings because NVDA does not
use status cells at the moment.

### Driver requirements

- support for both 46 and 80 cells models
- support for both automatic and manual detection
- when connected allows device plugging out and in, and power switching off and
on so that display content is up-to-date and buttons work as expected after
these operations.

### Design

Driver has modular structure:

`constants.py` contains all the constant definitions, for example button
values and names.

`driver.py` is the main part of the code. It implements `BrailleDisplayDriver`
class which is in response of all read and write operations. It also takes care
to format data which is meant to be displayed on the braille line.

Important main functions of `BrailleDisplayDriver` are:

- `_readHandling`; performs connecting/reconnecting to the device, and all read
operations during connection
- `_somethingToWrite`; performs all write operations to the display
- `display`; prepares data to be displayed on the braille line

In `gestures.py` numeric values of pressed buttons are interpreted as gestures
so that they can be forwarded to NVDA input system.

`_threading.py` defines two threads. Thread called albatross_read calls
`BrailleDisplayDriver` `_readHandling` function when it gets signaled that port
has data to be read. Idea is somewhat similar to `hwIo` `onReceive` function.
For deeper read and write operations control own thread was implemented. In
addition, it calls `_readHandling` if it detects port problems so that
`_readHandling` can try to reconnect. Albatross_read thread sleeps most of the
time because user does not press buttons continuously, and connection problems
occur rarely.

The second thread is timer which checks periodically (after approximately 1.5
seconds) that some data has been sent to display so that it keeps connected.
`_SomethingToWrite` function updates time of last write operation. If there is
at least 1.5 seconds from last write operation, display is feeded data packet
containing `START_BYTE` and `END_BYTE` which enclose data which is sent to be
displayed on the braille line.
