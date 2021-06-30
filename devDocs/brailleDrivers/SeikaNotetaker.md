Note: This is a transcribed and reformatted copy of SeikaNotetaker.pdf. This PDF was taken from [this comment on GitHub](https://github.com/nvaccess/nvda/pull/12581#issuecomment-867517014) ([archive](https://archive.is/NBKRC)).


# Seika Notetaker Protocol V6.2.0
Acronyms:

- (SR) Screen Reader, eg NVDA
- (SBD) Seika Notetaker Braille Display

NOTE: When the routing key or/and button is pressed, there is no information send
from SBD to SR. When all routing key or/and button is released, then the information
will be send from SBD to SR

## 1. Handshake of SR and SBD

SR->SBD: `0xff 0xff 0xa1`

If SBD is prepare OK, then SBD will answer the SR handshake request:

SBD->SR: `0xff 0xff 0xa2 N B E R S1 S2…S(N-3)`

N means the number of the following bytes

B means the number of the buttons in the SBD

E means the number of cells in the SBD

R means the number of the routing switches in the SBD
S1…S(N-3) means the SBD description，each byte in the S1…S(N-3) is corresponding to
the ASCII character.

For example:

1. Seika Notetaker 16cell: `0xff 0xff 0xa2 0x11 0x16 0x10 0x10 S1 S2 … S14`
2. Seika Notetaker 40cell: `0xff 0xff 0xa2 0x11 0x16 0x28 0x28 S’1 S’2 … S’14`

## 2. SR will send SSD the braille message:
SR->SBD: `0xff 0xff 0xa3 E C1 C2…CE`

E means the number of the following bytes,

C1… CE means the braille message which will be displayed on the Seika.

The byte C1 will be display in the leftmost of SBD, and the byte CE will be display in
the rightmost of BD.

For example::
1. Seika Notetaker 16cell: `0xff 0xff 0xa3 0x10 C1……C16`
2. Seika Notetaker 40cell: `0xff 0xff 0xa3 0x28 C1……C40`

The bits in the symbol byte correspond to the dot values of the Braille character to
be displayed.

The braille dots in a cell are numbered as follows:


| | |
--|--
1 | 4
2 | 5
3 | 6
7 | 8

Braille dot 1 corresponds to bit 0, braille dot 2 corresponds to bit 1, and so on.…

For
example, the character "a" is represented by braille dot 1.
Therefore, bit 0 in the symbol byte must be set on and all other bits set off.…

The
binary value for "a" is 00000001, or hexadecimal 01.…

For the character "d",
represented by braille dots 1,4,5, the binary value is 00011001, or hexadecimal 0x19.

It is recommended that a table look-up system be used to perform this translation.

## 3. Routing button
SBD->SR `0xff 0xff 0xa4 G HZ1 HZ2 … HZG` ,

G means the smallest integral value that is not less than R/8. R means the number of
the routing switches in the SBD.

If a button of cursor routing keys board is released, the below packet of data
will be send from SBD to SR, which bit =1 means the key is pressed and
released, bit=0 means the key is not pressed:

HZ1-HZG hold data for the horizontal cursor routing keys on a SBD
	
Ex.:
1. routing key 1 is in bit 0 of HZ1.
2. routing key 8 is in bit 7 of HZ1.
3. routing key 9 is in bit 0 of HZ2.
4. routing key 40 is in bit 7 of HZ5.

If the cell number is not the 8 times G, then the high bit will be Zero. For
example, the 20 routing key, then 0xff 0xff 0xa4 0x03 HZ1 HZ2 HZ3, and the HZ3=
0000 xxxx, the 17th routing key is HZ3 bit0, the 20th routing key is HZ3 bit3.

For example:
1. Seika Notetaker 16cell: 0xff 0xff 0xa4 0x02 HZ1 HZ2
2. Seika Notetaker 40cell: 0xff 0xff 0xa4 0x05 HZ1 HZ2 HZ3 HZ4 HZ5

## 4. Button
SBD->SR, `0xff 0xff 0xa6 M P1 P2 ... PM`,

M means the smallest integral value that is not less than B/8. B means the
number of the buttons in the SBD.

If a button is released, the below packet of data will be send from SBD to SR,
which bit =1 means the key is pressed and released, bit=0 means the key is not
pressed, if there are more than one key is pressed, then there will be more than
one bit =1:

 P1 P2 P3 hold data for the buttons on a SBD
3

Ex.:
1. k1 is in bit 0 of P1.
2. K8 is in bit 7 of P1.
3. K22 is in bit 5 of P3.

### Seika Notetaker key map (transcribed diagram):

At the top of the device, a row of 8 buttons (braille keyboard): K7 K3 K2 K1 K4 K5 K6 K8

In the middle of the device, a panel with:
* Routing keys 1-16 or 1-40, across the top of the panel
* Cells 1-16 or 1-40, below the routing keys
* K11 on the left of the panel (Left Button)
* K12 on the right of the panel (Right Button)

Below the panel, at the bottom of the device, from left to right:
* Left Joystick (LJ)
  - K13 (Center)
  - K14 (Left)
  - K15 (Right)
  - K16 (Up)
  - K17 (Down)
* K9 (Backspace)
* K10 (Space)
* Right Joystick (RJ)
  - K18 (Center)
  - K19 (Left)
  - K20 (Right)
  - K21 (Up)
  - K22 (Down)

# 5. Button and routing key combined
SSD->SR `0xff 0xff 0xa8 (M+G) P1 P2 … PM HZ1 HZ2 … HZG`

P1 P2 P3 and HZ1…HZG are defined as the above section3 and section4

ex:
1. Seika Notetaker 16cell SSD->SR `0xff 0xff 0xa8 0x05 0x00 0x90 0x00 0x00 0x40` means that: 13th button, 16th button, and 15th routing key are pressed and
released.
2. Seika Notetaker 40cell SSD->SR `0xff 0xff 0xa8 0x08 0x01 0x20 0x00 0x00 0x00 0x02 0x00 0x00` means that: 14th button, 17th button and 18
th routing key
are pressed and released.
