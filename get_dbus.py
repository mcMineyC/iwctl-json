#!/usr/bin/python3

import sys
import dbus
import collections

bus = dbus.SystemBus()

manager = dbus.Interface(bus.get_object("net.connman.iwd", "/"),
                                        "org.freedesktop.DBus.ObjectManager")
objects = manager.GetManagedObjects()

Obj = collections.namedtuple('Obj', ['interfaces', 'children'])
tree = Obj({}, {})
for path in objects:
    node = tree
    elems = path.split('/')
    for subpath in [ '/'.join(elems[:l + 1]) for l in range(1, len(elems)) ]:
        if subpath not in node.children:
            node.children[subpath] = Obj({}, {})
        node = node.children[subpath]
    node.interfaces.update(objects[path])

root = tree.children['/net'].children['/net/connman'].children['/net/connman/iwd']
for path, phy in root.children.items():
    if 'net.connman.iwd.Adapter' not in phy.interfaces:
        continue

    properties = phy.interfaces['net.connman.iwd.Adapter']

    print("[ %s ]" % path)

    for key in properties:
        val = properties[key]
        if key == 'SupportedModes':
            val = [str(mode) for mode in val]
        print("    %s = %s" % (key, val))

    print("    Devices:")

    for path2, device in phy.children.items():
        if 'net.connman.iwd.Device' not in device.interfaces:
            continue

        print("    [ %s ]" % path2)
        for interface in device.interfaces:
            name = interface.rsplit('.', 1)[-1]
            if name not in ('Device', 'Station', 'AccessPoint', 'AdHoc'):
                continue

            properties = device.interfaces[interface]
            for key in properties:
                val = properties[key]
                print("        %s.%s = %s" % (name, key, val))

            if name != 'Station':
                continue

            print("        Sorted networks:")

            station = dbus.Interface(bus.get_object("net.connman.iwd", path2),
                                     'net.connman.iwd.Station')
            for path3, rssi in station.GetOrderedNetworks():
                print("        [ %s ]" % path3)

                properties2 = objects[path3]['net.connman.iwd.Network']
                print("            SSID = %s" % (properties2['Name'],))
                print("            Signal strength = %i dBm" % (rssi / 100,))
                print("            Security = %s" % (properties2['Type'],))