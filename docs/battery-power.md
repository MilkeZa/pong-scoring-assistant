# Notes on the Battery Ideas

It can't be that hard to do, right?

## Getting Acceptable Input Power

As mentioned in the *Power Supply* subsection of the *Notes on the Components List* in the HARDWARE.md file, the Pico accepts a range of 1.8v to 5.5v. A 9v battery would fry the board, and a 1.5v battery isn't enough to get things going.

### Don't Fry the Pi

> *This has not yet been tested, but in theory should work.*

One of the simplest things to allow for the use of powering the system via a 9v battery pack is to use a little thing called a step-down-converter, A.K.A a [*buck converter*](https://en.wikipedia.org/wiki/Buck_converter). This is something that can either be put together on another breadboard, or purchased from your favorite electronics supply shop.

### A Simpler Approach

> *This has not yet been tested, but in theory should work.*

An approach that's both simpler and cheaper is likely already within your house junk drawer, found in the form of a set of AA batteries.
