# Building NVDA Forks with AppVeyor

[//]: # (Links for use elsewhere in the document)
[git]: https://www.git-scm.com
[GitHub]: https://www.github.com/
[NVDA]: https://github.com/nvaccess/nvda/
[NV Access]: https://www.nvaccess.org/
[AppVeyor]: https://appveyor.com/
[Contributing]: https://github.com/nvaccess/nvda/blob/master/projectDocs/dev/contributing.md
[Recommended Build Environment]: https://github.com/nvaccess/nvda/blob/master/projectDocs/dev/buildingNVDA.md
[Create Dev Environment]: https://github.com/nvaccess/nvda/blob/master/projectDocs/dev/createDevEnvironment.md
[Self-signed Build]: https://github.com/nvaccess/nvda/blob/master/projectDocs/dev/selfSignedBuild.md
[YAML]: https://yaml.org/
[gh]: https://cli.github.com/
[nvda-devel]: https://groups.io/g/nvda-devel
[gist]: https://github.com/ajourneythroughdatascience/blog/blob/master/version-control/what-are-github-gists-and-how-to-use-them/what-are-github-gists-and-how-to-use-them.md#what-are-github-gists-and-how-to-use-them

Author: Luke Davis, Open Source Systems, Ltd. ([@XLTechie](https://github.com/XLTechie) on [GitHub])

Copyright: &copy; 2024, NV Access Limited and Luke Davis, all rights reserved.

## Introduction

For various reasons, you may not be able to, or may not wish to, construct the [Recommended Build Environment] for NVDA.
However, you still might want to create, build, and test your own modifications to the NVDA codebase.

Cloud-based services are available to build software for those not wanting to build it locally, and this is an increasingly popular option in the software development field.
* [GitHub Actions](https://github.com/features/actions), is one example.
* Another example is [AppVeyor], which is the service that NV Access itself uses to build NVDA's production versions, alphas, and to test pull requests submitted by the community.

It is [AppVeyor] that we will be exploring below.
This document seeks to provide a set of step by step instructions, to enable anyone with a fork of NVDA to build it using the [AppVeyor] platform, without requiring any local build environment beyond the fork itself.

## Structure of this document

In this document, all major sections are titled at heading level two.
Subsections are indicated at heading level three, and subsidiary items are given heading levels four and five.

That said, the best way to use this document, is to start at the beginning, and work your way through to the end, at least the first time you create an AppVeyor build setup for NVDA.

## Prerequisites

Before following the steps in this how-to, you will need a [GitHub] account, and an [AppVeyor] account.
If you don't yet have an AppVeyor account, it is possible for you to login to AppVeyor with your GitHub credentials.
To do this, when you go to create your account on AppVeyor, choose "log in with GitHub" as your sign in method.
Doing it this way is not required to complete any aspect of this how-to, but it can be convenient to connect those two accounts from the start.

It is assumed that you have already read the [NVDA] document on [Contributing], and the "[Create Dev Environment]" file's section called "Getting the Source Code", as you will need to have an [NVDA] fork already in place on your development computer.

Furthermore, you should already be generally familiar with [git], [GitHub], and how to work with repositories.
This how-to won't go into any of these basic areas in any detail, and will only summarize topics the reasonably experienced developer is likely to understand already.

While it is not strictly required, it is highly recommended that you install the [gh] tool, so that you may control various aspects of [GitHub] from the commandline.

## Situations not covered in this how-to

* This document assumes your NVDA coding workflow involves branching off of `master` (or another official branch such as `beta`); working on the code; and pushing the result to your NVDA fork.\
We don't cover, and the modifications we make to `appveyor.yml` are not tested with, any workflow which involves issuing pull requests against your NVDA fork.\
It may work, but results are unknown.
* Currently, we disable elements related to code signing, and don't attempt it.\
It is discussed in the [Self-signed Build] document, but not in the context of building forks on [AppVeyor].

## Overview

We will undertake the following general steps:
* Setup GitHub and local environments.
* Tell AppVeyor where to find the new repository.
* Configure AppVeyor to find the config file.
* Modify the AppVeyor configuration already included with NVDA to work for unofficial purposes.
* Try the first build!

## Getting started

If you haven't already, per the "Prerequisites" section above, fork a copy of the main [NVDA] repository into your GitHub account.
You can call your fork "NVDA", or "my_nvda", or whatever you want.
For the rest of this how-to, we will assume you have called it "nvda".

Next, clone the fork to your local dev environment, and perform the other source code setup tasks recommended in the "Getting the Source Code" and "Keeping the fork in sync" sections of the [Create Dev Environment] document.

If you are using the "[gh]" tools for working with [GitHub] from the commandline, you can do both steps in one command with:

```sh
gh repo fork --clone=true --remote=true nvaccess/nvda -- --recurse-submodules
```

## Where to put the build file

In order to actually build NVDA, AppVeyor has to be given a set of instructions to follow.
This is done using the `appveyor.yml` file, which is a text file in the [YAML] format.
(More on the format and content later.)

The most common placement for this file, is in the root directory of your repository.
Unfortunately, since NV Access already uses AppVeyor for official builds, it would be difficult to keep your build file in the root directory of your NVDA fork.
This is because you will need to permanently change a few items in that file, and you wouldn't want that private build file "contaminating" your pull requests or diffs.

[AppVeyor] has thought of this, and enables you to use a publicly accessible URL to retrieve your `appveyor.yml` file, overriding any `appveyor.yml` that appears in the repository.
That is the option we will use, to provide our customized `appveyor.yml` file.

The most obvious solution that suggests, is to use a public facing web server.
To do so, simply upload the `appveyor.yml` file; and provide the URL to AppVeyor as directed below in the "Configuring AppVeyor to build the project" section.
Be sure to set the content type and filename [as directed by AppVeyor in this document](https://www.appveyor.com/docs/build-configuration/#alternative-yaml-file-location).

As suggested at that link, you may also use a GitHub [gist], which is described below in further detail.

It is also possible to store your `appveyor.yml` file in an uncompiled public branch in your repo, and use a direct [GitHub] URL to point to that file.
However unless you have to modify the build scripts themselves (which you don't just to build a fork of NVDA), this is not a recommended approach.
If you do want to modify build scripts, or wish to examine this method, review the section "Advanced topic: a build control branch", at the end of this document.

### Storing appveyor.yml in a gist

If you use the [gh] commandline tools, a [gist] is likely the easiest way to manage your build configuration file.
Alternatively, gists can be managed on the web, but the process for creating and editing them was not perfectly accessible as of 2023, so [gh] is recommended, and web instructions are not provided.

To create a gist containing the `appveyor.yml` configuration file:

1. Change to the directory of your NVDA fork.
2. Type the following--replacing "YOUR_GITHUB_USERNAME" with your actual username, and changing the rest of the description in quotes however you prefer:

       gh gist create appveyor.yml --desc "YOUR_GITHUB_USERNAME's appveyor.yml for building NVDA"

If it worked, you should receive some output similar to the following:
```
- Creating gist appveyor.yml
Created gist appveyor.yml
https://gist.github.com/YOUR_GITHUB_USERNAME/A_LONG_STRING_OF_CHARACTERS_IDENTIFYING_YOUR_GIST
```

It is best to keep that URL because you will need it later.
Although if you ever do lose it, you can find it again with:

```sh
gh gist list
```

That will show your available gists.
Match the description from the second column with the description you used when creating your [gist].
The first column of that line will contain the GUID from when you first created the gist (the part that appeared after your username and the forward slash in the URL), which you can use to reproduce the URL.

Now, each time you want to edit the `appveyor.yml` file (you will need to in the next section), type the following:

```sh
gh gist edit URL_OR_ID
```

Replace "`URL_OR_ID`" with the URL you kept from before, or the ID string you get from `gh gist list`.
This will open your text editor, and present a temporary copy of the file for you to edit.
Make your modifications, save, and exit the editor.
The file will be returned to GitHub with your latest modifications, and the `appveyor.yml` file from the fork will remain untouched.

Lastly, give the URL of the gist directly to AppVeyor, as described in the "Configuring AppVeyor to build the project" section below.

## Setting up the project on AppVeyor

It's now time to log in to AppVeyor, and configure the project.
Go to the [AppVeyor sign-in page](https://ci.appveyor.com/login).

* If you created an account with an email address and password, enter them.
* If you used a developer account, such as your [GitHub] account as recommended above, choose that provider from the list on the page, and follow the prompts.
* If you have recently logged in from the same browser, you shouldn't have to log in again.

1. The default page for AppVeyor, once you have logged in, is the projects page. If that's not where you ended up, find and go to the projects page.
2. Find and select "NEW PROJECT".
3. If you have not already authorized AppVeyor as a Github app, select "GitHub" under the "Cloud" heading, and do so now.
    *(FixMe: more instructions may be needed here.)*
4. Move to the "Select repository for your new project" heading, and then to the heading representing your GitHub username.
5. Below that heading, you should find your GitHub repositories listed. Go to the one representing your NVDA fork.
6. This part is less than perfectly accessible via the usual methods: you will need to use `NVDA+numpadDivide`, to route the mouse to the repository name, and then `numpadDivide` to click on it.
    You may also be able to use object navigation to achieve this.
7. When you have selected the repository name, an "Add" link will appear below it.
    Select that link normally, and you will have attached the repository to AppVeyor.

## Configuring AppVeyor to build the project

After properly executing the previous section, you will be on the AppVeyor project dashboard, for your NVDA fork repository.

1. Find and select the "Settings" link (last item on the first list under the project name heading).
2. Change the following settings:
    * "Custom configuration .yml file name": you must set this to the direct web access to your raw `appveyor.yml` file.
        This may be a personal website, or the URL to a [gist], as discussed in prior sections.
    * Find the checkbox for "Rolling builds".
        You don't have to, but probably do want to select this.
        read more about [rolling builds here](https://www.appveyor.com/docs/build-configuration/#rolling-builds).
    * You may want to select the checkbox for "Do not build on pull request events", depending on your workflow.
        As noted earlier, this how-to is not optimized for pull request based workflows.
3. Press the "Save" button at the bottom.
    There is no way with NVDA to determine that the save was successful.
    You can press it more than once with no ill effect, or just assume it worked.

## Editing appveyor.yml

Once you've figured out where you will put your `appveyor.yml` file, and have given [AppVeyor] that information, you will need to edit it to work.

`appveyor.yml` is divided into sections.
[AppVeyor] has quite comprehensive [documentation](https://www.appveyor.com/docs/appveyor-yml/) about their [YAML] format, and the AppVeyor build configuration specifically.
The many possibilities are out of scope for this document, but the minimal necessary configuration is given below.

To get started, open your `appveyor.yml` file for editing, and follow along.

If this is your first edit of a [YAML] file, be aware that like Python, the spacing and indentation is very important.
Unlike Python, however, tabs are not the preferred indentation character for the [NVDA] project--spaces are.
The indentation generally progresses by one space further inward, for each keyword that modifies the starting keyword.
(Technically, [AppVeyor] wants two spaces per level of indentation according to their [spec](https://www.appveyor.com/docs/appveyor-yml/), but [NV Access] only uses one, so that's what we'll use here.)

The YAML file consists of several sections, each starting with a keyword, followed by a colon.
The section may only hold one value or element, in which case it is usually written on the same line as the introductory keyword.
For more complex sections, the initial keyword is on a line of its own, and the section that contains its value appears on the following lines.
At the end of each such multi-line section, there is usually a blank line left to aid in readability.
You can read more about the [YAML] format, though you shouldn't need to understand it in great detail if you are primarily copying and pasting from this how-to.
The last thing to note, is that this document is based on the 2024 version of the file.
If the file has changed by the time you read this, assume the new version is more accurate, and try to adapt these instructions to fit.
In particular, if any section is listed below as not needing to be changed, but the representative text here is different than what the file in the [NVDA] repository indicates: ignore what is written here and make your modifications based on what's in the newest file provided by the project.

### The top of the file: don't change

The first couple lines of the file, are generally used to specify the build operating system and support software, and the basic version string to be used by built executables.
The existing lines are fine for that; it is best not to change anything here.

### Branches to build

You will first need to edit the "branches" keyword.
This tells AppVeyor what branches to build.
For [NV Access], it is necessary to build production releases, pull requests, try builds, and so on.
That means the file currently contains something like this:

```yaml
branches:
 only:
  - master
  - beta
  - rc
  - /try-.*/
  - /release-.*/
```

That tells AppVeyor, to build only when pushes are made to those branches.
But that is basically the opposite of what we want in a non-NV Access fork!

Most likely, you only want to build new branches that you push to the fork.
You probably don't have an interest in building master, beta, etc., as these branches will often become very out of sync with their NV Access counterparts.
To achieve this, change the keyword "`only`", to "`except`" in this section.
Now, `master`, `beta`, etc., will never be built by AppVeyor on your fork.

If you have some other requirements, modify this section accordingly.

For example, let us say that you do all of your work in branches with detailed topic names such as "`addXFeature`".
Once you have a successful build, and want to do a pull request: you copy the work to a "`fix#####`" or "`f#####`" branch, reflecting the issue number of the fixed issue.
But, you don't want your AppVeyor worker to build these, both because NV Access's setup is going to build them; and because if you use any notification section (see "Advanced topic: email notifications" at the end), you don't want NV Access getting notified and bothered by your fork's CI activity.
To implement this model, you can use the following branch exceptions:

```yaml
  - /^[Ff]\d+$/
    - /^[Ff][Ii][Xx](\d+)$/
```

Your whole branches section would look like this:
```yaml
branches:
 except:
  - master
  - beta
  - rc
  - /try-.*/
  - /release-.*/
  - /^[Ff]\d+$/
  - /^[Ff][Ii][Xx](\d+)$/
```

Now branches `master`, `beta`, and `fix1234`, will not be built even if you push to them.

### Changing the publisher

Next up, is the "`environment`" section.
The first thing you need to change here, is the publisher.
Search for "`scons_publisher`".
Remove "NV Access" and replace it with your identifier.
This can be your name, your organization's name, or even your GitHub handle.
It is just a string that is used when building certain files.

### Turning off undesired features

NV Access has already configured `appveyor.yml` to work well for the compilation of NVDA.
It calls out to multiple Powershell based build scripts, to modularize the build process.
However, there are several things that these scripts do, that are inappropriate for an NVDA fork which does not have access to NV Access's infrastructure, security keys, etc.
Those features could be made to work, through significant modifications to the build scripts; but that is beyond the scope of this how-to.
Therefore, these sections should be "turned off", or your builds will fail.

In the environment section, you will find several "feature" variables set to "configured", following a brief comment explaining their purpose.
Make sure the following lines are commented out by putting a hash symbol (#) right before the first text on each line:
* `feature_uploadSymbolsToMozilla`
* `feature_buildAppx`
* `feature_crowdinSync`
* `feature_signing`

Optionally, you may also comment out the line which sets `feature_buildSymbols`.
If you don't need the symbols, there's no reason to build them, but other than a small increase to build time, it doesn't hurt anything to leave this line alone.

## Building and waiting

With the branches adjusted, and those four variables commented out, the [AppVeyor] build process should now work for your fork!
Exit the editor, and try pushing some new code to a branch!

```sh
cd nvda
git checkout master
git submodule update --init
git checkout -b addXFeature
# Edit edit edit, hack hack hack
git commit -am 'Initial commit of new feature code. This feature does amazing thing X!'
git push -u myFork
```

If everything went as intended, [AppVeyor] will now start building your "`addXFeature`" branch.
The build process is likely to take approximately 30 minutes.
You can observe the build in progress, under the "Console" section of the AppVeyor interface, including a constant timer of how long it is taking.

### Trouble shooting

If your project doesn't seem to be building, you may try the following:

* Look for the "`CANCEL BUILD`" control for the in-progress build.
    If you find it, it means the build is running.
    If not, continue down this list.
 * Try using the "`Current build`" link under the project name heading, to load a new copy of the project view.
* If something still doesn't appear to be working correctly, try refreshing the project page with F5.
* If there still isn't a current build being shown, keep reading down the page to find out if the build failed in some way.

If the text from your last commit appears on the page, you know at least that AppVeyor detected the push event.
You will then need to determine if, and how, the build failed.

* If the "`Console`" section isn't helpful, try reading anything under the "`Messages`" section.
* If you still can't figure out what happened, do a page search for the "`Log`" link.
    Once you find that, hopefully the log can explain what you need to know.
* The "`Events`" link may also be helpful, to find out what happened.

If nothing even tried to build, there may be an error in your `appveyor.yml` file (although if it is a syntax error, you will be informed).
If there is no [YAML] error, and there is no evidence of the attempted build, there may be a disconnect between your fork's repository and [AppVeyor].
It may be useful to attempt to build master, using the "`NEW BUILD`" link, to at least determine if AppVeyor can access your GitHub repository.

You may try asking for help on the [nvda-devel] mailing list, or the [AppVeyor] forums.

## When the build completes

When the build finishes, you can find the executable installer and other files (including lint and other test results) in the "Artifacts" section.

Tip: the list (`l/`shitft+l`, `comma` and `shift+comma`), and list item (`i`/`shift+i`) NVDA quick nav commands, can be very helpful in speeding up navigation of the AppVeyor build related pages, if you learn the page layout.

## Conclusion

If your first build was successful by following this document, then congratulations!

We hope that these instructions have proven to be useful.
There are a couple of advanced topics below, but you have now learned the essentials of building NVDA forks with AppVeyor.
Please submit issues on the [nvda] GitHub issue tracker, if you notice any errors, or any areas where you think the how-to should be improved.

Thank you for reading!

## Advanced topics

* Many developers may desire email notifications upon build completion.
* A few developers may want to work on NVDA's build scripts or build process directly, which requires a somewhat different approach from the one described above.

If you fall into either of these categories, please read the appropriate subsection below.
If neither of these topics interest you, you may stop reading at this point.

### Advanced topic: email notifications

AppVeyor provides many methods for being [notified](https://www.appveyor.com/docs/notifications/) of various build events.
One form of notification is documented below.

It is likely that the notification which most developers will want, is an email upon success or failure.
While there are many possibilities for configuration and customization, what follows is a detailed email notification that should serve most needs adequately.

#### Add a notifications section to appveyor.yml

Edit your `appveyor.yml` file.
Move to the end of the file, and insert a blank line.
After the blank line, paste in the following section, making sure to preserve the indentation.

```yml
notifications:
  - provider: Email
    to:
      - '{{commitAuthorEmail}}'
    message: >-
        <p>{{projectName}} {{branch}}</p>
        <div>{{#jobs}}
        <p>Messages:<br />
        {{#messages}}
        {{message}}<br />
        {{/messages}}</p></div>
        <div><p>Artifacts:<br />
        {{#artifacts}}<ul>
        <li><a href="{{url}}">{{fileName}}</a></li>
        {{/artifacts}}</ul>
        {{/jobs}}</p></div>
    on_build_success: true
    on_build_failure: true
    on_build_status_changed: true
```

Save your edit, and you should now receive detailed email notifications to the committer email address you use with git, whenever a build succeeds or fails.

### Advanced topic: a build control branch

While the gist or personal website methods for storing `appveyor.yml` are likely sufficient for most needs, those developers who wish to change NVDA's build scripts or the AppVeyor process itself, will need a different approach.

If all you're doing is modifying a build script in a branch, for which you intend to submit a pull request to NV Access for merger into NVDA as a whole, you don't need this method.
However, if you want to change the NVDA build process for all builds of your fork, *without* submitting that changed build process to NV Access, you will run into a problem.
You can't just change scripts in a normal branch, because they will either override the NV Access scripts for that single branch; or, if you put them in e.g. the `master` branch, they will leak into all your future branches, and contaminate any pull requests.
We need to build with your modified scripts, but not let them show up in any normal branches.

To solve this problem, you can create a separate branch, that is never merged back to master, and that is never part of any pull request.
You can keep all build related files in this build specific branch of your fork.

The rest of this subsection will detail that process.

#### A branch for your build file

Previously, you may have used a gist, or a personal website, to contain your `appveyor.yml` file, and fed it to [AppVeyor] using a direct URL.
Now, however, we will make a branch that is dedicated to nothing other than our customized build process.
We will store the `appveyor.yml` file there instead, as well as any build scripts we may customize.

Change into the directory of your fork, and create and checkout a new branch based on master:
```sh
cd nvda
git checkout master
git pull
git checkout -b _myBuild
```

Here, we have called the branch "`_myBuild`" just to be clear, but you could call it "`appveyor`", or anything you want; the name doesn't matter, as long as it makes sense to you, and is unique within the NVDA project.

None of the files in this branch matter, except for `appveyor.yml`, and the files under the `appveyor` directory.
You are never going to merge this branch with master.
It exists strictly to allow you to keep your copy of `appveyor.yml`, and any customized build scripts, separate from the NV Access copy in the master branch.

#### Editing appveyor.yml for your build branch

First, you should make all the edits already discussed under the "Editing appveyor.yml" section above.
However, you need to make the following additions while editing:

##### Avoid building the build branch

While you're editing the "`branches:`" section, you need to add your build branch.
This branch is just informational for AppVeyor, and should never actually be built.
Thus, for example, the branches section might look like:

```yaml
branches:
 except:
  - _myBuild
  - master
  - beta
  - rc
  - /try-.*/
  - /release-.*/
```

##### Add a variable for your build branch

While you're editing the "`environment:`" section, you will need to add one variable of your own.
This will allow you to fetch any customized build scripts from your `_myBuild` (or whatever you called it) branch.

So, after what is already there (whether or not you have commented all of the "`feature_`*" variables out as directed in "Turning off undesired features"), add a properly indented line such as:

```yaml
 myBuildBranch: _myBuild
```

**Be sure to replace "`_myBuild`" with the name of your build branch (created above), if different.**

#### Editing the install section

The "install" section of `appveyor.yml` sets up the environment on which the application (NVDA, in this case) is built.

If we do nothing, the scripts that it calls will come from the branch you are trying to build, not the branch that configures your build.

To explain that another way: after your AppVeyor configuration is finished and working, you will start editing NVDA code, which you will want to compile.
For example you may have edits in the "`testCode`" branch.
So you push the "`testCode`" branch to GitHub.

AppVeyor starts up, and attempts to compile that branch, using the `appveyor.yml` file from your provided URL.
Your `testCode` branch is checked out into your AppVeyor build environment.
At this point, the build scripts that AppVeyor is using, are the ones found in `testCode`.
However you aren't working on build scripts in `testCode`, you're working on some other part of the NVDA codebase, so the build scripts are the default ones from the NVDA master branch, which is as it should be.
But the build scripts you have modified (we will be doing that below), are in your build branch (`_myBuild`).
We must somehow make AppVeyor go out and get those scripts, to use instead of the ones it already has.

We do that in the "install" section.
Below, we give the current contents of that section, line by line, with discussion for each.
The revised portion appears in full at the end.

##### Lines 1 through 3

Current content:

```yaml
install:
 - ps: |
    "INSTALL_START, $(Get-Date -Format 'o')"| Out-File ../timing.csv -Append
```

These lines simply initiate the section, and record the timing information for later use.
These should be left the same.
However immediately after these lines, you should insert the following new lines:

```yaml
 - git fetch origin %myBuildBranch%
 - git checkout origin/%myBuildBranch% -- appveyor
```

This should cause everything in the `appveyor` directory, to be replaced with the same named files in your build branch's `appveyor` directory.
Of course, if there are other files or folders you need to do this with, you can add them to the `git checkout` command as well.

##### The rest of the install section

After that, you can use the remainder of the install section as it appears in the original.
At the end, the full install section should look like this:

```yaml
install:
 - ps: |
    "INSTALL_START, $(Get-Date -Format 'o')"| Out-File ../timing.csv -Append
 - git fetch origin %myBuildBranch%
 - git checkout origin/%myBuildBranch% -- appveyor
 - ps: appveyor\scripts\setBuildVersionVars.ps1
 - ps: appveyor\scripts\decryptFilesForSigning.ps1
 - py -m pip install --upgrade --no-warn-script-location pip
 - git submodule update --init
 - ps: |
    "INSTALL_END, $(Get-Date -Format 'o')"| Out-File ../timing.csv -Append
```

#### Finishing with appveyor.yml

With the modifications made, you can save `appveyor.yml`, and put it in your remote branch:

```sh
git add appveyor.yml
git commit -m "Modified appveyor.yml to support the custom build branch"
git push -u myFork
```

Lastly, you need to tell AppVeyor where to find the file.
Generally, you will follow the steps in the "Configuring AppVeyor to build the project" subsection above.
However, when entering the URL, you'll want to use a [GitHub] URL which points directly to the latest version of `appveyor.yml` in your fork's build branch.
Replace the relevant capitalized place holders in this URL, and enter it in the appropriate field:
```
https://raw.githubusercontent.com/GITHUB_USER_NAME/REPO_NAME/BUILD_BRANCH/appveyor.yml
```

#### Modify your build scripts

Now, you are able to make whatever changes you want to the build process for your fork, by modifying the files under the `appveyor` directory in your `_myBuild` branch.

For example, if you wanted to use both virtual CPU cores which [AppVeyor] offers during your compilation, you could modify:
```
appveyor/scripts/setSconsArgs.ps1
```
by changing line six from:
```
$sconsArgs = "version=$env:version"
```
to:
```
$sconsArgs = "version=$env:version -j 2"
```

If you save, commit, and push that change on your `_myBuild` branch: the next time you build any branch in your fork, scons will be called with the `-m2` switch, and will use both cores.

*N.b. You could also make that particular small change in `appveyor.yml`, by modifying the "`build_script`" section.
But this was just a minor example of what can be done.*
