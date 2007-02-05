#comtypesClient.py
#$Rev$
#$Date$
#Origionally from comtypes
#http://www.sourceforge.net/projects/comtypes/
#Patched to generate com interfaces in the comInterfaces directory even if it is an executable.

'''High level client level COM support module.
'''

################################################################
#
# TODO: 
#
# - rename wrap
#
# - beautify the code generator output (import statements at the top)
#
# - add a GetTypelibWrapper(obj) function?
#
# - refactor this code into several modules now that this is a package
#
################################################################

# comtypesClient

import sys, os, new, imp
import weakref
import ctypes
import comtypes
from comtypes.hresult import *
import comtypes.automation
import comtypes.connectionpoints
import comtypes.typeinfo

import logging
logger = logging.getLogger(__name__)

__all__ = ["CreateObject", "GetActiveObject", "CoGetObject",
           "GetEvents", "ReleaseEvents", "GetModule"]

__verbose__ = __debug__

################################################################
# Determine the directory where generated modules live.
gen_dir = ".\\comInterfaces"
#comInterfaces=__import__('comInterfaces',globals(),locals(),[])


### for testing
##gen_dir = None
    
################################################################

def _my_import(fullname):
    # helper function to import dotted modules
    return __import__(fullname, globals(), locals(), ['DUMMY'])

def _my_findmodule(fullname):
    # Use imp.find_module to find out whether a module exists or not.
    # Raise ImportError if it doesn't exist.
    #
    # Hm, couldn'w we directly look for the .py or .pyc/.pyo files?
    name, rest = fullname.split(".", 1)
    file_, pathname, desc = imp.find_module(name)
    if file_:
        file_.close()
    for name in rest.split("."):
        file_, pathname, desc = imp.find_module(name, [pathname])
        if file_:
            file_.close()

def _name_module(tlib):
    # Determine the name of a typelib wrapper module.
    libattr = tlib.GetLibAttr()
    modname = "_%s_%s_%s_%s" % \
              (str(libattr.guid)[1:-1].replace("-", "_"),
               libattr.lcid,
               libattr.wMajorVerNum,
               libattr.wMinorVerNum)
    return "comInterfaces." + modname

def GetModule(tlib):
    """Create a module wrapping a COM typelibrary on demand.

    'tlib' must be an ITypeLib COM pointer instance, the pathname of a
    type library, or a tuple/list specifying the arguments to a
    comtypes.typeinfo.LoadRegTypeLib call:

      (libid, wMajorVerNum, wMinorVerNum, lcid=0)

    Or it can be an object with _reg_libid_ and _reg_version_
    attributes.
    
    This function determines the module name from the typelib
    attributes, then tries to import it.  If that fails because the
    module doesn't exist, the module is generated in the comInterfaces
    package.

    It is possible to delete the whole comtypes\gen directory to
    remove all generated modules, the directory and the __init__.py
    file in it will be recreated when needed.

    If comInterfaces __path__ is not a directory (in a frozen
    executable it lives in a zip archive), generated modules are only
    created in memory without writing them to the file system.

    Example:

        GetModule("shdocvw.dll")

    would create modules named
    
       comInterfaces._EAB22AC0_30C1_11CF_A7EB_0000C05BAE0B_0_1_1
       comInterfaces.SHDocVw

    containing the Python wrapper code for the type library used by
    Internet Explorer.  The former module contains all the code, the
    latter is a short stub loading the former.
    """
    if isinstance(tlib, basestring):
        # we accept filenames as well
        tlib = comtypes.typeinfo.LoadTypeLibEx(tlib)
    elif isinstance(tlib, (tuple, list)):
        tlib = comtypes.typeinfo.LoadRegTypeLib(comtypes.GUID(tlib[0]), *tlib[1:])
    elif hasattr(tlib, "_reg_libid_"):
        tlib = comtypes.typeinfo.LoadRegTypeLib(comtypes.GUID(tlib._reg_libid_),
                                                *tlib._reg_version_)
    # determine the Python module name
    fullname = _name_module(tlib)
    # create and import the module
    mod = _CreateWrapper(tlib, fullname)
    modulename = tlib.GetDocumentation(-1)[0]
    if modulename is None:
        return mod
    modulename = modulename.encode("mbcs")

    # create and import the friendly-named module
    try:
        return _my_import("comInterfaces." + modulename)
    except:
        # this way, the module is always regenerated if importing it
        # fails.  It would probably be better to check for the
        # existance of the module first with imp.find_module (but
        # beware of dotted names), and only regenerate if if not
        # found.  Other errors while importing should probably make
        # this function fail.
        if __verbose__:
            print "# Generating comInterfaces.%s" % modulename
        modname = fullname.split(".")[-1]
        code = "from comInterfaces import %s\nglobals().update(%s.__dict__)\n" % (modname, modname)
        code += "__name__ = 'comInterfaces.%s'" % modulename
        if gen_dir is None:
            mod = new.module("comInterfaces." + modulename)
            exec code in mod.__dict__
            sys.modules["comInterfaces." + modulename] = mod
            setattr(comInterfaces, modulename, mod)
            return mod
        # create in file system, and import it
        fileName=os.path.join(gen_dir, modulename + ".py")
        ofi = open(fileName,"w")
        ofi.write(code)
        ofi.close()
        return _my_import("comInterfaces." + modulename)
        
def _CreateWrapper(tlib, fullname):
    # helper which creates and imports the real typelib wrapper module.
    try:
        return _my_import(fullname)
    except Exception:
        # we could not import the module.  What was the reason?
        try:
            _my_findmodule(fullname)
        except ImportError:
            # module does not exist, generate it
            pass
        else:
            # any other error: fail
            raise
        # We generate the module since it doesn't exist
        from comtypes.tools.tlbparser import generate_module
        modname = fullname.split(".")[-1]
        if gen_dir is None:
            import cStringIO
            ofi = cStringIO.StringIO()
        else:
            ofi = open(os.path.join(gen_dir, modname + ".py"), "w")
        # use warnings.warn, maybe?
        if __verbose__:
            print "# Generating comInterfaces.%s" % modname
        generate_module(tlib, ofi, GetModule, _name_module)

        if gen_dir is None:
            code = ofi.getvalue()
            mod = new.module(fullname)
            exec code in mod.__dict__
            sys.modules[fullname] = mod
            setattr(comInterfaces, modname, mod)
        else:
            ofi.close()
            mod = _my_import(fullname)
            reload(mod)
        return mod

def wrap_outparam(punk):
    logger.info("wrap_outparam(%s)", punk)
    if punk.__com_interface__ == comtypes.automation.IDispatch:
        return wrap(punk)
    return punk

# XXX rename this!
def wrap(punk):
    """Try to QueryInterface a COM pointer to the 'most useful'
    interface.
    
    Get type information for the provided object, either via
    IDispatch.GetTypeInfo(), or via IProvideClassInfo.GetClassInfo().
    Generate a wrapper module for the typelib, and QI for the
    interface found.
    """
    if not punk: # NULL COM pointer
        return punk # or should we return None?
    # find the typelib and the interface name
    logger.info("wrap(%s)", punk)
    try:
        pci = punk.QueryInterface(comtypes.typeinfo.IProvideClassInfo)
        logger.info("Does implement IProvideClassInfo")
        tinfo = pci.GetClassInfo() # TypeInfo for the CoClass
        # find the interface marked as default
        ta = tinfo.GetTypeAttr()
        for index in range(ta.cImplTypes):
            if tinfo.GetImplTypeFlags(index) == 1:
                break
        else:
            if ta.cImplTypes != 1:
                # Hm, should we use dynamic now?
                raise TypeError, "No default interface found"
            # Only one interface implemented, use that (even if
            # not marked as default).
            index = 0
        href = tinfo.GetRefTypeOfImplType(index)
        tinfo = tinfo.GetRefTypeInfo(href)
    except comtypes.COMError:
        logger.info("Does NOT implement IProvideClassInfo")
        try:
            pdisp = punk.QueryInterface(comtypes.automation.IDispatch)
        except comtypes.COMError:
            logger.info("No Dispatch interface: %s", punk)
            return punk
        try:
            tinfo = pdisp.GetTypeInfo(0)
        except comtypes.COMError:
            pdisp = Dispatch(pdisp)
            logger.info("IDispatch.GetTypeInfo(0) failed: %s" % pdisp)
            return pdisp
    try:
        punk.QueryInterface(comtypes.IUnknown, tinfo.GetTypeAttr().guid)
    except comtypes.COMError:
        logger.info("Does not seem to implement default interface from typeinfo, using dynamic")
        return Dispatch(punk)

    itf_name = tinfo.GetDocumentation(-1)[0] # interface name
    tlib = tinfo.GetContainingTypeLib()[0] # typelib

    # import the wrapper, generating it on demand
    mod = GetModule(tlib)
    # Python interface class
    interface = getattr(mod, itf_name)
    logger.info("Implements default interface from typeinfo %s", interface)
    # QI for this interface
    # XXX
    # What to do if this fails?
    # In the following example the engine.Eval() call returns
    # such an object.
    #
    # engine = CreateObject("MsScriptControl.ScriptControl")
    # engine.Language = "JScript"
    # engine.Eval("[1, 2, 3]")
    #
    # Could the above code, as an optimization, check that QI works,
    # *before* generating the wraper module?
    result = punk.QueryInterface(interface)
    logger.info("Final result is %s", result)
    return result

# Should we do this for POINTER(IUnknown) also?
ctypes.POINTER(comtypes.automation.IDispatch).__ctypes_from_outparam__ = wrap_outparam

# XXX move into comtypes
def _getmemid(idlflags):
    # get the dispid from the idlflags sequence
    return [memid for memid in idlflags if isinstance(memid, int)][0]

# XXX move into comtypes?
def _get_dispmap(interface):
    # return a dictionary mapping dispid numbers to method names
    assert issubclass(interface, comtypes.automation.IDispatch)

    dispmap = {}
    if "dual" in interface._idlflags_:
        # It would be nice if that would work:
##        for info in interface._methods_:
##            mth = getattr(interface, info.name)
##            memid = mth.im_func.memid
    
        # See also MSDN docs for the 'defaultvtable' idl flag, or
        # IMPLTYPEFLAG_DEFAULTVTABLE.  This is not a flag of the
        # interface, but of the coclass!
        #
        # Use the _methods_ list
        assert not hasattr(interface, "_disp_methods_")
        for restype, name, argtypes, paramflags, idlflags, helpstring in interface._methods_:
            memid = _getmemid(idlflags)
            dispmap[memid] = name
    else:
        # Use _disp_methods_
        # tag, name, idlflags, restype(?), argtypes(?)
        for tag, name, idlflags, restype, argtypes in interface._disp_methods_:
            memid = _getmemid(idlflags)
            dispmap[memid] = name
    return dispmap

def GetEvents(source, sink, interface=None):
    """Receive COM events from 'source'.  Events will call methods on
    the 'sink' object.  'interface' is the source interface to use.
    """
    # When called from CreateObject, the sourceinterface has already
    # been determined by the coclass.  Otherwise, the only thing that
    # makes sense is to use IProvideClassInfo2 to get the default
    # source interface.

    if interface is None:
        # QI for IConnectionPointContainer and thne
        # EnumConnectionPoints would also work, but doesn't make
        # sense.  The connection interfaces are enumerated in
        # arbitrary order, so we cannot decide on out own which one to
        # use.
##        cpc = source.QueryInterface(IConnectionPointContainer)
##        for cp in cpc.EnumConnectionPoints():
##            print comtypes.com_interface_registry[str(cp.GetConnectionInterface())]
        try:
            pci = source.QueryInterface(comtypes.typeinfo.IProvideClassInfo2)
        except comtypes.COMError:
            raise TypeError("cannot determine source interface")
        # another try: block needed?
        guid = pci.GetGUID(1)
        interface = comtypes.com_interface_registry[str(guid)]
        logger.debug("%s using sinkinterface %s", source, interface)

    if issubclass(interface, comtypes.automation.IDispatch):
        dispmap = _get_dispmap(interface)

        for memid, name in dispmap.iteritems():
            # find methods to call, if not found ignore event
            mth = getattr(sink, "%s_%s" % (interface.__name__, name), None)
            if mth is None:
                mth = getattr(sink, name, lambda *args: 0)
            dispmap[memid] = mth

        class DispEventReceiver(comtypes.COMObject):
            _com_interfaces_ = [interface]

            def IDispatch_Invoke(self, this, memid, riid, lcid, wFlags, pDispParams,
                                 pVarResult, pExcepInfo, puArgErr):
                dp = pDispParams[0]
                # DISPPARAMS contains the arguments in reverse order
                args = [dp.rgvarg[i].value for i in range(dp.cArgs)]
                self.dispmap[memid](None, *args[::-1])
                return 0

            def GetTypeInfoCount(self, this, presult):
                if not presult:
                    return E_POINTER
                presult[0] = 0
                return S_OK

            def GetTypeInfo(self, this, itinfo, lcid, pptinfo):
                return E_NOTIMPL

            def GetIDsOfNames(self, this, riid, rgszNames, cNames, lcid, rgDispId):
                return E_NOTIMPL

        rcv = DispEventReceiver()
        rcv.dispmap = dispmap
    else:
        class EventReceiver(comtypes.COMObject):
            _com_interfaces_ = [interface]

        for itf in interface.mro()[:-2]: # skip object and IUnknown
            for info in itf._methods_:
                restype, name, argtypes, paramflags, idlflags, docstring = info

                mth = getattr(sink, name, lambda self, this, *args: None)
                setattr(EventReceiver, name, mth)
        rcv = EventReceiver()

    # XXX All of these (QI, FindConnectionPoint, Advise) can also fail
    # (for buggy objects?), and we should raise an appropriate error
    # then.

    try:
        cpc = source.QueryInterface(comtypes.connectionpoints.IConnectionPointContainer)
        cp = cpc.FindConnectionPoint(ctypes.byref(interface._iid_))
        logger.debug("Start advise %s", interface)
        cookie = cp.Advise(rcv)
    except:
        logger.error("Could not connect to object:", exc_info=True)
        raise

    def release(ref):
        # XXX Do not reference 'source' here!
        logger.debug("End advise %s", interface)
        try:
            cp.Unadvise(cookie)
        except (comtypes.COMError, WindowsError):
            # are we sure we want to ignore errors here?
            pass
        del _active_events[(ref, sink, interface)]

    # clean up when the source goes away.
    guard = weakref.ref(source, release)
    _active_events[(guard, sink, interface)] = release

_active_events = {}

def ReleaseEvents(source, sink=None, interface=None):
    """Don't any longer receive events from source.  If 'sink' is
    specified, only connections to this objects are closed.  If
    'interface' is specified, only comections from this interface are
    closed.
    """
    count = 0
    # make a copy since we will delete entries
    for (ref, s, itf), release in _active_events.copy().iteritems():
        if ref() == source:
            if sink is None or s == sink:
                if interface is None or interface == itf:
                    release(ref)
                    count += 1
    # Should count == 0 be an error?
    return count

################################################################
#
# Object creation
#
def GetActiveObject(progid,
                    interface=None,          # the interface we want
                    sink=None,               # where to send events
                    sourceinterface=None):   # the event interface we want
    clsid = comtypes.GUID.from_progid(progid)
    if interface is None:
        interface = getattr(progid, "_com_interfaces_", [None])[0]
    obj = comtypes.GetActiveObject(clsid, interface=interface)
    return _manage(obj, clsid,
                  interface=interface,
                  sink=sink,
                  sourceinterface=sourceinterface)
                    
def _manage(obj, clsid, interface,
            sink, sourceinterface):
    if interface is None:
        obj = wrap(obj)
    if sink is not None:
        if sourceinterface is None:
            # use default outgoing interface for the coclass.
            sourceinterface = comtypes.com_coclass_registry[str(clsid)]._outgoing_interfaces_[0]
        GetEvents(obj, sink, sourceinterface)
    return obj


def CreateObject(progid,                  # which object to create
                 clsctx=None,             # how to create the object
                 machine=None,            # where to create the object
                 interface=None,          # the interface we want
                 sink=None,               # where to send events
                 sourceinterface=None):   # the event interface we want
    """Create a COM object from 'progid', and try to QueryInterface()
    it to the most useful interface, generating typelib support on
    demand.  A pointer to this interface is returned.

    'progid' may be a string like "InternetExplorer.Application",
       a string specifying a clsid, a GUID instance, or an object with
       a _clsid_ attribute which should be any of the above.
    'clsctx' specifies how to create the object, use the CLSCTX_... constants.
    'machine' allows to specify a remote machine to create the object on.
    'sink' specifies an optional object to receive COM events.
    'sourceinterface' is the interface that sends events.  If not specified,
        the default source interface is used.

    You can also later request to receive events with GetEvents().
    """
    clsid = comtypes.GUID.from_progid(progid)
    logger.debug("%s -> %s", progid, clsid)
    if interface is None:
        interface = getattr(progid, "_com_interfaces_", [None])[0]
    if machine is None:
        logger.debug("CoCreateInstance(%s, clsctx=%s, interface=%s)",
                     clsid, clsctx, interface)
        obj = comtypes.CoCreateInstance(clsid, clsctx=clsctx, interface=interface)
    else:
        logger.debug("CoCreateInstanceEx(%s, clsctx=%s, interface=%s, machine=%s)",
                     clsid, clsctx, interface, machine)
        obj = comtypes.CoCreateInstanceEx(clsid, clsctx=clsctx, interface=interface, machine=machine)
    return _manage(obj, clsid,
                   interface=interface,
                   sink=sink,
                   sourceinterface=sourceinterface)

def CoGetObject(displayname,
              interface=None,          # the interface we want
              sink=None,               # where to send events
              sourceinterface=None):   # the event interface we want
    """Create an object by calling CoGetObject(displayname).

    Additional parameters have the same meaning as in CreateObject().
    """
    punk = comtypes.CoGetObject(displayname, interface)
    return _manage(punk,
                   clsid=None,
                   interface=interface,
                   sink=sink,
                   sourceinterface=sourceinterface)

################################################################

def Dispatch(obj):
    # Wrap an object in a Dispatch instance, exposing methods and properties
    # via fully dynamic dispatch
    if isinstance(obj, _Dispatch):
        return obj
    if isinstance(obj, ctypes.POINTER(comtypes.automation.IDispatch)):
        return _Dispatch(obj)
    return obj

class _Dispatch(object):
    # Expose methods and properties via fully dynamic dispatch
    def __init__(self, comobj):
        self._comobj = comobj

    def __enum(self):
        e = self._comobj.Invoke(-4) # DISPID_NEWENUM
        return e.QueryInterface(comtypes.automation.IEnumVARIANT)

    def __getitem__(self, index):
        enum = self.__enum()
        if index > 0:
            if 0 != enum.Skip(index):
                raise IndexError, "index out of range"
        item, fetched = enum.Next(1)
        if not fetched:
            raise IndexError, "index out of range"
        return item

    def QueryInterface(self, *args):
        "QueryInterface is forwarded to the real com object."
        return self._comobj.QueryInterface(*args)

    def __getattr__(self, name):
##        tc = self._comobj.GetTypeInfo(0).QueryInterface(comtypes.typeinfo.ITypeComp)
##        dispid = tc.Bind(name)[1].memid
        dispid = self._comobj.GetIDsOfNames(name)[0]
        flags = comtypes.automation.DISPATCH_PROPERTYGET
        return self._comobj.Invoke(dispid,
                                   _invkind=flags)

    def __iter__(self):
        return _Collection(self.__enum())

##    def __setitem__(self, index, value):
##        self._comobj.Invoke(-3, index, value,
##                            _invkind=comtypes.automation.DISPATCH_PROPERTYPUT|comtypes.automation.DISPATCH_PROPERTYPUTREF)

class _Collection(object):
    def __init__(self, enum):
        self.enum = enum

    def next(self):
        item, fetched = self.enum.Next(1)
        if fetched:
            return item
        raise StopIteration

    def __iter__(self):
        return self


