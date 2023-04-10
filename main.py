"""
File   : main.py
Author : Zachary Milke
Description :
    This file is run when the Pi Pico it is loaded onto is plugged into power.

Created on : 06-APR-2023
Updated on : 10-APR-2023
"""


# Imports ---------------------------------------------------------------------
from ping_pong_system import pps_start


def main():
    """ Main entrypoint for the application.
    """

    # For help keeping track of Ping Pong scoring.
    pps_start()


if __name__ == "__main__":
    main()
