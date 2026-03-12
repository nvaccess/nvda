# Visual Studio Smoke Testing Plan

## Objective

To ensure NVDA functions correctly with Microsoft Visual Studio (not VS Code) across typical developer workflows.
This plan focuses on basic navigation, solution/project/file operations, code editor accessibility, debugging, and common development tasks.
Visual Studio is based on WinForms and as such smoke testing can reveal issues with the framework.

## Areas Covered

* Application launch and window navigation
* Solution, project, and file operations
* Code editor accessibility
* Debugging
* Search and navigation
* Extensions

## 1. Application Launch and Window Navigation

### Steps

1. Launch Visual Studio
1. Verify NVDA announces the Visual Studio window title
1. Use `alt` to access the menu bar
1. Use `ctrl+tab` to switch between open documents and tool windows
1. Use `ctrl+alt+l` to focus the Solution Explorer
1. Use `ctrl+alt+x` to open the Toolbox
1. Use `ctrl+q` to access Quick Launch

### Expected Results

* NVDA announces window title and major UI regions
* Navigation between panels and tool windows is clear and consistent

## 2. Solution, Project, and File Operations

### Steps

1. Use `ctrl+shift+n` to create a new project
1. Use `ctrl+shift+o` to open an existing project or solution
1. Use `ctrl+shift+s` to save all files
1. Use `ctrl+s` to save the current file
1. Use `ctrl+f4` to close the current document
1. Use `ctrl+shift+a` to add a new item to the project
1. Use `delete` to remove a file from the project

### Expected Results

* NVDA announces file dialogs, project structure, and file actions
* Solution and project operations are accessible and confirmed by speech

## 3. Code Editor Accessibility

### Steps

1. Type and navigate code in the editor using arrow keys
1. Use `ctrl+home` and `ctrl+end` to jump to start/end of file
1. Use `ctrl+f` to open the find dialog and search for text
1. Use `ctrl+h` to open the replace dialog
1. Use `ctrl+z` and `ctrl+y` to undo/redo
1. Use `ctrl+shift+space` for parameter info
1. Use `ctrl+space` for code completion
1. Use `f12` to go to definition
1. Use `shift+f12` to find all references

### Expected Results

* NVDA announces line numbers, code, and search results
* Editing, navigation, and code assistance features are accessible

## 4. Debugging

### Steps

1. Use `f5` to start debugging
1. Use `shift+f5` to stop debugging
1. Use `f9` to toggle a breakpoint
1. Use `f10` to step over, `f11` to step into, `shift+f11` to step out
1. Use `ctrl+alt+w,1` to open the Watch window
1. Use `ctrl+alt+q` to open the QuickWatch dialog
1. Use `ctrl+alt+c` to open the Call Stack window

### Expected Results

* NVDA announces debugging state, breakpoints, and window focus
* Stepping, breakpoints, and variable inspection are accessible

## 5. Search and Navigation

### Steps

1. Use `ctrl+f` to search within the current file
1. Use `ctrl+shift+f` to search across the solution
1. Use `ctrl+comma` to go to any file, symbol, or line
1. Use `ctrl+minus` and `ctrl+shift+minus` to navigate back and forward
1. Use `ctrl+g` to go to a specific line

### Expected Results

* NVDA announces search dialogs, results, and navigation targets
* All search and navigation features are accessible

## 6. Extensions

### Steps

1. Use `ctrl+q` to open Quick Launch, type "extensions"
1. Use arrow keys to navigate to Extensions and Updates
1. Use `tab` and arrow keys to browse available extensions
1. Use `enter` to install or enable an extension

### Expected Results

* NVDA announces extension names, details, and actions
* Installing and managing extensions is accessible
