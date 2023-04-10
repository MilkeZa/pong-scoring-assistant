"""
File   : ping_pong.py
Author : Zachary Milke
Description : 
    Builds the PingPongSystem class, defining the structure with which
    the system will act. In as few words as possible, it helps keep the score for
    people playing ping pong who are too lazy to use a whiteboard or remember the
    score in their heads. Numbers are hard sometimes.

Created on  : 04-APR-2023
Updated on  : 10-APR-2023

"""


# Imports ---------------------------------------------------------------------
from machine import (
    Pin,
    I2C
)
from _thread import start_new_thread
from utime import (
    ticks_ms,
    ticks_diff,
    sleep_ms
)
from ssd1306 import SSD1306_I2C


# Class Definition ------------------------------------------------------------
class PingPongSystem:
    """
    A class used to setup and operate the ping pong scoring assist system.
    """

    def __init__(self):
        self.p1_sub_trigger, self.p1_add_trigger = 0, 0
        self.p2_sub_trigger, self.p2_add_trigger = 0, 0

        # Create the buttons used to increment/decrement score.
        # With n being the player #:
        #   btn_pn_add = Increment score for player n.
        #   btn_pn_sub = Decrement score for player n.
        self.btn_p1_sub = Pin(16, Pin.IN, Pin.PULL_UP)
        self.btn_p1_add = Pin(17, Pin.IN, Pin.PULL_UP)
        self.btn_p2_sub = Pin(18, Pin.IN, Pin.PULL_UP)
        self.btn_p2_add = Pin(19, Pin.IN, Pin.PULL_UP)

        # Setup debouncing to prevent weird behavior in buttons.
        self.debounce_delay = 250  # Time in ms between valid button presses.
        self.p1_sub_last, self.p1_add_last = ticks_ms(), ticks_ms()
        self.p2_sub_last, self.p2_add_last = ticks_ms(), ticks_ms()
        self.btn_p1_sub.irq(trigger=Pin.IRQ_RISING, handler=self.btn_handler)
        self.btn_p1_add.irq(trigger=Pin.IRQ_RISING, handler=self.btn_handler)
        self.btn_p2_sub.irq(trigger=Pin.IRQ_RISING, handler=self.btn_handler)
        self.btn_p2_add.irq(trigger=Pin.IRQ_RISING, handler=self.btn_handler)

        # Values used for the score system.
        self.scores, self.scores_text = { 1: 0, 2: 0 }, { 1: "00", 2: "00" }

        # Setting up the I2C controllers and OLED devices.
        i2c1 = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
        i2c2 = I2C(1, sda=Pin(2), scl=Pin(3), freq=100000)

        self.oled1 = SSD1306_I2C(128, 64, i2c1)
        self.oled2 = SSD1306_I2C(128, 64, i2c2)

        # Draw and refresh the screens.
        self.draw_screens()
        self.refresh_screens()

    def draw_screens(self) -> None:
        """ Draws the header and body sections to the screens.
        """

        self.draw_header()
        self.draw_body()

    def draw_header(self) -> None:
        """ Draws the header section to the screen.
        """

        # White rectangle showing header area.
        self.oled1.rect(0, 0, 128, 24, 1)
        self.oled2.rect(0, 0, 128, 24, 1)

        self.oled1.text("Player 1", 30, 8)
        self.oled2.text("Player 2", 30, 8)

    def draw_body(self) -> None:
        """ Draws the body section to the screen.
        """

        # White rectangle showing body area.
        self.oled1.rect(0, 25, 128, 39, 1)
        self.oled2.rect(0, 25, 128, 39, 1)

        self.oled1.text("P1 - P1", 32, 32)
        self.oled2.text("P1 - P1", 32, 32)

        # Write the score text to screen.
        score_text = f"{self.scores_text[1]}   {self.scores_text[2]}"
        self.oled1.text(score_text, 32, 48)
        self.oled2.text(score_text, 32, 48)

        # Update the screens.
        self.refresh_screens()

    def redraw_body(self) -> None:
        """ Writes over body section with a filled black rectangle, then
        redraws the section with updated scores.
        """

        # Draw a black rectangle, essentially erasing previous graphics.
        self.oled1.fill_rect(0, 25, 128, 39, 0)
        self.oled2.fill_rect(0, 25, 128, 39, 0)

        # Redraw the body.
        self.draw_body()

    def refresh_screens(self) -> None:
        """ Calls the show method on both screens, updating any changes that
        may have been made.
        """

        self.oled1.show()
        self.oled2.show()

    def btn_handler(self, pin: Pin):
        """ Button handler to act as simple debouncer for buttons. First, the
        method will determine which button triggered the interrupt. It will
        then check if enough time has passed since the last time it was
        pressed. If yes, update the score, otherwise, do nothing.

        Params
        -----
        pin : Pin [required]
            Pin representing the button that was pressed.
        """

        # Determine which button was pressed.
        if pin is self.btn_p1_sub:
            if ticks_diff(ticks_ms(), self.p1_sub_last) > self.debounce_delay:
                self.p1_sub_trigger = 1
                self.p1_sub_last = ticks_ms()
        elif pin is self.btn_p1_add:
            if ticks_diff(ticks_ms(), self.p1_add_last) > self.debounce_delay:
                self.p1_add_trigger = 1
                self.p1_add_last = ticks_ms()
        elif pin is self.btn_p2_sub:
            if ticks_diff(ticks_ms(), self.p2_sub_last) > self.debounce_delay:
                self.p2_sub_trigger = 1
                self.p2_add_last = ticks_ms()
        elif pin is self.btn_p2_add:
            if ticks_diff(ticks_ms(), self.p2_add_last) > self.debounce_delay:
                self.p2_add_trigger = 1
                self.p2_add_last = ticks_ms()

    def update_scores(self, player: int, point: int) -> None:
        """ Increments/Decrements the current score for a given player.

        Params
        -----
        player : int [required]
            An integer value representing the player that will have their score
            updated.

        point : int [required]
            An integer value indicating the addition/subtraction of a point.
        """

        # Handle point logic. If point is positive, increment score for player.
        # if negative, check if point can be decremented. If yes, decrement
        # score. If no, subtract zero.
        if point == 1:
            self.scores[player] += 1
        else:
            self.scores[player] -= 1 if self.scores[player] > 0 else 0

        # Set the scores_text variables. Two digits will always show on the
        # screens. If score is below 10, leading digit is 0, otherwise,
        # leading digit is unchanged.
        score_text = str(self.scores[player])
        if len(score_text) == 1:
            score_text = f"0{score_text}"

        # Update the scores_text dictionary.
        self.scores_text[player] = score_text

        # Refresh the screens to show updated scores.
        # print("(Player, Score, Score Text)", end=' : ')
        # print(f"(P1, {self.scores[1]}, {self.scores_text[1]})", end=', ')
        # print(f"(P2, {self.scores[2]}, {self.scores_text[2]})")
        self.redraw_body()


def pps_start() -> None:
    """ Starts listening for an interrupt from the buttons indicating who
    has scored a point.
    """

    # Create a new PingPongSystem instance, then begin looping, waiting for
    # presses of the buttons.
    try:
        pp_system = PingPongSystem()

        while True:
            # Check for button triggers.
            if pp_system.p1_sub_trigger == 1:
                pp_system.p1_sub_trigger = 0
                pp_system.update_scores(1, -1)
            elif pp_system.p1_add_trigger == 1:
                pp_system.p1_add_trigger = 0
                pp_system.update_scores(1, 1)
            elif pp_system.p2_sub_trigger == 1:
                pp_system.p2_sub_trigger = 0
                pp_system.update_scores(2, -1)
            elif pp_system.p2_add_trigger == 1:
                pp_system.p2_add_trigger = 0
                pp_system.update_scores(2, 1)

    except KeyboardInterrupt as kb_exc:
        # Used primarily in building application and debugging. CTRL + C would
        # stop the app during a run.
        print(f"Keyboard interrupt, stopping.\n\n{kb_exc}")

    except Exception as exc:
        # This is a little too generic for my liking, but it's a simple way to
        # catch any exceptions that may creep up, causing unexcepted behaviour.
        print(f"Exception occurred during runtime. Details below: \n\n{exc}")


def blink_led(on_time: int = 250, off_time: int = 1500) -> None:
    """ Meant to be run on a separate thread from the PingPongSystem, this
    function toggles the state of the onboard LED at a given rate.

    Params
    -----
    on_time : int [required]
        An integer representing how long in milliseconds the onboard LED will
        remain ON.

    off_time : int [required]
        An integer representing how long in milliseconds the onboard LED will
        remain OFF. In other words, how long the LED will wait in the OFF state
        before turning back ON.
    """

    # Create the pin to control the LED state.
    onboard_led = Pin(25, Pin.OUT)

    # Loop constantly, blinking every blink_time milliseconds.
    while True:
        # Set the LED to a high state.
        onboard_led.value(1)
        sleep_ms(on_time)

        # Set the LED to a low state.
        onboard_led.value(0)
        sleep_ms(off_time)


def main():
    """ Main entrypoing for the application.
    """

    # Call the start method and begin playing.
    pps_start()


if __name__ == "__main__":
    main()
