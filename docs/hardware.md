# Hardware Used

This file contains more detailed information regarding the hardware that was used when planning and putting together the score keeping system.

## Component List

| Quantity | Component Name |
| :------: | :------------- |
| 1 | 5v power supply |
| 1 | Micro-usb cable |
| 1 | Raspberry Pi Pico |
| 2 | 400 point breadboard |
| 2 | 24mm (~1") OLED I^2C display |
| 4 | 6 x 6 x 6 mm tactile push buttons |
| 4 | 5.6k ohm resistors |
| *n*\* | Male to male jumper wires |
| *n*\* | Male to female jumper wires |
| *n*\* | Female to female jumper wires |

\**n* is simply a placeholder telling that quantities can and will vary greatly.

## Notes on the Component List

> **

Similar to the setup of files when running the system, the hardware required can also be polymorphic depending on how individuals want the system to run, or what they happen to have in their possession when building it. The list mentioned above is one of many that will get the job done in a "good enough" sort of way.

### Power supply

> *TL;DR any 5v DC power brick will work.*

It's also possible to use two (2) or three (3) 1.5v batteries in series to power the device. This would require additional components - or soldering if doing it by hand - but is within the realm of possibility.

Check out this link [here](https://projects.raspberrypi.org/en/projects/introduction-to-the-pico/12) for more infomration on powering the board, provided by the Raspberry Pi Foundation.

### Pi Pico

> *It's probably possible to get away with knockoff boards too.*

The setup I made uses the base Pico, however, the Pico H, Pico W, and Pico HW should all work as well. I haven't personally tested on any of these, but they operate on the same RP2040 microcontroller and MicroPython interpreter so if any changes to the setup are necessary, they're likely to be minimal.

### Breadboard

The pair 400 point breadboards used can be swapped out for a single 830 point board, or for a more permanent solution the components can be soldered directly to one another on a prototype board.

### 5.6k ohm resistors

These act as pull-up resistors for the I^2C communications channels, and don't necessarily need to be 5.6k ohm values, this is just what I found to give the results desired and be closest to me on my desk when designing.

### Jumper wires

The number of jumper wires required will depend on many factors, such as the number of pins grounded on the Pico, component positioning on the board, length of the wires, etc. Your build may choose to use exclusively M -> M combined with F -> F, or drop jumper wires completely in favor of 22 awg solid core copper wire.

## Warnings

### Don't be Stupid.
Use caution when connecting wires to one another and individual components. While nothing in this project would be powerful enough to do any damage, that doesn't mean you should go ahead and touch your tongue to both terminals of a 9v battery.

### Beware of Input Voltages.
The recommended input voltage for the board is between 1.8 - 5v, so while voltages outside this range may work temporarily, they can cause damage to the microcontroller or other components suddenly and without warning.
