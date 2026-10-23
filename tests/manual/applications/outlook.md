# Classic Outlook recipient suggestions

Use a source build with add-ons disabled, Classic Outlook, and contacts matching a known prefix.
Record the NVDA branch and commit, Outlook version, Windows version and speech synthesizer.
Keep each candidate's complete logs in its own directory so log rotation preserves the previous run.
This procedure concerns Classic Outlook's recipient popup, not new Outlook.

## Restart and initial announcement

1. Start both NVDA and Classic Outlook fresh and open a new message.
1. In To, type `c`, pause, then type `h` (substitute a prefix matching local contacts if needed).
   * The first selected recipient must be spoken once as soon as it appears, without Backspace or arrow keys.
   * If refinement leaves the same recipient selected, it must remain quiet.
   * A changed recipient must be spoken once.
1. Clear the field and retry `c`; the first suggestion must be announced again.
1. Restart only NVDA, leaving Outlook open, and repeat.
1. Restart only Outlook, leaving NVDA running, and repeat.

## Selection and popup lifecycle

1. Test prefixes yielding one match, several matches, and no matches.
   * No results must produce no recipient announcement.
1. Refine and shorten the prefix with typing and Backspace.
   * A recipient that remains selected must not be repeatedly announced.
1. Navigate with Up and Down Arrow, including A to B to A.
   * Each changed selection must be spoken once, including the return to A.
1. Dismiss with Escape and reopen the same prefix.
   * The initial recipient must be announced again.
1. Accept with Enter, then repeat with Tab. Clear the accepted recipient and reopen the same prefix.
   * Each newly opened popup must announce its initial selection once.
1. Move between To, Cc and Bcc; repeat the core prefix and navigation checks in each field.
1. Move to another compose window and to another application while suggestions are open.
   * Old suggestions must not be announced over the new focus.
   * Returning and reopening suggestions must announce the initial selection again.

## Output and logging

1. Listen to speech and compare it with Speech Viewer or the speech entries in the complete log.
   * Check for missing announcements and duplicates after both restart variants.
1. Verify braille recipient messages and visual highlighting separately with suitable equipment/settings.
   Record unavailable checks as unverified.
1. Repeat the restart and initial-announcement checks with MSAA and UIA diagnostic logging disabled.
   * Announcement behaviour must be independent of these settings.
1. For a failure, record the exact action, expected recipient and audible result, and preserve both rotated logs.
   Classify it as event delivery, selection retrieval, duplicate suppression or lifecycle reset before changing the fix.

Where an older MSAA-based Outlook version is available, also verify its existing recipient announcement and navigation behaviour.
