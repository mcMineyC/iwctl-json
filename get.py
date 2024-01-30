from dbus_next.aio import MessageBus
from dbus_next import Variant
import asyncio

async def main():
    bus = await MessageBus().connect()

    # alternatively, get the data dynamically:
    introspection = await bus.introspect('net.connman.iwd', '/')

    proxy_object = bus.get_proxy_object('com.example.name',
                                        '/com/example/sample_object0',
                                        introspection)

    interface = proxy_object.get_interface('com.example.SampleInterface0')

    def changed_notify(new_value):
        print(f'The new value is: {new_value}')

    await interface.on_changed(changed_notify)

    # Use get_[PROPERTY] and set_[PROPERTY] with the property in
    # snake case to get and set the property.


    await bus.wait_for_disconnect()

asyncio.run(main())