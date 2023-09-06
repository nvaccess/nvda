# Garbage collection errors
NVDA's `garbageHandler.py` monitors Python's cyclic garbage collector and reports
on objects that are unreachable.
Cyclic references are typically a symptom of bad design, and can cause major problems for certain objects.
For instance, cyclic references involving COM objects may cause a deadlock if the garbage collector happens to break the cycle and release the COM object in the wrong thread.

## How to know about a cyclic reference?
The log may contain errors like the following.
```
WARNING - garbageHandler.notifyObjectDeletion (10:45:23.171) - MainThread (21820):
Garbage collector has found one or more unreachable objects. See further warnings for specific objects.
...
WARNING - garbageHandler.notifyObjectDeletion (10:45:23.171) - MainThread (21820):
Deleting unreachable object <eventHandler._EventExecuter object at 0x1AC15350>
ERROR - garbageHandler._collectionCallback (10:45:23.172) - MainThread (21820):
Found at least 1 unreachable objects in run
```

## How to debug a cyclic reference?

Once you can reliably reproduce the log error, you can tell the garbage collector to save all unreachable objects.
After an unreachable object is detected the references to the unreachable object can be inspected via the python console.
Inspecting this should give you a fair idea of where the issue is occurring.

1. Open the NVDA Python console `NVDA+control+z`
1. Enable saving all objects:
   ``` python
   import gc
   gc.set_debug(gc.DEBUG_SAVEALL)
   ```
1. Reproduce the unreachable object error.
1. If garbage collection errors have not yet been logged, force a collect by calling:
   ``` python
   gc.collect()
   ```

1. All unreachable objects will now be stored in `gc.garbage`.
   It may be a very large list.
   Some tricks for narrowing this list down:
   - From the log, you can get the memory address (`id`) of the object.
     Then use:
     ``` python
     memoryAddress = 0xabcd123
     obj = None
     for o in gc.garbage:
     	if memoryAddress == id(o)
     		obj = o
     ```
   - Listing the types collected, look for the type(s) matching the log message:
     ``` python
     for index, o in enumerate(gc.garbage):
     	print(index, type(o))
     ```
1. Once you have a reference (`obj`) to the unreachable object, see what other objects refer to an object you can call.
   You can do this by using `gc.get_referrers`.
   The python console has a reference to `obj`, there may be a lot of output.
   You can reduce this by looking at the types and following the most relevant.
   ``` python
   for index, o in enumerate(gc.get_referrers(obj)):
   	print(index, type(o))
   ```
1. Continue following the references to build a picture of the cycle.

## Typical problems
Some examples of common issues:
- Exceptions caught and assigned to a local variable.
