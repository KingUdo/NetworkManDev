#!/usr/bin/env python

import commands, re

def getmac(iface): #simple funktion to find the mac Adress of the interface which is given to it
    ifconfigOut = commands.getoutput("ifconfig " + iface) #check the output of ifconfig
    mac = re.search('\w\w:\w\w:.+\n', ifconfigOut)	#find the mac address
    if mac is None:					#break the whole process if no mac is found, I know not clean, but the easyest way for this script
	print ("Mac error")
	exit()
    else:
        parsedMac = mac.group()
    return parsedMac


##MAIN

file = open('/etc/NetworkManager/NetworkManager.conf', 'r') #Open the Network Manager conf file
filelist = []
for line in file:						#Itterate threw the lines of the config file, saveing those to the list 'filelist' and filtering the macs already in the file.
	filelist.append(line)
	if 'unmanaged-devices=' in line.strip():
		macs = re.findall('mac:(.*?)\;',line.strip())
		print("Unmannaged Devices: ")
		for x in range(len(macs)):
			print  macs[x]
file.close()
dev = raw_input("add(a) or remove(r): ")			#check with user if he wants to add or remove a mac
if dev == "a":
	dev1 = raw_input("Which device?: ")
	if any(getmac(dev1).strip() in s for s in macs):
		print(str(dev1) + " already not managed")
	else:
		print ("Adding: " + str(dev1) + " with mac: " + str(getmac(dev1).strip()))

		udev = ""
		for x in range(len(macs)):			#creating the macs string
			udev += "mac:" + str(macs[x].strip()) + ";"
		udev = "unmanaged-devices=" + udev + "mac:" + str(getmac(dev1).strip()) + ";\n"

		file = open('/etc/NetworkManager/NetworkManager.conf', 'w') #writing the whole dukument 

		for line in filelist:
		        if 'unmanaged-devices=' in line.strip():
				file.write(udev)
			else:
				file.write(line)
		file.close()
		output = commands.getoutput("sudo service network-manager restart") #restarting the network manager
		if output == "":
			print("success")

if dev == "r":
	dev1 = raw_input("Which device?: ")
	if any(getmac(dev1).strip() in s for s in macs):
                print ("Removing: " + str(dev1) + " with mac: " + str(getmac(dev1).strip()))
		udev = ""
		del macs[macs.index(getmac(dev1).strip())]

                for x in range(len(macs)):
                        udev += "mac:" + str(macs[x].strip()) + ";"
		udev = "unmanaged-devices="+ udev + "\n"

                file = open('/etc/NetworkManager/NetworkManager.conf', 'w')

                for line in filelist:
                        if 'unmanaged-devices=' in line.strip():
                                file.write(udev)
                        else:
                                file.write(line)
                file.close()
                output = commands.getoutput("sudo service network-manager restart")
                if output == "":
                        print("success")

	else:
		print(str(dev1) + " is already managed")
