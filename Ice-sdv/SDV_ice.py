# -*- coding: utf-8 -*-
#
# Copyright (c) ZeroC, Inc. All rights reserved.
#
#
# Ice version 3.7.6
#
# <auto-generated>
#
# Generated from file `SDV.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

from sys import version_info as _version_info_
import Ice, IcePy

# Start of module fourApps
_M_fourApps = Ice.openModule('fourApps')
__name__ = 'fourApps'

_M_fourApps._t_SDV = IcePy.defineValue('::fourApps::SDV', Ice.Value, -1, (), False, True, None, ())

if 'SDVPrx' not in _M_fourApps.__dict__:
    _M_fourApps.SDVPrx = Ice.createTempClass()
    class SDVPrx(Ice.ObjectPrx):

        def initFourApps(self, s, context=None):
            return _M_fourApps.SDV._op_initFourApps.invoke(self, ((s, ), context))

        def initFourAppsAsync(self, s, context=None):
            return _M_fourApps.SDV._op_initFourApps.invokeAsync(self, ((s, ), context))

        def begin_initFourApps(self, s, _response=None, _ex=None, _sent=None, context=None):
            return _M_fourApps.SDV._op_initFourApps.begin(self, ((s, ), _response, _ex, _sent, context))

        def end_initFourApps(self, _r):
            return _M_fourApps.SDV._op_initFourApps.end(self, _r)

        @staticmethod
        def checkedCast(proxy, facetOrContext=None, context=None):
            return _M_fourApps.SDVPrx.ice_checkedCast(proxy, '::fourApps::SDV', facetOrContext, context)

        @staticmethod
        def uncheckedCast(proxy, facet=None):
            return _M_fourApps.SDVPrx.ice_uncheckedCast(proxy, facet)

        @staticmethod
        def ice_staticId():
            return '::fourApps::SDV'
    _M_fourApps._t_SDVPrx = IcePy.defineProxy('::fourApps::SDV', SDVPrx)

    _M_fourApps.SDVPrx = SDVPrx
    del SDVPrx

    _M_fourApps.SDV = Ice.createTempClass()
    class SDV(Ice.Object):

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::fourApps::SDV')

        def ice_id(self, current=None):
            return '::fourApps::SDV'

        @staticmethod
        def ice_staticId():
            return '::fourApps::SDV'

        def initFourApps(self, s, current=None):
            raise NotImplementedError("servant method 'initFourApps' not implemented")

        def __str__(self):
            return IcePy.stringify(self, _M_fourApps._t_SDVDisp)

        __repr__ = __str__

    _M_fourApps._t_SDVDisp = IcePy.defineClass('::fourApps::SDV', SDV, (), None, ())
    SDV._ice_type = _M_fourApps._t_SDVDisp

    SDV._op_initFourApps = IcePy.Operation('initFourApps', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_string, False, 0),), (), None, ())

    _M_fourApps.SDV = SDV
    del SDV

# End of module fourApps
