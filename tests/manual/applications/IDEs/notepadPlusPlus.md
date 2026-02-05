# Notepad++ Smoke Testing Plan

## Objective

To ensure NVDA functions correctly with Notepad++ across typical user workflows.
This plan focuses on basic navigation, file operations, editor accessibility, and common text editing tasks.
Notepad++ is based on Scintilla and smoke testing can reveal issues with the framework.

## Areas Covered

* Application launch and window navigation
* File operations (open, save, close)
* Editor accessibility
* Search and replace
* Multiple tabs and documents
* Plugins and settings

## 1. Application Launch and Window Navigation

### Steps

1. Launch Notepad++
1. Verify NVDA announces the Notepad++ window title
1. Use `ctrl+tab` to switch between open documents/tabs
1. Use `ctrl+shift+tab` to switch in reverse order
1. Use `ctrl+w` to close the current tab
1. Use `ctrl+n` to create a new document
1. Use `ctrl+o` to open an existing file

### Expected Results

* NVDA announces window title and major UI regions
* Navigation between tabs and documents is clear and consistent

## 2. File Operations

### Steps

1. Use `ctrl+n` to create a new file
1. Type sample text
1. Use `ctrl+s` to save, enter a filename, and confirm
1. Use `ctrl+o` to open an existing file
1. Use `ctrl+w` to close the current file
1. Use `ctrl+shift+s` to save as
1. Use `ctrl+shift+o` to open in another instance

### Expected Results

* NVDA announces file dialogs and file actions
* File operations are accessible and confirmed by speech

## 3. Editor Accessibility

### Steps

1. Type and navigate text in the editor using arrow keys
1. Use `ctrl+home` and `ctrl+end` to jump to start/end of file
1. Use `ctrl+upArrow` and `ctrl+downArrow` to scroll without moving cursor
1. Use `ctrl+leftArrow` and `ctrl+rightArrow` to move by word
1. Use `shift+arrowKeys` to select text
1. Use `ctrl+a` to select all text
1. Use `ctrl+z` and `ctrl+y` to undo/redo

### Expected Results

* NVDA announces line numbers, text, and cursor position
* Editing and navigation are accessible

## 4. Search and Replace

### Steps

1. Use `ctrl+f` to open the find dialog
1. Enter a search term and use `f3` to find next
1. Use `shift+f3` to find previous
1. Use `ctrl+h` to open the replace dialog
1. Enter search and replace terms
1. Use `alt+a` to replace all
1. Use `alt+r` to replace current
1. Use `ctrl+f3` to find in files

### Expected Results

* NVDA announces search dialogs, results, and replacements
* All search and replace features are accessible

## 5. Multiple Tabs and Documents

### Steps

1. Open multiple files to create tabs
1. Use `ctrl+tab` to switch between tabs
1. Use `ctrl+shift+tab` to switch in reverse order
1. Use `ctrl+w` to close individual tabs
1. Use `ctrl+shift+w` to close all tabs
1. Use `ctrl+shift+t` to reopen closed tab
1. Use `ctrl+shift+s` to save all files

### Expected Results

* NVDA announces tab names and switching between tabs
* Multiple document management is accessible

## 6. Plugins and Settings

### Steps

1. Use `alt+p` to open the Plugins menu
1. Navigate through available plugins
1. Use `f7` to access Settings
1. Navigate through settings categories
1. Change a simple setting and verify it takes effect

### Expected Results

* NVDA announces plugin names and settings options
* Plugin management and settings are accessible
