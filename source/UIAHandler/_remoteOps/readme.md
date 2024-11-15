# UI Automation Remote Operations for NVDA

## Introduction
If you have code that makes more than a few UI Automation calls all in a row, you may want to consider rewriting the code as a Remote Operation.
This will allow Windows to execute the code all in one cross-process call, thereby significantly speeding up execution.

Following is a simple example of a remote operation.
### Example 1: Fetching the names of all ancestors of a UI Automation element
```py
import api
from UIAHandler import UIA
from UIAHandler._remoteOps.operation import Operation
from UIAHandler._remoteOps.remoteAPI import RemoteAPI

# Fetch the UI Automation element for the current focus in NVDA
focusElement = api.getFocusObject().UIAElement

# Create a new Remote Operation
op = Operation()

# Build the instructions for the remote operation.
@op.buildFunction
def code(ra: RemoteAPI):
	# Create a new remote element initializing it to the focus element.
	element = ra.newElement(focusElement)
	# Create a new array to hold the names we collect.
	names = ra.newArray()
	# Declare a while loop that will walk up the ancestors and collect the names.
	with ra.whileBlock(lambda: element.isNull().inverse()):
		# Fetch the name property of this element and store it in the array.
		name = element.getPropertyValue(UIA.UIA_NamePropertyId)
		names.append(name)
		# Fetch the element's parent and point element to it.
		parent = element.getParentElement()
		element.set(parent)
	# Now back outside the while loop.
	# Return the names array from the remote operation.
	ra.Return(names)
# Now the operation is built.

# Actually execute the remote operation, which will return the names array to NVDA.
names = op.execute()
# Print the names we got back.
print(f"{names=}")
```

## Building a remote operation
To build a remote operation, you define a function decorated by the `Operation.buildFunction` decorator.
This function must take a `RemoteAPI` object as its one and only argument.
The function will use methods on the `RemoteAPI` object to declare all its actions and logic.
Avoid using any other APIs, function calls or control flow.
```py
op = Operation()
@op.buildFunction
def code(ra: RemoteAPI):
	# Call some methods on ra...
```

### Returning values
To return a value or values from a remote operation, use the `ra.Return` method, passing one or more remote values as arguments:
```py
op = Operation()
@op.buildFunction
def code(ra: RemoteAPI):
	i = ra.newInt(10)
	div = i / 7
	mod = j % 7
	ra.Return(div, mod)
```

Note that all build functions must return at least one value.
Otherwise, `Operation.execute` will raise a `NoReturnException`.

### All operations require at least one element or text range
The primary reason for writing a remote operation is to perform actions upon one or more UI automation elements or text ranges.
And as a remote operation is executed in a remote provider, it needs to be connection bound, meaning that it needs to be associated with at least one element or text range from that provider process.
Therefore, all remote operations require at least one element (via ra.newElement) or text range (via ra.newTextRange) to be declared.
Also, all elements and text ranges in the operation must be from the same provider process.

### Declarative style and control flow
When building a remote operation, the actions are specified in a declarative style.
In other words, the code internally builds up a set of low-level instructions under the hood which will later be executed remotely.
This is most evident when specifying control flow such as a while loop:
```py
counter = ra.newInt(0)
with ra.whileBlock(lambda: counter < 5):
	counter += 1
```
From Python's point of view, the body of the declared while loop is only run once, as it is only being declared, not executed.
Similarly, for if-else blocks:
```py
condition = ra.newBool(True)
with ra.ifblock(condition):
	# Do stuff if condition is true...
with ra.elseBlock():
	# do stuff if condition is false...
```

From Python's point of view, the code inside both the if and else blocks will be run, as as it is declaring (not executing) the code here.
This will be covered more in further sections about control flow.
But the most important thing to remember here is that you should avoid using any of Python's own control flow (such as if or while, as it most likely will not do what you expected).
The remote API has all the control flow you need, such as ifBlock, elseBlock, whileBlock, tryBlock, again covered in later sections.

### Method arguments
When providing arguments to methods, you can use remote values previously declared in the operation, or you can use literal Python values.
When using literal Python values, these will be automatically remoted as special constant values for you.
For example:
```py
textRange = ra.newTextRange(UIATextRange)
textRange.move(TextUnit_Word, 1)
```

In this example, the values TextUnit_Word and 1 will be automatically remoted.

### Basic remote types
#### Equality checks
All types support equality checks:
```py
i = ra.newBool(True)
j = ra.newBool(False)
k = i == j
```

#### Setting a specific value
All types have a `set` method which allows you to set the remote variable to a specific value:
```py
i = ra.newBool(False)
# i is initialised as false.
# But now set it to true
i.set(True)
```

For most types, `set` will copy the value, i.e. setting `a` to `b` and then manipulating `b` will not change `a`.
However, for certain types such as elements, text ranges and arrays, these are held by reference and therefore manipulating the value it was set two will change the underlying object for both variables.

#### Booleans
```py
a = ra.newBool(True)
b = ra.newBool(False)
```

##### Logical operators
Booleans support logical operations:
* and: `a & b`
* or: `a | b`
* Inverse: `a.inverse()`

Unfortunately the Python language does not allow overriding `!=`, `and` and `or` to return custom types.
Thus why the above operators were chosen.

#### Ints and floats
Remote operations support declaring and manipulating int and float types.
```py
myInt = ra.newInt(5)
myFloat = ra.newFloat(7.2)
```

There is also unsigned int (`ra.newUint`) but the only place you may need to use this is for interacting with the size of a remote array (covered later).

Please note that remote operations do not allow ints and floats to be converted to one another.

##### Arithmetic
Ints, uints and floats all support the standard arithmetic operations: add, subtract, multiply, divide and modulo.
There are both binary and in-place operators for these.
```py
i = ra.newInt(5)
j = ra.newInt(6)
# addition
k = i + j
k += j
# subtraction
l = i - j
l -= j
# multiplication
m = i * j
m *= j
# division
n = i / j
n /= j
# modulo
o = i % j
o %= j
```

##### Comparison operators
Ints and floats support comparisons, returning a boolean: less, less equals, equals, greater equals and greater.
```py
i = ra.newInt(5)
j = ra.newInt(6)
k = i < j
l = i <= j
m = i == j
n = i >= j
o = i > j
```

#### Strings
```py
s = ra.newString("Hello")
```

##### Concatenation
Strings can be concatenated to create a new string:
```py
s = ra.newString("Hello ")
t = ra.newString("world")
u = s + t
```

Or they can be concatenated in-place:
```py
s = ra.newString("Hello ")
t = ra.newString("world")
s += t
```

### UIA elements
#### Declaring an element
To create a new remote element, call `ra.newElement`, giving it an existing `IUIAutomationElement` comtypes pointer as its argument:
```py
element = ra.newElement(UIAElement)
```

#### Fetching element properties
To fetch properties from an element, use `getPropertyValue`:
```py
name = element.getPropertyValue(UIA_NamePropertyId)
controlType = element.getPropertyValue(UIA_ControlTypePropertyId)
```

Any of the standard UI Automation property IDs can be used here.

#### Navigating the element tree
To navigate to other elements in the tree from this element, use the following methods on the element:
* `getParentElement`
* `getFirstchildElement`
* `getLastChildElement`
* `getPreviousSiblingElement`
* `getNextSiblingElement`

#### Pointing to another element
To make an element point to another physical UI Automation element, call its `set` method with another remote element as an argument:
```py
parent = element.getParentElement()
element.set(parent)
```

This is useful when walking the element tree in a loop.

### UI Automation text ranges
#### Declaring a text range
To create a new remote text range, call `ra.newTextRange`, giving it an existing IUIAutomationTextRange comtypes pointer as its argument:
```py
textRange = ra.newElement(UIATextRange)
```

Note that under the hood the text range is automatically cloned after it has been remoted, so that any manipulation of the remote text range (such as moving its ends) is not reflected in the original IUIAutomationTextRange you gave it.

#### Retrieving text, comparison and manipulation
The majority of methods found on `IUIAutomationTextRange` are available on remote text ranges, including:
* `getText`
* `compareEndpoints`
* `moveEndpointByUnit`
* `moveEndpointByRange`
* `expandToEnclosingUnit`
* `getEnclosingElement`
* ...

Refer to the `RemoteTextRange` class in remoteAPI.py, or official [IUIAutomationTextRange documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange) for all the call signatures.
But as an example, here is an algorithm that can count the number of words in a text range:
```py
wordCount = ra.newInt(0)
textRange = ra.newTextRange(UIATextRange)
tempRange = textRange.clone()
# Collapse the range to the start
tempRange.moveEndpointByRange(TextPatternRangeEndpoint_End, tempRange, TextPatternRangeEndpoint_Start)
with ra.whileBlock(lambda: tempRange.move(TextUnit_word, 1) == 1):
	with ra.ifblock(tempRange.compareEndpoints(textPatternRangeEndpoint_Start, textRange, TextPatternRangeEndpoint_End) >= 0):
		ra.breakLoop()
	wordCount += 1
ra.Return(wordcount)
```

#### Text range logical adapter to improve logic and readability
The verboseness of many of the compare and move text range methods can make it hard to quickly read the code and gain a good idea of what the algorithm is actually doing.
It is also quite tricky to write an algorithm that is easily reversed.
Therefore remote text ranges have a `getLogicalAdapter` method, taking a single boolean `reverse` argument which returns a special object which wraps a remote text range, and provides friendly start and end properties, which take the reversal into account.
Here is an example of how you could write an algorithm to fetch the first 20 words in the text range, either from the start or end:
```py
textRange = ra.newTextRange(UIATextRange)
words = ra.newArray()
counter = ra.newInt(0)
logicalTextRange = textRange.getLogicalAdapter(reverse=False)  # Change to True to reverse the algorithm.
logicalTempRange = logicalTextRange.clone()
# Collapse the range to the start
logicalTempRange.end = logicalTempRange.start
# Loop up to 20 times
with ra.whileBlock(lambda: counter < 20):
	# Move the end of the text range forward by one word.
	# If it fails, break out of the loop.
	with ra.ifBlock(logicalTempRange.end.moveByUnit(TextUnit_Word, 1) == 0):
		ra.breakLoop()
	# If our temp range has passed the end of the original text range, break out of the loop.
	with ra.ifBlock(logicalTempRange.end > logicalTextRange.end):
		ra.breakLoop()
	# collect the text and add it to the words array.
	text = logicalTempRange.textRange.getText(-1)
	words.append(text)
	# collapse the range to the end.
	logicalTempRange.start = logicalTempRange.end
	# Increment the counter by 1.
	counter += 1
# Return the words array.
ra.Return(words)
```

By simply changing the False to True, the algorithm is automatically reversed, as the start and end properties reverse, and the `numUnits` argument on the methods have their sign flipped.
As shown above, `start` and `end` properties can be assigned to which moves the endpoint, and they can be moved by a unit with `moveByUnit`.
They can also be compared with `<`, `<=`, `==`, `>=`, and `>`.
If you still want the comparison delta (like with `compareEndpoints`), the properties also have a `compareWith` method, which takes another endpoint and gives back a number less than 0, equal to 0 or greater than 0.

### control flow
The remoteAPI object has methods for control flow that return Python context managers, so that they can be used as `with` statements.

#### if-else
To conditionally perform actions, place them in a `with` statement using `ra.ifBlock`.
`ifBlock` takes one argument, which is a remote boolean.
If this argument is evaluated to True during execution, then the actions within the `with` statement are executed.
An optional `with` statement using `ra.elseBlock` can directly follow the `ifBlock` `with` statement, and if the condition evaluates to False, then the actions within the `elseBlock` `with` statement will be executed instead.
```py
i = ra.newInt(5)
j = ra.newInt(6)
with ra.ifblock(i < j):
	# do stuff if true...
with ra.elseBlock():
	# do stuff if false...
```

#### While loops
To keep performing some actions while a condition is True, place the actions in a `with` statement using `ra.whileBlock`.
`whileBlock` takes one argument, which is a lambda that will return a remote boolean.
```py
counter = ra.newInt(0)
with ra.whileBlock(lambda: counter < 5):
	# do some actions
	counter += 1
```

`ra.breakLoop` and `ra.continueLoop` methods can be called within the loop body to break or continue respectively.

Please note that the condition of the while loop must be placed in a lambda as it needs to be fully evaluated within the top of the loop.
If this was not done, the instructions that produced the final boolean condition would appear before the loop and never get re-run on subsequent iterations.

#### try-catch
If an action causes an error, it is possible to catch the error by placing those actions in a `with` statement using the `ra.tryBlock` method.
When using `ra.tryBlock`, a second `with` statement using `ra.catchBlock` must follow straight after.
If an error occurs within the `tryBlock` `with` statement, then execution jumps to the `catchBlock` `with` statement.
You can capture the exact error code as the value of the `with` statement.
```py
with ra.tryBlock():
	# do stuff...
with ra.catchBlock() as errorCode:
	# do stuff...
```

If it is an element or text range method that causes the error, the error code will be the COM HRESULT for that method E.g. `E_INVALIDARG`.
Other errors such as divide by 0 have their own error codes.

### Higher-level algorithms
#### Looping over a range of numbers
Although you can use a while loop and a counter to loop over a range of numbers, the library provides a helper method `ra.forEachNumInRange` which takes start, stop, and optional step arguments.
This method can be used in a `with` statement to loop over a range of numbers like so:
```py
with ra.forEachNumInRange(0, 10, 2) as num:
	# do something with num
```

#### Looping over arrays
To simplifying looping over each item in an array, the library provides `ra.forEachItemInArray` which can be used in a `with` statement like such:
```py
array = ra.newArray()
# Populate the array...

with ra.forEachItemInArray(array) as item:
	# do something with the item...
```

## Executing an operation
Once an operation is built, you will want to actually execute it on the remote provider.
To execute the operation, call `Operation.execute`.
This method takes no arguments, and returns any values previously returned with `ra.Return`.
These values are brought back to NVDA and converted to real Python types.

### Instruction limits
So as to not freeze a remote provider, Microsoft has placed a limit on how many instructions can be executed for one operation.
Currently this limit is 10,000.
This seems a lot, but once you are dealing with many while loop iterations containing a lot of actions, it is very easy to to hit this limit.
If the instruction limit is reached, then `Operation.execute` will raise `InstructionLimitExceededException`.
Assuming your algorithm was written appropriately, you could then re-execute it, and the remote provider will have had a chance to run its own main loop or do what ever it needs to do between operations.

To aide in writing algorithms that can handle this instruction limit and continue to execute where it left off, there are several features of this Remote Operations library that can be used.

#### Automatic retry
`Operation.execute` takes a `maxTries` keyword argument which is set to 1 by default, meaning that the operation will only be executed once, and if the instruction  limit is hit, then `InstructionLimitExceededException` is raised.
However, if `maxTries` is greater than 1, `Operation.execute` will automatically retry  more times until the operation executes without hitting the limit, or when `maxTries` is reached.

This in itself however is not too useful unless some other changes are made to the algorithm itself, so that it is suitable for running multiple times by remembering where it left off.

#### Static values
Most `ra.newXXX` methods take a `static` keyword argument which is set to `False` by default.
However, if set to `True`, subsequent executions of the operation will initialize the value to what it was when the last execution finished.
```py
counter = ra.newInt(0, static=True)
with ra.whileBlock(lambda: counter < 20000):
	counter += 1
```

The above example will most definitely hit the instruction limit, however, because static was set to true, on the next execution counter will be re-initialized with the last value it was before the limit was hit.

Please note though that the execution will still start again from the first instruction, so the algorithm still needs to be written to take this into account.

It could be possible in future to implement the library to start from the exact instruction where the limit was hit, but this would mean marshalling each and every declared remote variable out and then back in, which could be costly.
This is why it currently only does it for ones marked as `static`.

Also, currently it is impossible to mark arrays as `static`, as arrays cannot be initialized with a value in the low-level remote operations framework.
Again, in future the library could be extended to support this, but it would involve having to marshal out all items, and marshal them back in, appending them to the array one at a time, which would also be costly.

#### Building iterable functions
A common use of remote operations is to walk a text range or element tree, and collect data which would be returned in an array.
However, as arrays can not be marked as `static`, this would involve a lot of extra code to handle execution continuation after the instruction limit is reached.
Therefore the library supports a `Operation.buildIterableFunction` decorator, which can be used in place of `Operator.buildFunction`.
Within a function that uses this decorator, rather than using ra.Return to return value and halt, you can use `ra.Yield` which will yield a value and continue to execute (until the instruction limit is reached of course).
To actually execute an iterable function though, instead of using `Operation.execute`, you use `Operation.iterExecute` as the generator to a `for` loop, which will iterate over the yielded values.
```py
op = Operation()

@op.buildIterfunction
def code(ra: RemoteAPI):
	counter = ra.newInt(0, static=True)
	with ra.whileBlock(lambda: counter < 20000):
		with ra.ifBlock((counter % 1000) == 0):
			ra.Yield(counter)
		counter += 1

for item in op.iterExecute(maxTries=10):
	print(f"{item=}")
```

The above example will print 0, 1000, 2000, 3000...

Although the `for` loop will see each yielded value separately, they will only physically yield either when the instruction limit is reached, and or when the execution finally reaches the end, which still means that as many actions as possible are executed in one cross-process call.

## Debugging
It can be tricky to debug a remote operation as it executes in the remote provider.
Therefore the library contains several features which can help.

### Dumping instructions
The library can dump all the instructions to NVDA's log each time an operation is built, by setting the Operation's `enableCompiletimeLogging` keyword argument to True.
Even if left as False, instructions will still be automatically dumped to NVDA's log if there is an uncaught error while executing, or the instruction limit is reached and it has run out of tries.
Following is code for a simple remote operation, followed by a dump of its instructions.
```py
counter = ra.newInt(0, static=True)
with ra.whileBlock(lambda: counter < 20000):
	with ra.ifBlock((counter % 1000) == 0):
		ra.Yield(counter)
	counter += 1
```

And now the instruction dump:
```
--- Begin ---
static:
0: NewInt(result=RemoteInt at OperandId 2, value=c_long(0))
const:
1: NewInt(result=const RemoteInt at OperandId 4, value=c_long(20000))
2: NewInt(result=const RemoteInt at OperandId 6, value=c_long(1000))
3: NewInt(result=const RemoteInt at OperandId 10, value=c_long(0))
4: NewInt(result=const RemoteInt at OperandId 11, value=c_long(1))
main:
5: NewArray(result=RemoteArray at OperandId 1)
6: NewLoopBlock(breakBranch=RelativeOffset 12, continueBranch=RelativeOffset 1)
# Entering RemoteNumber.__lt__(20000, )
# Using cached const RemoteInt at OperandId 4 for constant value 20000
7: Compare(result=RemoteBool at OperandId 3, left=RemoteInt at OperandId 2, right=const RemoteInt at OperandId 4, comparisonType=<ComparisonType.LessThan: 3>)
# Exiting RemoteNumber.__lt__
8: ForkIfFalse(condition=RemoteBool at OperandId 3, branch=RelativeOffset 9)
# While block body
# Entering RemoteNumber.__mod__(1000, )
# Entering RemoteNumber.__truediv__(1000, )
# Using cached const RemoteInt at OperandId 6 for constant value 1000
9: BinaryDivide(result=RemoteInt at OperandId 5, left=RemoteInt at OperandId 2, right=const RemoteInt at OperandId 6)
# Exiting RemoteNumber.__truediv__
# Entering RemoteNumber.__mul__(1000, )
# Using cached const RemoteInt at OperandId 6 for constant value 1000
10: BinaryMultiply(result=RemoteInt at OperandId 7, left=RemoteInt at OperandId 5, right=const RemoteInt at OperandId 6)
# Exiting RemoteNumber.__mul__
# Entering RemoteNumber.__sub__(RemoteInt at OperandId 7, )
11: BinarySubtract(result=RemoteInt at OperandId 8, left=RemoteInt at OperandId 2, right=RemoteInt at OperandId 7)
# Exiting RemoteNumber.__sub__
# Exiting RemoteNumber.__mod__
# Entering RemoteBaseObject.__eq__(0, )
# Using cached const RemoteInt at OperandId 10 for constant value 0
12: Compare(result=RemoteBool at OperandId 9, left=RemoteInt at OperandId 8, right=const RemoteInt at OperandId 10, comparisonType=<ComparisonType.Equal: 0>)
# Exiting RemoteBaseObject.__eq__
13: ForkIfFalse(condition=RemoteBool at OperandId 9, branch=RelativeOffset 2)
# If block body
# Begin yield (RemoteInt at OperandId 2,)
# Yielding RemoteInt at OperandId 2
# Entering RemoteArray.append(RemoteInt at OperandId 2, )
14: RemoteArrayAppend(target=RemoteArray at OperandId 1, value=RemoteInt at OperandId 2)
# Exiting RemoteArray.append
# End of if block body
# Entering RemoteNumber.__iadd__(1, )
# Using cached const RemoteInt at OperandId 11 for constant value 1
15: Add(target=RemoteInt at OperandId 2, value=const RemoteInt at OperandId 11)
# Exiting RemoteNumber.__iadd__
# End of while block body
16: ContinueLoop()
17: EndLoopBlock()
18: Halt()
--- End --
```

Looking at the dump we can see the library stores instructions in three specific sections:
* `static`: for initializing static instructions. this section is replaced before each execution.
* `const`: This section holds values which have been automatically remoted, and are used through out the rest of the instructions.
* `main`: the instructions implementing the main logic of the operation.

We can also see that a part from each numbered instruction and its parameters, there are also comments which help to understand the higher-level logic, such as when entering and exiting particular methods.

We can see that yielding values is actually implemented by the library internally as an array.

and finally, we can see that the modulo (%) operator is actually emulated by the equation: `a - (a / b) * b`, as the low-level remote operations framework does not actually support modulo.

### Adding compiletime comments
It is possible to add comments to the instruction dump when building an operation by using `ra.addCompiletimeComment`.
It takes a single argument which is a literal string value.

### Runtime remote logging
Setting an Operation's `enableRuntimeLogging` keyword argument to True enables remote logging at execution time.
`ra.logRuntimeMessage` can be called to log a message at runtime.
It takes one or more literal strings and or remote values, and concatinates them together remotely.
For remote values that are not strings, `logRuntimeMessage` uses the remote value's `stringify` method to produce a string representation of the value.

After the operation is executed, the remote log is marshalled back and dumped to NvDA's log, thereby giving the ability to trace what is happening during the execution.
Though be aware that as remote logging itself involves creating and manipulating remote values, then the number of instructions can change quite significantly with remote logging enabled.

### Local mode
When unit testing this library, or in a scenario where remote operations is unavailable but you want to use the exact same algorithm but locally, you can set the Operation's `localMode` keyword argument to True.
This causes all instructions to be executed locally, rather than in a remote provider.
This will of course be significantly slower, as every instruction that manipulates an element or text range will be itself one cross-process call.
However, it is a useful means of testing and debugging, and much care has been taken to ensure that the results and side-effects are identical to executing it remotely.

This differs some what from Microsoft's original remote operations library which implemented its local mode so that instructions were executed locally at build time, and executing did nothing.
This library produces instructions just as it would remotely, but it is these low-level instructions that are executed locally at execution time, following all the same rules and limitations that executing remotely would.
Thus, it is more suited to debugging / testing, rather than as a means of executing where remote operations is unavailable, as code could be written much more efficiently using comtypes IUIAutomation interfaces directly.
