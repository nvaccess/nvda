# LibreOffice Smoke Testing Plan

## Objective

To ensure NVDA functions correctly with LibreOffice applications (Writer, Calc, Impress) across typical user workflows.
This plan focuses on basic navigation, document interaction, and accessibility of key features.

## Applications Covered

* Writer
* Calc
* Impress

---

## Writer Smoke Tests

### 1. Launch and Document Navigation

#### Steps

1. Launch Writer
1. Verify NVDA announces the Writer window title
1. Use `ctrl+n` to create a new document
1. Use `tab` to move through the toolbar and document area
1. Use arrow keys to move through the document

#### Expected Results

* NVDA announces window title, toolbar, and document area
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
1. Use `ctrl+f` to open the find bar
1. Use `ctrl+g` to go to a page/section
1. Use `shift+f5` to return to last edit

#### Expected Results

* Spell check and navigation features are accessible
* NVDA announces review results and navigation targets

---

## Calc Smoke Tests

### 1. Launch and Basic Navigation

#### Steps

1. Launch Calc
1. Verify NVDA announces the Calc window title
1. Use `ctrl+n` to create a new spreadsheet
1. Use arrow keys to move between cells
1. Use `tab` to move across cells and toolbar

#### Expected Results

* NVDA announces window title, toolbar, and cell coordinates
* Navigation between cells is clear and consistent

### 2. Data Entry and Basic Operations

#### Steps

1. Enter data in cells
1. Use `ctrl+c` to copy, `ctrl+v` to paste, `ctrl+x` to cut
1. Use `ctrl+z` and `ctrl+y` to undo/redo
1. Use `ctrl+s` to save, `ctrl+o` to open a spreadsheet
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

---

## Impress Smoke Tests

### 1. Launch and Basic Navigation

#### Steps

1. Launch Impress
1. Verify NVDA announces the Impress window title
1. Use `ctrl+n` to create a new presentation
1. Use `tab` to move through the toolbar and slide area
1. Use arrow keys to move between slides and within slide content

#### Expected Results

* NVDA announces window title, toolbar, and slide area
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
