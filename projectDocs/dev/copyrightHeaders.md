In NVDA files, which are licensed under the terms of a modified GNU General Public License, use the following copyright header:

```py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) <CREATED YEAR>-<LAST UPDATED YEAR> NV Access Limited, <YOUR NAME>
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
```

Replacing:
- `<YOUR NAME>` with your name.
- `<CREATED YEAR>` the year the file was created
- `<LAST UPDATED YEAR>` when the file was last updated.
For new files this can be missing.
e.g. a file created in 2025 might have `# Copyright (C) 2025`

Some files are covered by the GNU LGPL, for example the controller client and its examples.
This allows someone to use them (or parts of them) as-is.
In this case use the following header:

```py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) <CREATED YEAR>-<LAST UPDATED YEAR> NV Access Limited, <YOUR NAME>
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1 or later.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html
```

In some files an older style of referring to the contributors is used.
The contributors is not a list of names and may just say something like:
`Copyright (C) 2006-2024 NVDA Contributors`.
We suggest referring to the git logs to identify specific authors.
