#!/usr/bin/env python
# -*- coding: utf-8 -*-
from myMainWindow import myMainWindow
from PyQt5.QtWidgets import *
import logging

def main():
    """ Main program """
    # start the logger
    logging.basicConfig(filename='foodinator_log.log',format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO) # use INFO in release
    logging.info('App Started')

    # load the ui
    app = QApplication([])
    #window = QMainWindow()
    window = myMainWindow()

    # run the gui
    window.show()
    app.exec()
    #
    logging.info('Program exited normaly')
    # Code goes over here.
    return 0

if __name__ == "__main__":
    main()
