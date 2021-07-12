
## Lint overview
Our linting process with Flake8 consists of two main steps:
- Generating a diff
- Running Flake8 on the diff

## Common problems
There are several common situations for which the Flake8 errors don't clearly indicate an error free solution.

### Continuation lines

According to the
[Pep8 indentation guide](https://www.python.org/dev/peps/pep-0008/#indentation),
continuation lines (Python's implicit line joining inside parentheses) are expected
to follow one of two main styles:

- Vertical alignment
  - The first parameter is on the same line as the opening parenthesis
  - For each subsequent line, the first character should be aligned with the
    first character of the first parameter.
- Hanging indent
  - There is no parameter on the same line as the opening parenthesis.
  - The first parameter is indented by a standard amount on the following line.
  - All subsequent parameters have the same indent.

What this means for us:
- Vertical alignment
  - Requires spaces to meet the length of arbitrary function/variable names
  - Requires counting characters to determine the number of spaces before arguments
  - Alignment must be changed if the function/variable name changes.
- Hanging indent
  - Fixed indentation
  - Takes up more vertical space

Previously Flake8 checkers didn't know which style we intend, they allow for both.
We now configure Flake8-tabs with the `continuation-style=hanging` option to enforce hanging indent
and it will complain about code which seems to be using vertical alignment style (warning ET113).

#### Preferred formatting for continuation lines

- Use hanging indent style.
  - Line break after the opening parenthesis, putting the first parameter on a new line.
- For function definitions, double indent the params to avoid ET121

```python
# method with many parameters
# use "hanging indent style" - start params on new line to avoid ET113 and ET128
def foo(
		arg1,  # double indent to avoid ET121
		arg2
):  # put the closing paren on a new line, reduce the diff when changing parameters.
	# long expression
	# use "hanging indent style" - start params on new line to avoid ET113 and ET128
	if(
		arg1 is not None  # not a function definition, no double indent required
		and arg2 is None
	):  # put the closing paren on a new line, reduce the diff when changing conditions
		return None

	# use "hanging indent style" - start params on new line to avoid EET113 and T128
	values = [
		"value1", # not a function definition, no double indent required
		"value2",
	]  # put the closing bracket on a new line, reduce the diff when adding items.
	return values

```

Note: An inline comment on an opening parenthesis/bracket/brace does not cause an error
EG:
```python
def foo(  # a comment here is fine
		arg1
):
	items = [  # a comment here is fine
		"item1",
		"item2",
	]
	print(items)
```

#### ET113 (flake8-tabs)

Error messages:
 - *Option continuation-style=hanging does not allow use of alignment as indentation*

A parameter is on the same line as the opening paran/bracket/brace.
Move this parameter to a new line to resolve this error.
When triggered, it is likely that ET128 will be triggered for subsequent lines with parameters.

#### ET128 (flake8-tabs)

Error messages:
- *unexpected number of tabs at start of definition line*
- *unexpected number of tabs and spaces at start of expression line*s

Its likely that this is triggered because the linter is expecting "vertical alignment"
style for the set of continuation lines, rather than "hanging indent" style.
To confirm look for ET113 triggered on the same line.
To change this, ensure that there is a newline after the opening paren/bracket/brace.

An example cause:
```python
def foo(arg1, # Triggers ET113
	arg2,  # Triggers ET128: arg2 not vertically aligned with start of first parameter.
):
	return None
```

#### ET121 (flake8-tabs)

Error messages:
- *unexpected number of tabs at start of definition line (expected 2, got 1)*

Example cause:
```python
def foo(
	arg1,  # one level of indentation, matches the function body
	arg2,
):
	return None
```

In function definitions we require double indentation of parameters to differentiate from
the body of the function.

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
