#!/usr/bin/env python3
"""Flow-Controller demo

Usage:
  FlowController_demo.py [--conn_addr=CONN_ADD] [--dummy] [--debug] [--console] [--info]

Options:
  --conn_addr=CONN_ADD  Connection address of physical instrument [default: None].
                        Required if not in dummy mode.
  --dummy               Use dummy connection for instruments that return semi-random data
                        so that one can run the program away from the test stand.
  --debug               Allow debug print statements.
  --info                Allow info print statements.
  --console             Print logger output to console.
"""

import logging
import sys

from docopt import docopt

from PyQt6.QtWidgets import QGridLayout, QTabWidget

import hardware_control as hc

commands = docopt(__doc__)
dummy = commands["--dummy"]
conn_addr = commands["--conn_addr"]

logger = logging.getLogger(__name__)
hc.setup_logging_docopt(logger, commands)


class Demo(hc.HCMainWindow):
    def __init__(self, dummy):
        super().__init__(dummy=dummy)

        self.setWindowTitle("Flow Controller Demo")

        # This is the main widget (a widget with tabs), actual device widgets are added to it
        self.tabs = QTabWidget()

        # Create an flow controller Alicat_M_Series instrument backend and add it to the app
        self.app.add_instrument(hc.instruments.Alicat_M_Series("alicat", conn_addr))

        # Create a FlowController GUI control that connects to the instrument backend
        self.instr_ctrl = hc.gui.FlowController(self.app, "alicat", "Flow Controller")

        # Create an interactive ipython console
        self.ipython = hc.gui.Qtconsole(self.app)

        # Create tabs for the flow controller control and the ipython console, respectively
        self.tabs.addTab(self.instr_ctrl, "Instruments")
        self.tabs.addTab(self.ipython, "Interactive")

        self.setCentralWidget(self.tabs)
        self.show()


main_window = Demo(dummy=dummy)
sys.exit(main_window.app.exec_())
