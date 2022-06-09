#!/usr/bin/env python
# -*- coding: utf-8 -*-
from MyMainWindow import MyMainWindow
from PyQt5.QtWidgets import *
import logging
from logging.handlers import RotatingFileHandler
from AppDefaults import AppDefaults
from foodClasses import *
import sys

# setup the logger
logging.basicConfig(filename=AppDefaults().logging_path,
                    format=AppDefaults().logging_format,
                    level=logging.INFO)
main_logger = logging.getLogger('foodinator.main')



def main(args):
    """ Main program """
    main_logger.info("Starting application")
    # load the ui
    app = QApplication([])
    window = MyMainWindow()

    # run the gui
    window.show()
    app.exec()
    #
    main_logger.info('App exited normally.')
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
