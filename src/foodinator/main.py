#!/usr/bin/env python
# -*- coding: utf-8 -*-
from myMainWindow import myMainWindow
from PyQt5.QtWidgets import *
import logging
from foodClasses import *
import sys


def main(args):
    """ Main program """

    # load the ui
    app = QApplication([])
    window = myMainWindow()

    # run the gui
    window.show()
    app.exec()
    #
    logging.info('App exited normally.')
    # Code goes over here.
    return 0


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    run()