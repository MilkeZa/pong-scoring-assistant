# Ping Pong Scoring Assistant

A system designed to assist in the process of keeping score for ping pong games between individual players, or teams. Built using the MicroPython programming language and some basic electronic components, it really just counts up or down based on button input and displays those counts on two small screens meant to be
placed on opposing sides of the table.

## Required Libraries / Packages

| Name | Description | URL |
| :--- | :---------- | :-- |
| MicroPython | Microcontroller port of the Python language. | [Home](https://micropython.org) |
| micropython_ssd1306 | SSD1306 module for MicroPython. | [Home](https://github.com/stlehmann/micropython-ssd1306) / [PyPI](https://pypi.org/project/micropython-ssd1306/) |

## Using the system

There are an endless number of methods that can be used to run the system. In the current state, a *main.py* file is created on the Pico, which is run at startup. Within this file, the pps_start function is imported and subsequently called within the main method. Should the hardware and software be setup and loaded properly, it should be plug and play.

## Future Considerations

> *Think of this as a 'TODO if possible' list.*

Be it generic bug fixes or efficiency improvements, here is a non-comprehensive list of things that I would like to implement or adjust in the future.

- [ ] Adding images of the current setup to the GitHub repository.
- [ ] Adding the circuit diagram for the hardware to the GitHub repository files.
- [ ] Ability to power the entire setup from a 9v battery. A voltage converter such as a buck converter will be necessary, as the Pico takes 5v power input. This would remove the 5v power supply and micro-usb cable from the parts list, in addition to making the whole setup mobile.

    1. Along with battery power, it would be nice to have an On/Off switch so that it wouldn't be necessary to plug in the power to use it and unplug it when finished.
    2. Another thing that would be useful is an estimation of battery life left that shows on both screens. I have no clue how to go about this, but would be nice to gauge the power draw of the device and determine when a new battery would be necessary. A simple "progress bar"-esque line of pixels at the bottom the screen would suffice.
