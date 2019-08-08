
## Lint overview
Our linting process with Flake8 consists of two main steps:
- Generating a diff
- Running Flake8 on the diff

## Common problems
There seem to be several common situations for which the Flake8 errors don't clearly indicate an error free solution.

### Line-breaking functions and statements

Lint errors you may encounter:
- ET128 (flake8-tabs) *unexpected number of tabs and spaces at start of expression line*
  - In particular, if this error message "expects x spaces", its likely that it is expecting a
  code alignment style, rather than hanging indent style.
  To change this expectation, first ensure that there is a newline after the opening
  paren/bracket/brace.
- ET121 (flake8-tabs) *unexpected number of tabs at start of definition line*

#### Preferred formatting

- Break after the parenthesis, putting the first parameter on a new line.
- Double indent the params to avoid ET121

```python
# method with many parameters
# start params on new line to avoid aligning with parenthesis.
def foo(
		arg1,  # double indent to avoid ET121
		arg2
):
	# long expression
	# start params on new line to avoid aligning with parenthesis.
	if(
		arg1 is not None
		and arg2 is None
	):
		return None

	values = [
		"value1",
		"value2",
	]
	return values

```

Note: A comment an inline comment causes an erroneous error from flake8-tabs:
See https://gitlab.com/ntninja/flake8-tabs/issues/1
EG:
```python
def foo(  # a comment here causes error ET128
		arg1
):
	pass
```

#### Explanation

An example of code that will trigger this lint error:
```python
def foo(arg1,
	arg2,
):
	return None
```

The [Pep8 indentation guide](https://www.python.org/dev/peps/pep-0008/#indentation) seems to favour aligning the start of each parameter name to be to the right of the opening parenthesis (or bracket). 
However, we don't use spaces which often makes this alignment impossible.
Instead we choose the alternative style, hanging indent for parameters, and matching indentation for the closing bracket / parenthesis / brace.
In function definitions we require double indentation of parameters to differentiate from the body of the function.

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
