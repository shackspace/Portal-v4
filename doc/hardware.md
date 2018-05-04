# Portal v4 Hardware

## Hardware

The basis for the Portal is a ELV Keymatic lock that is controlled by a Raspberry Pi. The Keymatic normally is powered by batteries but the one used with the portal in the shackspace is modded for the use with a power adapter and the Raspberry Pi controlls it through two optical couplers.

## Input and Output

The Raspberry Pi is connected to the local network via ethernet (which is needed for ntp and sending the open/close status of the door in the shack rz). The internal Raspberry Pi wireless card is used as the wireless access point. The access point is not secured since only connections via ssh will be used.

The Raspberry Pi has two sensors. One reed contact which indictates if the door is closed and one contact which indicates if the lock is closed. A button initiates the closing procedure of the portal when pressed and door are closed (if reed contact reports that the door is closed). A beeper will give audio responses at the beginning, during and at the end of the closing procedure.

Two pins are needed for the opening and closing of the keymatic.

PIN 7	Keymatic open
PIN 11	Keymatic close
PIN 13	Door reed contact
PIN 15	Door lock contact
PIN 29	Close button
PIN 31	Bepper

## Known issues with portal hardware v1

* The debouncing of the close button via software does not seem to work. Now a capacitor was added parralel to the button. In the next PCB version the capacitor should be added to the PCB. The capacitor should then be added between Raspberry Pi GPIO pin and ground.
* The traces should have been wider. The resistance was significant from the breadboard to the PCB.

