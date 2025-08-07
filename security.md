# Reporting Security Issues

Please do not report security vulnerabilities through public GitHub issues.
You can report security issues directly through [a GitHub Security Advisory](https://github.com/nvaccess/nvda/security/advisories/new).
Please use [our advisory template](./projectDocs/issues/securityAdvisoryTemplate.md).
Alternatively, please report security issues via an email to [info@nvaccess.org](mailto:info@nvaccess.org).

You should receive an acknowledgement in the advisory or via email response within 3 business days.
If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the requested information listed below (as much as you can provide) to help us better understand the nature and scope of the possible issue.
This information will help us triage your report more quickly.

* Type of issue (e.g. denial of service, privilege escalation, etc.)
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including what an attacker can achieve by exploiting the issue
* Potential workarounds to mitigate the issue
* Indicators of compromise caused by the issue
* If there is a known solution or approach to fixing this issue

Examples of handled security issues in NVDA can be found in the [NVDA GitHub Security Advisories page](https://github.com/nvaccess/nvda/security/advisories).

## Security Advisory Group

NV Access is committed to maintaining the highest standards of security in NVDA. In line with this commitment, we have established a Security Advisory Group. This group plays a pivotal role in enhancing the security of NVDA.

Objectives and Functioning:

* The group is composed of dedicated users and security enthusiasts who volunteer their expertise.
* It focuses on identifying, analysing and resolving security issues in a collaborative manner.
* The group's contributions are instrumental in maintaining and elevating our security standards.
* Their insights and recommendations are directly incorporated into our development process, leading to more secure and reliable software.

We welcome participation from our user community. If you have a keen interest in security and wish to contribute, please [contact us](mailto:info@nvaccess.org).

## Severity Levels

* P1 (Critical): Vulnerabilities with a medium or higher severity (CVSS 4+) causing a significant risk to the security and privacy of NVDA users.
* P2 (High): Vulnerabilities with a low severity (CVSS <4) that present a potential security risk.

## Response Timelines (SLAs)

* Acknowledgement and Triage: Within 3 business days of receipt.
* P1 (Critical):
  * Planning and Mitigation: Detailed assessment of the issue and assessment of possible technical solutions within 1 week of triage.
  Development of a resolution will then begin immediately.
  * Patch Release: Target patch release of a workaround within 2 weeks of completing assessment.
  A thorough and complete resolution may need to be scheduled into the next minor release.

* P2 (High):
  * Planning and Mitigation: Assessment within 2 weeks of triage.
  * Patch Release: Target patch release in the next scheduled minor release.
* Security Advisory: A security advisory will be published concurrently with the release of the patch.
The advisory will provide details of the vulnerability and rectification steps.
As details of the vulnerability will be available in the code repository, immediate disclosure aligns with responsible disclosure principles.

## Resource Allocation

* P1 (Critical): Immediate attention from core developers and/or the Security Advisory Group. Other development tasks may be temporarily deprioritised.
* P2 (High): Dedicated resources will be allocated, with prioritisation based on severity and available development bandwidth.
