#!/usr/bin/python3

from gi.repository import GLib

import dbus
import dbus.mainloop.glib
import json

def printr(junk):
    return

_dbus2py = {
    dbus.String : str,
    dbus.UInt32 : int,
    dbus.Int32 : int,
    dbus.Int16 : int,
    dbus.UInt16 : int,
    dbus.UInt64 : int,
    dbus.Int64 : int,
    dbus.Byte : int,
    dbus.Boolean : bool,
    dbus.ByteArray : str,
    dbus.ObjectPath : str
}

def dbus2py(d):
    t = type(d)
    if t in _dbus2py:
        return _dbus2py[t](d)
    if t is dbus.Dictionary:
        return dict([(dbus2py(k), dbus2py(v)) for k, v in d.items()])
    if t is dbus.Array and d.signature == "y":
        return "".join([chr(b) for b in d])
    if t is dbus.Array or t is list:
        return [dbus2py(v) for v in d]
    if t is dbus.Struct or t is tuple:
        return tuple([dbus2py(v) for v in d])
    return d

def pretty(d):
    d = dbus2py(d)
    t = type(d)

    if t in (dict, tuple, list) and len(d) > 0:
        if t is dict:
            d = ", ".join(["%s = %s" % (k, pretty(v)) for k, v in d.items()])
            return "{ %s }" % d

        d = " ".join([pretty(e) for e in d])

        if t is tuple:
            return "( %s )" % d

    if t is str:
        return "%s" % d

    return str(d)

def properties_changed(interface, changed, invalidated, path):
    iface = interface[interface.rfind(".") + 1:]
    for name, value in changed.items():
        printr("{%s} [%s] %s = %s" % (iface, path, name, pretty(value)))

relevant_ifaces = ["net.connman.iwd.Network"]

def interfaces_added(path, interfaces):
    for iface, props in interfaces.items():
        if not(iface in relevant_ifaces):
            continue

        printr("{Added %s} [%s]" % (iface, path))

        #PRINT JUNK
        for name, value in props.items():
            if name == "Name" and not (value.startswith("/net/connman/iwd")):
                for namee, valuee in props.items():
                    if namee == "Connected" and dbus2py(valuee) == True:
                        print("Connected to "+value)


def interfaces_removed(path, interfaces):
    for iface in interfaces:
        if not(iface in relevant_ifaces):
            continue

        printr("{Removed %s} [%s]" % (iface, path))

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    bus.add_signal_receiver(properties_changed,
                            bus_name="net.connman.iwd",
                            dbus_interface="org.freedesktop.DBus.Properties",
                            signal_name="PropertiesChanged",
                            path_keyword="path")

    bus.add_signal_receiver(interfaces_added, bus_name="net.connman.iwd",
                            dbus_interface="org.freedesktop.DBus.ObjectManager",
                            signal_name="InterfacesAdded")

    bus.add_signal_receiver(interfaces_removed, bus_name="net.connman.iwd",
                            dbus_interface="org.freedesktop.DBus.ObjectManager",
                            signal_name="InterfacesRemoved")

    mainloop = GLib.MainLoop()
    mainloop.run()
