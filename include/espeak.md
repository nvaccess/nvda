# eSpeak-ng submodule

The submodule contained in the `espeak` directory is a cross platform open source speech synthesizer.

## Building

NVDA has a custom build of eSpeak because not all components are required.

### Background

The main authority on build requirements is the upstream eSpeak CMake configuration, especially [`include/espeak/cmake/config.cmake`](./espeak/cmake/config.cmake) and [`include/espeak/src/libespeak-ng/config.h.in`](./espeak/src/libespeak-ng/config.h.in).
The legacy `*.vcxproj` files in [`include/espeak/src/windows/`](./espeak/src/windows/) are only a secondary reference and are not always kept up to date.

We do not use the upstream Visual Studio build directly; instead, NVDA maintains its own custom Windows build in [`nvdaHelper/espeak/sconscript`](../nvdaHelper/espeak/sconscript).

### Updating the version used by NVDA

1. Start from a clean branch off of NVDA `master`
   1. Check out the latest NVDA `origin/master` and create a new branch.
   1. Do a git clean to ensure the working directory is clean.
1. Ensure submodules are up to date
   1. Synchronize submodules with `git submodule sync`
   1. Update submodules with `git submodule update --init --recursive`
1. Checkout the new eSpeak-ng revision to try.
   1. Change to the `include/espeak/` directory
   1. Do `git fetch` to get the latest from the espeak-ng repo
   1. Do `git checkout origin/master` or whichever espeak-ng ref you wish.
1. Look at changes in the upstream build configuration and update our custom build.
   1. Diff the CMake config (`cmake/config.cmake` and `src/libespeak-ng/config.h.in`) with the previously used commit of espeak.
     * e.g.: `git diff b0b605c8a 56f2e9c73 cmake/config.cmake src/libespeak-ng/config.h.in`
   1. Changes to dictionary compilation should be reflected in `espeakDictionaryCompileList`.
   Diff `espeak-ng-data/lang`.
     * e.g.: `git diff --diff-filter=AD --stat --name-status b0b605c8a 56f2e9c73 dictsource ':(exclude)*_emoji'`
1. Update our record of the version number and build.
   1. Change back to the NVDA repo root.
   1. Update the `/DPACKAGE_VERSION` and other feature definitions in [`nvdaHelper/espeak/sconscript`](../nvdaHelper/espeak/sconscript).
      * The preprocessor definitions are provided here instead of in [`nvdaHelper/espeak/config.h`](../nvdaHelper/espeak/config.h).
      * [`nvdaHelper/espeak/config.h`](../nvdaHelper/espeak/config.h) must still exist because eSpeak includes a `config.h` header.
      * Compare against the upstream generated config in [`include/espeak/src/libespeak-ng/config.h.in`](./espeak/src/libespeak-ng/config.h.in), and use [`include/espeak/src/windows/config.h`](./espeak/src/windows/config.h) only as a legacy reference for `PACKAGE_VERSION`.
   1. Update NVDA's [dev environment documentation](../projectDocs/dev/createDevEnvironment.md#git-submodules) and [changelog](../user_docs/en/changes.md) with eSpeak version and commit.
      * Include any changes to supported languages in the changelog.
   1. Build NVDA: `scons source`
      * Expected warnings from eSpeak compilation:
         * On the first build after changes, all languages may show this warning.
         Our build intentionally compiles using the `phonemetable`.

         ```log
         espeak_compileDict_buildAction(["include\espeak\espeak-ng-data\uz_dict"], ["include\espeak\dictsource\uz_list", "include\espeak\dictsource\uz_rules"])
         Can't read dictionary file: 'C:\Users\sean\projects\nvda\include\espeak/espeak-ng-data\uz_dict'
         Using phonemetable: 'uz'
         Compiling: 'C:\Users\sean\projects\nvda\include\espeak\dictsource/uz_list'
               121 entries
         Compiling: 'C:\Users\sean\projects\nvda\include\espeak\dictsource/uz_rules'
               35 rules, 26 groups (0)
         ```

1. Run NVDA (set eSpeak-ng as the synthesizer) and test.
Test any added languages, you may need to find a sample of the language text to test with.
1. Ensure that the log file contains the new version number for eSpeak-NG.

### Troubleshooting Build failures

If python crashes while building, check the log.
If the last thing is compiling some dictionary try excluding it.
This can be done in [`nvdaHelper/espeak/sconscript`](../nvdaHelper/espeak/sconscript).
Remember to report this to the eSpeak-ng project.

If the build fails, take note of the error, compare the upstream CMake configuration and mirror any relevant changes in our `sconscript` file.

### Known issues

Due to problems with emoji support (causing crashes), emoji dictionary files are being excluded
from the build, they are deleted prior to compiling the dictionaries in the
[`nvdaHelper/espeak/sconscript`](../nvdaHelper/espeak/sconscript) file.

## Manually testing eSpeak-ng

If you wish to test eSpeak-ng directly, perhaps to create steps to reproduce when raising an issue for the eSpeak-ng project, consider feeding SSML directly to the executable provided by the project.

The [eSpeak docs](https://github.com/espeak-ng/espeak-ng/blob/master/docs/index.md) are worth reading.
They describe the various [(eSpeak-ng) command line arguments](https://github.com/espeak-ng/espeak-ng/blob/master/src/espeak-ng.1.ronn) (note also [speak-ng command line](https://github.com/espeak-ng/espeak-ng/blob/master/src/speak-ng.1.ronn)), and [instructions to build](https://github.com/espeak-ng/espeak-ng/blob/master/docs/building.md#windows) an `.exe` from a commit of eSpeak, locally on Windows.
However, historically the Windows build for espeak-ng hasn't been well maintained, with periods of build failures.
It is also different from the build approach within NVDA.

1. Install an (x86) release: <https://github.com/espeak-ng/espeak-ng/releases>
   `espeak.exe` is in `C:/Program Files (x86)/espeak-ng/`
   Adding it to your path temporarily will make the following easier.
1. Write out [some SSML](https://github.com/espeak-ng/espeak-ng/blob/master/docs/markup.md) that demonstrates the problem.

   ```sh
   $ cat /c/work/test-espeak-ssml.txt
   <prosody pitch="+100">I am now speaking at an extra high pitch.</prosody>
   <break time="1s"/>
   <prosody pitch="1">I am now speaking at the default pitch.</prosody>
   ```

1. Feed the SSML into `espeak-ng.exe`

   ```sh
   $ cat /c/work/test-espeak-ssml.txt | ./espeak-ng.exe --stdin -m
   # eSpeak-NG should output speech
   ```
