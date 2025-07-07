# NVDA Web Browser Smoke Testing Plan

## Objective

To ensure NVDA functions correctly with major web browsers across different architectures and versions.
This testing plan focuses on basic browse mode and focus mode functionality using W3C ARIA Authoring Practices samples as test content.

## Notes

* Test both browse mode (for reading content) and focus mode (for interactive elements).
* Use W3C ARIA Authoring Practices samples as standardized test content.
* Consider both 32-bit and 64-bit browser versions where applicable.

## Test Environment Requirements

### Browser Versions to Test

#### Google Chrome

Note: system tests already exist for 64bit Chrome.

* [Download Chrome (Official)](https://www.google.com/chrome/)
  * Chrome 64-bit (latest stable)
  * Chrome 32-bit (latest stable, if available)
  * Chrome Canary 64-bit (for early issue detection)

#### Microsoft Edge

* [Download Edge (Official)](https://www.microsoft.com/edge)
  * Edge 64-bit (latest stable)
  * Edge 32-bit (latest stable, if available)
  * Edge Canary 64-bit (for early issue detection)

#### Mozilla Firefox

* [Download Firefox (Official)](https://www.mozilla.org/firefox/)
  * Firefox 64-bit (latest stable)
  * Firefox 32-bit (latest stable, if available)
  * Firefox Nightly 64-bit (for early issue detection)

### UIA

For Chrome and Edge, toggle each option for use UIA in Chromium in Advanced Preferences.
Note: UIA support is experimental, NVDA should work optimally with the default UIA setting.

## W3C Test Samples

Use the following W3C ARIA Authoring Practices samples for testing:

### Basic Navigation and Structure

* [Landmarks](../../../include/w3c-aria-practices/content/patterns/landmarks/examples/):
  * [General principles](../../../include/w3c-aria-practices/content/patterns/landmarks/examples/general-principles.html)
  * [Navigation landmarks](../../../include/w3c-aria-practices/content/patterns/landmarks/examples/navigation.html)
  * [Main content landmarks](../../../include/w3c-aria-practices/content/patterns/landmarks/examples/main.html)
  * [Search landmarks](../../../include/w3c-aria-practices/content/patterns/landmarks/examples/search.html)

### Interactive Elements

* [Buttons](../../../include/w3c-aria-practices/content/patterns/button/examples/)
* [Links](../../../include/w3c-aria-practices/content/patterns/link/examples/)
* [Forms](../../../include/w3c-aria-practices/content/patterns/landmarks/examples/form.html)
* [Checkboxes](../../../include/w3c-aria-practices/content/patterns/checkbox/examples/)
* [Radio buttons](../../../include/w3c-aria-practices/content/patterns/radio/examples/)

### Complex Widgets

* [Combobox](../../../include/w3c-aria-practices/content/patterns/combobox/examples/)
* [Dialog](../../../include/w3c-aria-practices/content/patterns/dialog-modal/examples/)
* [Tabs](../../../include/w3c-aria-practices/content/patterns/tabs/examples/)
* [Accordion](../../../include/w3c-aria-practices/content/patterns/accordion/examples/)

## Test Cases

### 1. Browser Installation and Basic Launch

#### Steps

1. Launch the browser
1. Verify NVDA announces the browser window title correctly
1. Navigate to a simple HTML page (e.g., `about:blank`)

#### Expected Results

* NVDA announces browser window title and status
* Basic navigation works in browse mode

### 2. Browse Mode Testing

#### Steps

1. Load a W3C landmarks sample page
1. Use arrow keys to navigate through content
1. Use `h`, `shift+h` to navigate headings
1. Use `l`, `shift+l` to navigate links
1. Use `d`, `shift+d` to navigate landmarks
1. Use `f`, `shift+f` to navigate form fields
1. Use `t`, `shift+t` to navigate tables
1. Use `b`, `shift+b` to navigate buttons

#### Expected Results

* All navigation commands work correctly
* NVDA announces element types, names, and states appropriately
* Headings are announced with their level
* Links are announced with their destination (if available)
* Landmarks are announced with their role and name

### 3. Focus Mode Testing

#### Steps

1. Load a W3C form
1. Toggle to focus mode (`NVDA+space`)
1. Use `tab` to navigate between interactive elements
1. Use arrow keys to interact with form controls
1. Use `enter`/`space` to activate buttons and links
1. Test form field interaction (typing, selection)

#### Expected Results

* Focus mode toggle works correctly
* Tab navigation moves between interactive elements
* Form controls respond to keyboard input
* NVDA announces focus changes and element states
* Interactive elements are properly activated

### 4. Mixed Content Testing

#### Steps

1. Load a page with both static content and interactive elements
1. Navigate in browse mode through static content
1. Switch to focus mode when reaching interactive elements
1. Test seamless transition between modes
1. Verify proper announcement of mode changes

#### Expected Results

* Smooth transition between browse and focus modes
* Appropriate mode switching based on content type
* Clear indication of current mode

### 5. Slow pages / large pages

#### Steps

1. Test with slow-loading pages
1. Test with very large pages

#### Expected Results

* NVDA handles errors gracefully
* Performance remains acceptable

### 6. Dynamic Content Update Testing

#### Preconditions

* Browser is running with a W3C sample or custom page that demonstrates dynamic content updates (e.g., ARIA live regions, notifications, chat messages, updating counters, etc.)
* NVDA is running in browse mode and focus mode as appropriate

#### Steps

1. Load a page with ARIA live regions (e.g., [ARIA Live Region Example](https://www.w3.org/WAI/ARIA/apg/example-index/live_regions/polite.html))
1. Trigger a polite live region update (e.g., by clicking a button or waiting for an automatic update)
1. Trigger an assertive live region update
1. Load a page with dynamic notifications (e.g., ARIA alert role)
1. Trigger a notification (e.g., form validation error, chat message, etc.)
1. Load a page with dynamic content insertion/removal (e.g., adding/removing list items, updating counters)
1. Test dynamic updates in both browse mode and focus mode
1. Switch between tabs or windows and return to the page to check if updates are announced when focus returns

#### Expected Results

* NVDA announces polite and assertive live region updates according to ARIA specifications
* ARIA alerts and notifications are announced promptly and clearly
* Dynamic content changes (insertion, removal, updates) are announced as appropriate
* No duplicate or missing announcements
* Updates are announced in both browse and focus modes, as appropriate
* Returning focus to a page does not cause old updates to be re-announced, but new updates are still detected
* Performance remains acceptable during frequent updates

### 7. Browser UI Testing

#### Steps

1. Open the browser's main menu (e.g., `alt+f` for Chrome/Edge, `alt` for Firefox)
1. Navigate to the bookmarks or favorites menu
1. Create a new bookmark/favorite for the current page using keyboard shortcuts (e.g., `ctrl+d`)
1. Open the bookmarks/favorites manager and navigate through saved bookmarks
1. Delete or edit a bookmark/favorite
1. Open the browser's settings/preferences (e.g., `alt+f`, then `s` for Chrome/Edge; `alt+t`, then `o` for Firefox)
1. Navigate through the settings using keyboard navigation (`tab`, arrow keys)
1. Change a simple setting (e.g., homepage, privacy option) and confirm the change
1. Search within the settings/preferences page
1. Return to the main browser window and verify focus is restored

#### Expected Results

* All browser menus and dialogs are accessible with NVDA
* NVDA announces menu items, dialog titles, and options as they are navigated
* Creating, editing, and deleting bookmarks/favorites is possible using the keyboard and NVDA announces actions
* Browser settings/preferences are fully navigable and all options are announced
* Search within settings is accessible and results are announced
* Focus is restored to the main browser window after closing dialogs/menus
* No unexpected loss of speech or focus during these operations
