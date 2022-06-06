#!/usr/bin/env python
# -*- coding: utf-8 -*-
from myMainWindow import myMainWindow
from PyQt5.QtWidgets import *
import logging
from foodClasses import *
#TODO fix bug, if asking to find N random receipe and we have less than N receipe in total.
def main():
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


if __name__ == "__main__":
    main()
