# NVDA MS Office Smoke Testing Plan

## Objective

To ensure NVDA functions correctly with Microsoft Office applications (Outlook, Word, PowerPoint, Excel) across different UIA settings and typical user workflows.
This plan focuses on basic navigation, document interaction, and accessibility of key features.

## UIA Settings

For Word/Outlook, and Excel toggle the relevant UIA settings in Advanced Preferences.
Note: UIA support is evolving; NVDA should work optimally with the default UIA setting.

## Applications Covered

* Outlook
* Word
* PowerPoint
* Excel

---

## Outlook Smoke Tests

### 1. Launch and Basic Navigation

#### Steps

1. Launch Outlook
1. Verify NVDA announces the Outlook window title
1. Use `ctrl+1` to switch to Mail
1. Use `tab` and arrow keys to navigate the folder pane, message list, and reading pane

#### Expected Results

* NVDA announces window title and major panes
* Navigation between panes is clear and consistent

### 2. Reading and Managing Email

#### Steps

1. Use arrow keys to move through the message list
1. Use `enter` to open a message
1. Use `tab` to move through message headers and body
1. Use `ctrl+r` to reply, `ctrl+f` to forward, `delete` to delete
1. Use `ctrl+n` to create a new message
1. Compose a message, use `tab` to move between fields, and `ctrl+enter` to send

#### Expected Results

* NVDA announces message subjects, senders, and content
* All message actions are accessible and announced
* Composing and sending email is accessible

### 3. Calendar and Other Modules

#### Steps

1. Use `ctrl+2` to switch to Calendar
1. Use arrow keys to navigate the calendar
1. Use `tab` to move between calendar views and appointments
1. Use `ctrl+g` to go to a date
1. Use `ctrl+1` to return to Mail

#### Expected Results

* Calendar navigation is accessible
* Appointments and views are announced

---

## Word Smoke Tests

### 1. Launch and Document Navigation

#### Steps

1. Launch Word
1. Verify NVDA announces the Word window title
1. Use `ctrl+n` to create a new document
1. Use `tab` to move through the ribbon and document area
1. Use arrow keys to move through the document

#### Expected Results

* NVDA announces window title, ribbon, and document area
* Navigation is smooth and consistent

### 2. Basic Editing and Formatting

#### Steps

1. Type sample text
1. Use `ctrl+b` to bold, `ctrl+i` to italic, `ctrl+u` to underline
1. Use `ctrl+s` to save, `ctrl+o` to open a document
1. Use `ctrl+z` and `ctrl+y` to undo/redo
1. Use `alt+f4` to close

#### Expected Results

* NVDA announces formatting changes and file actions
* Editing and formatting are accessible

### 3. Reviewing and Navigation

#### Steps

1. Use `f7` for spell check
1. Use `ctrl+f` to open the navigation pane
1. Use `ctrl+g` to go to a page/section
1. Use `shift+f5` to return to last edit

#### Expected Results

* Spell check and navigation features are accessible
* NVDA announces review results and navigation targets

---

## PowerPoint Smoke Tests

### 1. Launch and Basic Navigation

#### Steps

1. Launch PowerPoint
1. Verify NVDA announces the PowerPoint window title
1. Use `ctrl+n` to create a new presentation
1. Use `tab` to move through the ribbon and slide area
1. Use arrow keys to move between slides and within slide content

#### Expected Results

* NVDA announces window title, ribbon, and slide area
* Navigation is smooth and consistent

### 2. Slide Editing and Presentation

#### Steps

1. Type sample text on a slide
1. Use `ctrl+m` to add a new slide
1. Use `ctrl+s` to save, `ctrl+o` to open a presentation
1. Use `f5` to start slideshow, `esc` to exit
1. Use arrow keys to move between slides during slideshow

#### Expected Results

* NVDA announces slide content and transitions
* Editing and presenting are accessible

---

## Excel Smoke Tests

### 1. Launch and Basic Navigation

#### Steps

1. Launch Excel
1. Verify NVDA announces the Excel window title
1. Use `ctrl+n` to create a new workbook
1. Use arrow keys to move between cells
1. Use `tab` to move across cells and ribbon

#### Expected Results

* NVDA announces window title, ribbon, and cell coordinates
* Navigation between cells is clear and consistent

### 2. Data Entry and Basic Operations

#### Steps

1. Enter data in cells
1. Use `ctrl+c` to copy, `ctrl+v` to paste, `ctrl+x` to cut
1. Use `ctrl+z` and `ctrl+y` to undo/redo
1. Use `ctrl+s` to save, `ctrl+o` to open a workbook
1. Use `alt+f4` to close

#### Expected Results

* NVDA announces data entry and clipboard actions
* File operations are accessible

### 3. Formulas and Navigation

#### Steps

1. Enter a formula (e.g., `=sum(a1:a5)`)
1. Use `f2` to edit a cell
1. Use `ctrl+arrowKey` to jump to the edge of data regions
1. Use `ctrl+space` to select a column, `shift+space` to select a row

#### Expected Results

* NVDA announces formula entry and cell editing
* Navigation shortcuts are accessible
