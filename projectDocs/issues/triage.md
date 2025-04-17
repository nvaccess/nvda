## Intent
This page intends to outline some of the information that might be helpful to those trying to triage issues.

Most of the issues raised on the NVDA GitHub repository fall into one of the following categories:

- adding support to new applications
- adding new features in NVDA
- adding new features to support 3rd party applications better
- adding support for new (web) accessibility standards
- bug reports

Firstly we want to catch high priority issues and ensure that they are attended to first.
This might be things like:

- a crash of NVDA
- synthesisers not working correctly
- an error in an existing feature.
- an essential function of an application ceased working with NVDA

Secondly, we want to ensure that there is enough information on the issue so that it can be well understood and work can start when it comes to the front of the queue. The sooner we do this, the more likely it is that we will get the information we need.
Most of the information required is asked for in the Github issue templates, so this is a great place to start.

## Check for duplicates
Pick a few keywords and search the NVDA repository on Github. We can also check if there is already a pull request in the works that may fix this issue.

## What kind of issue is it?
Can we label this as a regression, a requested change of behaviour, or a requested new feature?

### Regression
The behaviour of NVDA, or NVDA interacting with an application/software has changed to something worse.
This may mean that a feature has stopped working altogether, something isn't being announced accurately or perhaps a crash.
A regression can be caused by NVDA changing something, or an application/website changing.

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
- What version of NVDA was being used. Its good to get something like: stable, beta, rc, alpha. But much better to get the exact version of NVDA, retrieved from the NVDA menu by going to "Help" then "About". "alpha-28931,186a8d70"
- In which version of NVDA did this work as expected?
Knowing the last version where this worked in NVDA is very helpful for triage.
If an issue is a recent regression in alpha, i.e. an unreleased issue, it is fixed with a higher priority.
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

- What is the use case / user stories?
- How does it differ from the intended use case of the feature?

## Use cases / user stories
There are three things we are trying to define: Who, What, and Why.
This can often fairly naturally be stated in the following form. As a BLANK (the who), I want to be able to BLANK (the what) so that I can BLANK (the why).

Here is an example from a recent Github issue:

> As a Braille user, I notice that the cursor is a different shape when tethered to focus than it is when tethered to review. This is so that I can tell the difference between the two modes.

### Who

- Who does it affect? (for instance: Braille users, Speech users, developers working on accessibility for their websites/apps, NVDA developers)
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
As the GitHub issue grows, with more comments, questions, and discussion, it's useful to summarise the issues periodically.
This helps to condense various back and forth discussions into the final result.
This will make it easier for someone to quickly pick up the issue and understand it by reading the summary comment.
This also serves to re-iterate decisions that have been made throughout the discussion and ensure that everyone is on the same page.

## Labelling
NV Access can grant people who help triage issues the ability to label issues.
Labelling issues help indicate the priority and current state, helping NV Access and the community to decide on how to prioritise it.

### Types of issues
Issues can generally be labelled `bug` or `feature`.
We also have a label for `enhancement`, think of this as a more internal facing change. For instance, editing code comments to provide clearer / more complete information, or extending an internal framework/API to unblock other issues.

### Triaged status
An issue is triaged if it is ready to be worked on.
New features and enhancements should be [well defined](#new-features-1) before applying the `triaged` label.
Once a bug has clear steps to reproduce and is well documented, the `triaged` label can be applied.
A `triaged` issue should also have a [priority label](#priority).

Community members should avoid adding a `triaged` label to feature requests or decisions potentially involving significant or controversial changes to NVDA features or functionality, which may require community input or approval from NV Access.
The label should also be avoided for other issues that are controversial, or where the priority is unclear, such as bug fixes with an unclear solution.
For changes where a product decision from NV Access is required before applying the `triaged` label, the label `blocked/needs-product-decision` should be used.
Community members should apply the `triaged` label where an issue is a well formed bug report following the issue template, and has the following characteristics:

* Can easily be understood
* Isn't missing any important debug information
* Can clearly be reproduced
* Can clearly be prioritised
* Doesn't require a controversial solution
* They have not submitted the issue themselves

If an issue has been checked by NV Access, and needs further triage, the `needs-triage` label will be applied.
Please notify NV Access when you believe the issue is ready for the `triaged` label.
You can do this by tagging [relevant NV Access employees](../community/expertsList.md#nv-access) or emailing <info@nvaccess.org>.

A `triaged` issue that requires a complex fix may require advice from NV Access, such as a project plan, before implementation is started.

An issue with a simple solution should get labelled `good first issue`.
If it is a complex issue, technical investigation may be required.
This can be indicated with adding the label `blocked/needs-technical-investigation`.

### Priority
Bugs/regressions are given priorities based on an estimate of their severity and impact.

- `P1`:
  - `P1s` should always be fixed ASAP, in the current milestone, or the next.
  - Crash, freeze, instability or performance issue that affects most users.
  - A medium or higher severity ([CVSS 4+](https://www.first.org/cvss/v4.0/specification-document)) security issue.
  Note that security issues should not be reported publicly, and so labelling should not apply here.
  - A `P1` causes the inability to perform a popular task or majority of tasks in NVDA or a popular app.
- `P2`:
  - Crash, freeze, instability or performance issue that affects a small subset of users. It may be uncommon or difficult to reproduce.
  - A low severity ([CVSS <4](https://www.first.org/cvss/v4.0/specification-document)) security issue.
  Note that security issues should not be reported publicly, and so labelling should not apply here.
  - Popular documented feature does not work as expected
  - Popular task not supported and no work around
  - Misleading information or misleading handling from a popular task or feature
- `P3`:
  - Crash, freeze, instability or performance issue that affects one user, i.e. it cannot be reproduced by anyone else.
  - Feature does not work as expected
  - Task not supported and no work around
  - Misleading information or misleading handling
- `P4`:
  - Useful popular feature request or enhancement
  - UX inefficient (e.g. double speaking)
  - Web standard not followed causing app/web authors to require workarounds
- `P5`
  - Other feature requests affecting a small subset of users

## Legacy issues
Many older issues do not follow our issue template and have missing information.
Often they have conversation spanning years.
Summarising this information and opening a new issue filling out the issue template would be extremely useful in triaging these issues.

NV Access migrated tickets from our old issue tracker (Trac) into Github issues. These issues can be identified by having an author of `nvaccessauto`.

Some of the migrated issues have comments that indicate an attachment should be available, but it is not.
These attachments have been lost.

## NV Access staff-created tickets

The NVDA project greatly appreciates the involvement and contributions of its vibrant community, and we strongly encourage community members to actively engage with the project's issues and pull requests.

However, it's important to maintain a clear distinction between community contributions and the internal workflow of NV Access staff.
To that end, we kindly request that community members refrain from closing or consolidating tickets (issues, pull requests, etc.) that are created by NV Access staff, or are pending response from NV Access.

Community members are welcome and encouraged to interact with staff tickets in the following ways:

- Commenting on issues to provide feedback, suggestions, or additional context.
- Discussing proposed changes or feature requests.
- Submitting pull requests that address the issue or implement the requested changes, once issues have been triaged.

By refraining from closing or consolidating staff tickets, we can ensure that the NV Access team maintains control over their internal workflow and prioritisation, while still benefiting from the valuable insights and contributions of the community.

## Extra permissions for triage
GitHub allows NV Access to grant "triage" permissions to active contributors in the repository.
This grants the ability to manage issues, pull requests and discussions, such as closing/opening, labeling, and assigning.
Refer to [GitHub documentation](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization) for more information on triage permissions.

To request triage permissions, email info@nvaccess.org.
A consistent history of helpful activity in the repository is expected, for example helping debug issues, asking for missing information, providing constructive feedback on pull requests, submitting well-documented pull requests, constructively participating in discussions, mentoring new contributors or improving documentation.
Candidates will be considered on a case by case basis.

If conflict arises between how best to triage an issue, please defer to NV Access and keep the issue in an open, untriaged state i.e. with the labels "needs triage" and "blocked/needs-product-decision".
