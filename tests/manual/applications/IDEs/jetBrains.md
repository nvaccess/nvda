# JetBrains IDEs Smoke Testing Plan

## Objective

To ensure NVDA functions correctly with JetBrains IDEs (IntelliJ IDEA, Android Studio, PyCharm, WebStorm, etc.) across typical developer workflows.
This plan focuses on basic navigation, project operations, editor accessibility, and common IDE features.
JetBrains IDEs are based on the IntelliJ Platform, which is written in Java and smoke testing can reveal issues with the framework and Java applications more broadly.

## Areas Covered

* Application launch and window navigation
* Project operations
* Editor accessibility
* Search and navigation
* Debugging
* Version control
* Settings and plugins

## 1. Application Launch and Window Navigation

### Steps

1. Launch the JetBrains IDE
1. Verify NVDA announces the IDE window title
1. Use `alt+1` to focus the Project tool window
1. Use `alt+2` to focus the Favorites tool window
1. Use `alt+3` to focus the Find tool window
1. Use `alt+4` to focus the Run tool window
1. Use `alt+5` to focus the Debug tool window
1. Use `alt+6` to focus the TODO tool window
1. Use `alt+7` to focus the Structure tool window
1. Use `alt+8` to focus the Services tool window
1. Use `alt+9` to focus the Version Control tool window
1. Use `ctrl+tab` to switch between open files/tabs

### Expected Results

* NVDA announces window title and major UI regions
* Navigation between tool windows and tabs is clear and consistent

## 2. Project Operations

### Steps

1. Use `ctrl+shift+n` to create a new project
1. Use `ctrl+o` to open an existing project
1. Use `ctrl+shift+o` to open a project from version control
1. Use `ctrl+shift+s` to save all files
1. Use `ctrl+s` to save the current file
1. Use `ctrl+shift+a` to add a new file to the project
1. Use `delete` to remove a file from the project

### Expected Results

* NVDA announces project dialogs, project structure, and file actions
* Project operations are accessible and confirmed by speech

## 3. Editor Accessibility

### Steps

1. Type and navigate code in the editor using arrow keys
1. Use `ctrl+home` and `ctrl+end` to jump to start/end of file
1. Use `ctrl+f` to open the find dialog and search for text
1. Use `ctrl+r` to open the replace dialog
1. Use `ctrl+z` and `ctrl+y` to undo/redo
1. Use `ctrl+shift+space` for parameter info
1. Use `ctrl+space` for code completion
1. Use `ctrl+b` to go to declaration or usage
1. Use `ctrl+shift+b` to go to type declaration
1. Use `ctrl+u` to go to super method
1. Use `ctrl+alt+leftArrow` and `ctrl+alt+rightArrow` to navigate back and forward

### Expected Results

* NVDA announces line numbers, code, and search results
* Editing, navigation, and code assistance features are accessible

## 4. Search and Navigation

### Steps

1. Use `ctrl+f` to search within the current file
1. Use `ctrl+shift+f` to search across the project
1. Use `ctrl+shift+n` to find any file, class, or symbol
1. Use `ctrl+n` to find a class
1. Use `ctrl+shift+n` to find a file
1. Use `ctrl+shift+alt+n` to find a symbol
1. Use `ctrl+g` to go to a specific line
1. Use `ctrl+shift+a` to find an action

### Expected Results

* NVDA announces search dialogs, results, and navigation targets
* All search and navigation features are accessible

## 5. Debugging

### Steps

1. Use `f9` to toggle a breakpoint
1. Use `f8` to step over, `f7` to step into, `shift+f8` to step out
1. Use `f9` to resume program execution
1. Use `ctrl+f2` to stop debugging
1. Use `alt+5` to focus the Debug tool window
1. Use `alt+4` to focus the Run tool window
1. Use `ctrl+shift+f8` to view breakpoints

### Expected Results

* NVDA announces debugging state, breakpoints, and window focus
* Stepping, breakpoints, and variable inspection are accessible

## 6. Version Control

### Steps

1. Use `alt+9` to focus the Version Control tool window
1. Use `ctrl+k` to commit changes
1. Use `ctrl+t` to update project from version control
1. Use `ctrl+shift+k` to push changes
1. Use `ctrl+shift+a` to find version control actions

### Expected Results

* NVDA announces version control dialogs and actions
* All version control operations are accessible

## 7. Settings and Plugins

### Steps

1. Use `ctrl+alt+s` to open Settings/Preferences
1. Navigate through settings categories using arrow keys
1. Use `ctrl+alt+s` to open Plugins settings
1. Use arrow keys to browse available plugins
1. Use `enter` to install or enable a plugin

### Expected Results

* NVDA announces settings categories and plugin names
* Settings and plugin management are accessible
