<!-- 
Community triage information from 
https://github.com/nvaccess/nvda/wiki/Issue-triage-help
 -->


## Intent
This page intends to outline some of the information that might be helpful to those trying to triage issues.

Most of the issues raised on the NVDA Github repository fall into one of the following categories:

- adding support to new applications
- adding new features in NVDA
- adding new features to support 3rd party applications better
- bug reports

Firstly we want to catch high priority issues and ensure that they are attended to first.
This might be things like:

- a crash of NVDA
- synthesisers not working correctly
- an error in an existing feature.

Secondly, we want to ensure that there is enough information on the issue so that it can be well understood and work can start when it comes to the front of the queue. The sooner we do this, the more likely it is that we will get the information we need.
Most of the information required is asked for in the Github issue templates, so this is a great place to start.

## Check for duplicates
Pick a few keywords and search the NVDA repository on Github. We can also check if there is already a pull request in the works that may fix this issue.

## What kind of issue is it?
Can we label this as a regression, a requested change of behaviour, or a requested new feature?

### Regression
The behaviour of the software has changed, unintentionally. This may mean that a feature has stopped working altogether or there may be an error sound, or perhaps a crash.

### New features
This is something new, that NVDA does not do yet.

### Change of behaviour
The issue describes "Currently NVDA does something, but I would like it to do something else instead."

## Is there a work around?
We may already know of a work around, any existing alternatives, or if there is any way to achieve the request already?

## Information to collect.

This is the kind of information that might help when investigating the issue further.

### Regressions

- How is the regression triggered? We may call this the steps to reproduce, perhaps even STR for short. What this means is, that we are looking for the set of steps to make the bug happen on our own system.
- What happens / what is the actual behaviour? Some examples might be:
 - a crash
 - a freeze
 - an error noise
 - A log message
 - If there was an error noise or log message, was there any unexpected behaviour aside from this? For example, did NVDA fail to report something it should have?
- Even if it seems obvious, what should happen instead? 
 - Its worth clarifying this with the user, it helps to make sure everyone is on the same page, and that we truly understand what the issue is about.
- What version of NVDA was being used. Its good to get something like: 'stable', 'next', 'rc', 'release'. But much better to get the exact version of NVDA, retrieved from the NVDA menu by going to "Help" then "About". 'next-13896,5322f3d8'
- In which version of NVDA did this work as expected?
- If some other software is needed to reproduce the issue, it helps to know what that software is and what version is being used with NVDA. It's also useful if a test case / document is provided.
- Some behaviour is specific to operating systems or versions of operating systems. Sometimes a bug can only be reproduced on that particular version of the operating system. So its important to get this information as well. Similar to the NVDA version information, more specific is better. For instance its good if we know the issue occurred on: 'Windows 7', 'Windows 10 Insider'. But even better is to know the version and build too: 'Windows 10, fast insider, version 1703, build 16170.1000'.
- A copy of the (debug) log
- If it exists, a crash dump file.
- Can anyone else reproduce the issue?
- Has anyone else tried and failed to reproduce the issue?

This in particular can be quite time consuming for NV Access, but would be an excellent way for members of the community to contribute. By checking if you can reproduce issues on whatever system configurations you have around, or perhaps using VMs as well and reporting back the results.

### New features

Typically there would be some kind of description of the requested behaviour and why a user wants this behaviour.
To start with we can start with a general use case, and turn this into a set of user stories.
If possible we should try to identify any variations on the use case presented.

In order to assess the impact of the new feature it's useful to make a note of who the feature benefits, and if we require different behaviour for speech, braille, or visual users? This has two parts, how meaningful this feature is to a single individual, and how many individuals this will benefit.
Finally it may be useful to know if this is solved by other screen readers.
If so how does it work there?

### Change of behaviour

In a way this is like a combination of both a bug and a new feature request, and we likely want most of the information expected on both of those issue types.

However, the most important pieces of information for this kind of request are:

- How to reproduce the behaviour?
- What exactly is the current behaviour?
- What is wrong with the current behaviour?
- What should NVDA do instead?

Essentially this boils down to:

- What is the use case / user stories,
- How does it differ from the intended use case of the feature?

## Use cases / user stories
There are three things we are trying to define: Who, What, and Why.
This can often fairly naturally be stated in the following form. As a BLANK (the who), I want to be able to BLANK (the what) so that I can BLANK (the why).

Here is an example from a recent Github issue:

> As a Braille user, I notice that the cursor is a different shape when tethered to focus  than it is when tethered to review. This is so that I can tell the difference between the two modes.

### Who

- Who does it affect? (for instance: Braille users, Speech users, developers working on accessibility for their websites/apps, nvda developers)
- Knowing who, helps to give an estimate on how many users this will help.
- It also can help to highlight differences in requirements for different users. This happens when we are unable to define the same use case for two groups of users.

### What

- This can be a step by step of what they expect to do, and the kind of output they expect along the way.
- Things to consider here:
 - Does this need to work with other software? If so, what version?
 - Particularly when working with other software, it's helpful if an example document or file can be provided. Perhaps a relevant test case?

### Why
Often the hardest one, but also the most valuable.

- Why do they want to do this?
- What does it help them to achieve?
- It's valuable because it brings further understanding about the background that led to the what.
Perhaps once we have this background, a simpler what can be proposed.

## Summarise the issue
It's common that this process of collecting information will result in many comments on the issue.
As the github issue grows, with more comments, questions, and discussion, it's useful to summarise the issues periodically.
This helps to condense various back and forth discussions into the final result.
This will make it easier for someone to quickly pick up the issue and understand it by reading the summary comment.
This also serves to re-iterate decisions that have been made throughout the discussion and ensure that everyone is on the same page.

<!-- 
NV Access triage process from 
https://github.com/nvaccess/nvda/wiki/Triage-process/
 -->

For transparency, the following is a brief outline of the process NV Access is following for issue triage.
If you would like to help with the triage process (which is an excellent way to make a contribution to NVDA) please refer to [issue triage help on the wiki](https://github.com/nvaccess/nvda/wiki/Issue-triage-help)

### Missing attachments
NV Access migrated tickets from our old issue tracker ('Trac') into Github issues. These issues can be identified by having an author of `nvaccessauto`. Some of these issues have comments that indicate an attachment should be available, but it is not. All of these Trac attachments are now accessible at: https://www.nvaccess.org/files/nvdaTracAttachments/ (then the Github issue number). So as an example, for issue [#2396](https://github.com/nvaccess/nvda/issues/2396), get the attachments from https://www.nvaccess.org/files/nvdaTracAttachments/2396
If you come across one of these missing attachments, please upload if you think they're relevant to GitHub. Note you'll need to pay attention to Github's attachment naming restrictions, if it fails try zipping it.

### How prioritisation works
We differentiate between the priority for bugs (labelled `bug`) and new features (labelled `feature`). Rather than assign a priority to issues with the `feature` label, typically we try to group new features into a project of related work. We should try to ensure that new features are [well defined](https://github.com/nvaccess/nvda/wiki/Issue-triage-help#new-features-1) before applying the `feature` label. One exception here might be if we can determine that a feature is not something we are likely ever to work on. In this case we should apply `P4` and explain this is not something we are going to look at but will be happy to accept a pull request for. We also have a label for `enhancement`, think of this as a more internal facing change. For instance, editing code comments to provide clearer / more complete information, or extending an internal framework/API to unblock other issues.

Bugs/regressions are given priorities based on an estimate of their severity, impact and implementation cost:

- `P1` issues are typically crashes or severe errors that should be fixed immediately.
- `P2` issues should be among the next issues fixed. Try to start on the oldest of these issues.
- `P3` issues are less likely to get fixed, we hope to get to them "one day". However if something changes (severity/impact/cost) the priority can be reassessed.
- `P4` issues probably won't be worked on by NV Access, however we will be happy to provide implementation guidance and accept a Pull Request.

Due to the difficulty in assigning priorities to individual issues, recently (2019) NV Access has asked members of the community to provide their top 2 issues. This data allowed us to find trends resulting in a re-prioritisation of our efforts. While this exercise allowed us to tackle the most important issue for the majority, we are aware that critical issues for smaller groups may be missed. So the above process should still be followed, especially for P1 or P2 issues. If an issue is critical to you, please comment on the issue and explain why.
