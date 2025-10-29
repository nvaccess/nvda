# VSCodium Smoke Testing Plan

## Objective

To ensure NVDA functions correctly with VS Code or other VSCodium derivatives across typical user workflows.
This plan focuses on basic navigation, file operations, editor accessibility, and common development tasks.
VSCodium is based on Electron and as such smoke testing can reveal issues with the framework.

## Areas Covered

* Application launch and window navigation
* File operations (open, save, close)
* Editor accessibility
* Command palette and search
* Extensions
* Terminal

## 1. Application Launch and Window Navigation

### Steps

1. Launch VSCodium
1. Verify NVDA announces the VSCodium window title
1. Use `ctrl+shift+p` to open the command palette
1. Use `ctrl+tab` to switch between open files/tabs
1. Use `ctrl+b` to toggle the sidebar
1. Use `f1` to open the command palette (alternative)
1. Use `ctrl+shift+e` to focus the Explorer
1. Use `ctrl+shift+f` to focus the Search panel

### Expected Results

* NVDA announces window title and major UI regions
* Navigation between panels and tabs is clear and consistent

## 2. File Operations

### Steps

1. Use `ctrl+n` to create a new file
1. Type sample text
1. Use `ctrl+s` to save, enter a filename, and confirm
1. Use `ctrl+o` to open an existing file
1. Use `ctrl+w` to close the current file
1. Use `ctrl+shift+t` to reopen a closed file

### Expected Results

* NVDA announces file dialogs and file actions
* File operations are accessible and confirmed by speech

## 3. Editor Accessibility

### Steps

1. Type and navigate text in the editor using arrow keys
1. Use `ctrl+home` and `ctrl+end` to jump to start/end of file
1. Use `ctrl+f` to open the find bar and search for text
1. Use `ctrl+h` to open the replace bar
1. Use `ctrl+z` and `ctrl+y` to undo/redo
1. Use `ctrl+shift+\` to jump to matching bracket
1. Use `alt+upArrow` and `alt+downArrow` to move lines up/down

### Expected Results

* NVDA announces line numbers, text, and search results
* Editing and navigation are accessible

## 4. Command Palette and Search

### Steps

1. Use `ctrl+shift+p` or `f1` to open the command palette
1. Type to search for commands (e.g., "toggle word wrap")
1. Use arrow keys to navigate results
1. Press `enter` to execute a command
1. Use `ctrl+shift+f` to open the search panel
1. Enter a search term and review results

### Expected Results

* NVDA announces command palette, search results, and command execution
* All command palette and search features are accessible

## 5. Extensions

### Steps

1. Use `ctrl+shift+x` to open the Extensions panel
1. Use arrow keys to navigate available extensions
1. Use `tab` to move between extension details and actions
1. Use `enter` to install or enable an extension

### Expected Results

* NVDA announces extension names, details, and actions
* Installing and managing extensions is accessible

## 6. Terminal

### Steps

1. Use ``ctrl+` `` to open the integrated terminal
1. Type commands and review output
1. Use `ctrl+shift+\` to create a new terminal
1. Use `ctrl+tab` to switch between terminal and editor

### Expected Results

* NVDA announces terminal focus and output
* Terminal operations are accessible
