import nmcli, json

try:
    nmcli.disable_use_sudo()
    for dev in nmcli.device():
        if dev.device_type != 'wifi':
            continue
        results = nmcli.device.show(dev.device)
        info = dict()
        info["device"] = dev.device
        if results:
            info["connected"] = "yes"
            info["ssid"] = results["GENERAL.CONNECTION"]
            info["address"] = results["IP4.ADDRESS[1]"].split("/")[0]
        else:
            info["connected"] = "no"
        print(info)
#    print(nmcli.connection())
 #   print(nmcli.device())
  #  print(nmcli.device.wifi())
   # print(nmcli.general())

#    nmcli.device.wifi_connect('AP1', 'passphrase')
 #   nmcli.connection.modify('AP1', {
  #          'ipv4.addresses': '192.168.1.1/24',
   #         'ipv4.gateway': '192.168.1.255',
    #        'ipv4.method': 'manual'
     #   })
#    nmcli.connection.down('AP1')
 #   nmcli.connection.up('AP1')
  #  nmcli.connection.delete('AP1')
except Exception as e:
    print(e)
