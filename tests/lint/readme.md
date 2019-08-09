
## Lint overview
Our linting process with Flake8 consists of two main steps:
- Generating a diff
- Running Flake8 on the diff

## Scons lint
Executed with SCons.
```
scons lint base=origin/master
```
- Remember to set the the `base` branch (the target you would use for a PR).
- This SCons target will generate a diff file (`tests\lint\current.diff`) and run Flake8 on it.
- The output from Flake8 will be displayed with other SCons output, and will also be written to file (`tests\lint\current.lint`)
- This uses the NVDA flake8 configuration file (`tests\lint\flake8.ini`)

## Lint integration

For faster lint results, or greater integration with your tools you may want to execute this on the command line or via your IDE.

### Generate a diff

You can use the `tests/lint/genDiff.py` script to generate the diff, or create the diff on the commandline:
- Get the merge base
  - `git merge-base <baseBranch> HEAD`
  - `merge-base` is used to limit changes to only those that are new on HEAD.
- Create a diff with your working tree
  - `git diff -U0 <mergeBaseSha>`
  - `-U0`: Only include changed lines (no context) in the diff.
    - Otherwise developers may end up getting warnings for code adjacent to code they touched.
    - This could result in very large change sets in order to get a clean build.
  - Note: We don't use triple dot syntax (`...`) because it will not report changes in your working tree.

### Pipe to Flake8

Flake8 can accept a unified diff, however only via stdin.

In cmd:
```
type current.diff | py -3 -m flake8 --diff --config="tests/lint/flake8.ini"
```

In bash:
```
cat current.diff | py -3 -m flake8 --diff --config="tests/lint/flake8.ini"
```
