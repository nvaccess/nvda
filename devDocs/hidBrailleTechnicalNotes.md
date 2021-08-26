HID Braille Developer Notes

## HID (Human Interface Device)
The HID specification standardizes the low-level communication with a USB or Bluetooth device, plus the types of input and output controls on the device.
Example devices being keyboards, mice, screens, and now Braille Displays.

### Definitions
In this document, device means a piece of hardware that connects to a computer via a connection such as USB or Bluetooth.
The device may contain one or more Controls for a human to physically communicate with the device, such as buttons or keys for input, or LEDs or cells of raised Braille pins for output.

There are also several terms in HID which may be confusing to those just beginning to familiarise themselves with this technology.
* Descriptors
* Usage pages
* Usages
* Reports
* Collections
* Caps (Capabilities)

These terms are described in the subsections below. 

#### HID descriptors
At connection time, a HID device must expose a block of data over the connection called a descriptor.
This is machine-readable data that describes all the input and output controls supported by the device, including their type and number of elements etc.
It also defines the size of data blocks (or reports) that can be written to and read from the device.
A descriptor can be read by a human (either as raw values or with some kind of decompiler) but from the point of view of Windows, the descriptor is opaque, and other more high-level Windows APIs should be used to communicate with the device, which will do all the type checking for you.

#### HID Usage Pages
The HID specification groups controls into categories which it refers to as pages.
Each page has its own unique number, and is referred to as a usage Page.
A Usage Page may represent a specific device type such as a keyboard, joystick or Braille display, or may be more general such as a generic Buttons page.

#### HID Usages
A Usage represents a type of control (key, button, braille cell, LED).
The Usage is assigned its own constant name, and a unique number relative to the particular Usage Page in the standard it is found on.
A Usage defines information about the control such as whether it is a boolean button, static or dynamic value, flag, or selector (1 of many).
For further information on what these types (sel, dv, nary etc) actually mean, refer to the first few pages of the HID Usage Tables 1.22 specification referenced at the bottom of this document.
The specification itself may or may not define other aspects of the data type such as its size or number of elements, though the HID descriptor the device makes available at runtime must contain all this information.
Usage IDs are also used to uniquely identify collections of controls or values.

#### HID reports
A report is a block of data that is read from or written to the HID device.
It has a size specified by the HID descriptor, and contains a report ID as the first byte.
On Windows, when fetching a new report with `ReadFile`, the report ID is automatically written into the data block by Windows, and most likely never needs to be known by the developer user as other high-level Windows APIs that can extract data from reports will use this report ID byte internally.
When writing reports with `WriteFile` however, the developer user must set the appropriate report ID byte in the report specific to the value/s the developer user includes in the report.
On Windows the report ID can be found in the `HIDP_VALUE_CAPS` (value capabilities) structure for that value, fetched from the HID descriptor with `HidP_GetValueCaps`.

#### HID collections
HID controls are grouped into collections.
Some examples might be all the keys on a keyboard, or all the cells in a line of Braille. 
Each defined collection has a Usage Page and a Usage ID so it can be uniquely identified.
All HID devices have a top-level collection, which is the main point of entry for gathering information about the device, including fetching other collections.
These other collections are known as Linked collections.

#### Caps
A shortening of the word Capabilities used by particular Windows APIs and structures for HID.
E.g. `HidP_GetCaps` gets the capabilities of the HID device.
These include things like the number of input buttons or output values on the device, the size of reports, and the Usage and Usage Page for the device.
Similarly `HidP_GetButtonCaps` gets the capabilities of all buttons on the device.
Capabilities of buttons and values include such things as their Usage and Usage Page, whether they represent a range of Usages, and whether they have a NULL state etc.
 
### General pattern for supporting HID on Windows
#### Enumerating HID devices
* Fetch the class guid for HID devices with `HidD_GetHidGuid`
* Fetch the device information set for the local machine with `SetupDiGetClassDevs`, specifying the HID class guid as the class guid.
 * Keep calling `SetupDiEnumDeviceInterfaces`, increasing memberIndex each time, to enumerate over all available devices fetching a `SP_DEVICE_INTERFACE_DATA` structure for each, until the function returns false, which means there are no more devices left to enumerate.
* For each data structure fetched, call `SetupDiGetDeviceInterfaceDetail` to get a `SP_DEVICE_INTERFACE_DETAIL_DATA` structure.
* The `SP_DEVICE_INTERFACE_DETAIL_DATA` structure's devicePath member  is the path that should be used to open the device for reading / writing later.
* Some other properties such as hardwareID may be required to further identify the device, these can be fetched with `SetupDiGetDeviceRegistryProperty`.
* For an implementation see `listHidDevices` in NVDA's source/hwPortUtils.py 

#### Opening a HID device
* Use `CreateFile` to open a HID device, giving it the DevicePath as the file path.
 Note overlapped IO is possible; See `CreateFile` documentation.
 * If this device may need to be opened by other processes at the same time, you will want to specify `FILE_SHARE_READ | FILE_SHARE_WRITE` as well.
* Once the open device handle is no longer needed, it can be closed with `CloseHandle`.
* For an implementation see the `Hid` class in NVDA's source/hwIo/base.py 

#### Fetching device attributes
* To fetch info such as vendorID, productID and versionNumber, call `HidD_GetAttributes` on the open device handle.
* To fetch the manufacturer string, use `HidD_GetManufacturerString` giving the open device handle.
* To fetch the product string, use `HidD_GetProductString` giving the open device handle.

#### Fetching the HID descriptor
Fetching device capabilities, getting data from reports and setting data in reports all requires the device's HID descriptor.
Windows represents the HID descriptor as an opaque value referred to as the preparsed data.
* Fetch the device's preparsed data with `HidD_GetPreparsedData`, giving it the open device handle.
Note this must be freed once it is no longer needed with `HidD_FreePreparsedData`.
 
#### Fetching device capabilities
* To find out a top-level collection's Usage Page, Usage, number of input and output values, and report sizes, fetch a `HIDP_CAPS` structure for the device with `HidP_GetCaps`, giving the open device handle and the preparsed data.

#### Fetching value / button capabilities
type information of input buttons and values and output values on a device (such as their Usage ID, size and number of items) can be found out through a `HIDP_VALUE_CAPS` structure for each.
An array of these structures can be fetched with `HidP_GetValueCaps` for input or output values, and `HidP_GetButtonCaps` for buttons.
Sometimes a `HIDP_VALUE_CAPS` structure can represent a range of buttons or values, where minimum and maximum Usage IDs and Data indices are exposed, rather than a specific value.
Examples of these might be the way that Braille dot input keys are exposed.
There is only one `HIDP_VALUE_CAPS` structure, covering values from dot1 to dot8.
 
#### Reading data from the device
* Use `ReadFile` to read the next available input report from the device.
The size of data to read in bytes must be equal to the `InputReportByteLength` member of the device's `HIDP_CAPS` structure.
 * Use functions such as `HidP_GetData` and `HidP_GetUsages` to extract the current value of buttons and other values set in the report.

#### Writing data to the device
To set the value of particular controls on the device:
* Create an output report by allocating a block of memory of size OutputReportByteLength from the device's HIDP_CAPS structure, using something like `malloc`.
* Set the report ID (the first byte) to the report ID found in the `HIDP_VALUE_CAPS` structure for the value/s you want to set.
This obviously means you can only set values who share the same report ID in a single report.
* Set the data for the values using functions such as `HidP_SetUsageValue` or `HidP_SetUsageValuesArray`.
* Send the report to the device using `WriteFile`.
The size in bytes sent must be equal to the `OutputReportByteLength` of the device's `HIDP_CAPS` structure.

## HID Braille specification
### Background
Braille Display devices allow being controlled by Screen Readers using a variety of connections such as Serial, USB and Bluetooth.
The protocols used over these channels have traditionally been Braille Display manufacturer specific.
This has meant that in order for a Screen Reader to support a particular Braille display, it must have specific logic in the Screen Reader that knows how to speak the required device-specific protocol.
Further to this, On Windows at least, an OS-level driver provided by the Braille Display manufacturer must also be installed by the user in order for the computer to detect and communicate with the device.
With the introduction of the HID (Human Interface Device) standard for USB (and later Bluetooth), it became possible to remove the need for the required OS-level device driver on Windows if the Braille Display manufacturer exposed the device as a custom HID device, however the Screen Reader still needed device-specific code, as being custom HID only simplified the low-level bytes communication, but did not standardise what those bytes actually meant.

In 2018, The HID specification was extended to define the concept of a Braille Display device, including setting of braille cells, and the standardizing of common buttons found on Braille displays such as routing keys, Braille dot input keys, braille space and panning keys.
A new Usage Page was added to the HID specification: HID_USAGE_PAGE_BRAILLE (0x41).
This page contains new Usage IDs such as:
* BRAILLE_DISPLAY (0x1): the usage ID for the HID device's top-level collection.
* Collections such as BRAILLE_ROW (for containing braille cells)
* 8_dot_BRAILLE_CELL (0x3) and 6_dot_braille_cell (0x4), which is an output value that represents a physical braille cell on a the device.
* BRAILLE_KEYBOARD_DOT_1 through BRAILLE_KEYBOARD_DOT_8: the Braille dot input buttons for typing braille characters.
* left, right and centre braille space keys (for typing a space).
* Joystick and dpad buttons
* Panning buttons for scrolling the braille display.
details for the number of collections, usages, and reports must be queried at run time and may vary between devices and even with device firmware updates.

### Pattern for talking with a HID braille device
#### Initialization
* Follow the general instructions for enumerating and opening a HID device,  plus fetching device and value capabilities as mentioned earlier in this document.
* Ensure the Hid device is truly a Braille display by checking that the `HIDP_CAPS.UsagePage` of the HID device's top-level collection is set to `HID_USAGE_PAGE_BRAILLE` (0x41).
 * Find the correct output `HIDP_VALUE_CAPS` structure which represents the array of braille cells.
I.e.
the Usage ID is either EIGHT_DOT_BRAILLE_CELL or six_dot_braille_cell.
The `ReportCount` member of this struct states the number of cells for the device.
This structure should also be saved off as it is later needed when writing braille to the display.
* Collect all the `HIDP_VALUE_CAPS` structures for input buttons / values and store them in a mapping keyed by their `DataIndex` member (or a calculated data index offset from the `DataIndexMin` member if the `HIDP_VALUE_CAPS` represents a range of values).
* It may also be useful to store an index of each `HIDP_VALUE_CAPS` structure relative to the first `HIDP_VALUE_CAPS` structure in the current collection (I.e.
when the `LinkCollection` member last differed from the previous structure).
In other words, the index within its collection.
this is needed in some implementations to work out which routing key a value represents, as the Usage ID for the value will be just ROUTING_KEY and the collection will be one of the ROUTER_SET_* collection Usage IDs.

#### Writing cells to the device
* Create a HID output report (block of memory), setting the report ID (first byte) to the value of the ReportID member of the Braille cell `HIDP_VALUE_CAPS` structure found at construction time. 
* Call `HidP_SetUsageValueArray` to place the data (braille cell dot patterns) into the report at the appropriate place, Using the Usage ID and collection number etc from the cell `HIDP_VALUE_CAPS` structure.
* Send the report to the Braille display using `WriteFile`.
The number of bytes written will be the value of `HIDP_CAPS.OutputReportByteLength`.

#### Receive input (key / button presses)
* Read an input report of size `InputReportByteLength` with `ReadFile` (or an overlapped IO callback)
 * `HidP_GetData` can be used to extract all `HIDP_DATA` structures from the report.
these represent the state of all input buttons and other controls.
* Using the `DataIndex` member of each retrieved data item, lookup the original `HIDP_VALUE_CAPS` structure for that data index to find out its Usage Page and Usage ID.
This will denote the actual button pressed or changed value.
If you only need to find out what buttons are pressed, but not any further data such as the actual set value or data index, you could call `HidP_GetButtons`.
But this would not be useful for buttons such as routing keys as you need to know specifically which routing key was pressed.

## References:
* USB HID article on wikipedia: https://en.wikipedia.org/wiki/USB_human_interface_device_class
* Introduction to Human Interface Devices (HID), Windows Driver docs: https://docs.microsoft.com/en-us/windows-hardware/drivers/hid/
* Interpreting HID Reports, Windows driver docs: https://docs.microsoft.com/en-us/windows-hardware/drivers/hid/interpreting-hid-reports
* HID Usages, Windows driver docs: https://docs.microsoft.com/en-us/windows-hardware/drivers/hid/hid-usages
* HID Usage Tables 1.22 (Contains HID Braille page): https://www.usb.org/document-library/hid-usage-tables-122
