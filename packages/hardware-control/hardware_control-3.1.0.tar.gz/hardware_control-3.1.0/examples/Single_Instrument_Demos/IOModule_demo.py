"""General IO Module demo

Usage:
  IOModule_demo.py [--conn_addr=CONN_ADD] [--dummy] [--debug] [--console] [--info]

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

from PyQt6.QtWidgets import QWidget, QGridLayout
from docopt import docopt
from pathlib import Path

import hardware_control.instruments as hc_inst
import hardware_control as hc

commands = docopt(__doc__)
dummy = commands["--dummy"]
conn_addr = commands["--conn_addr"]

logger = logging.getLogger(__name__)
hc.setup_logging_docopt(logger, commands)


class Demo(hc.HCMainWindow):
    def __init__(self, dummy):
        super().__init__(dummy=dummy)

        self.setWindowTitle("Demo")

        # This is the main widget, actual device widgets are added to it
        self.main_widget = QWidget(self)

        # Create an Ni_9000 instrument backend and add it to the app
        self.app.add_instrument(
            hc_inst.Ni_9000(
                instrument_name="NI-9000",
                connection_addr=conn_addr,
                modules=[1, 2],
                analog_channels={1: ["o0", "o1"], 2: ["i0", "i1", "i2", "i3", "i4"]},
            )
        )

        # Create a IOModule GUI control that connects to the instrument backend.
        # The control must be given a json file with information about each module
        # channel. See IOModule.py for more details.
        self.iomodule = hc.gui.IOModule(
            self.app,
            "NI-9000",
            Path.cwd() / "settings_files" / "nidaq_grid_conf.json",
            num_columns=2,
        )

        # Add control to the main widget
        self.grid = QGridLayout()
        self.grid.addWidget(self.iomodule, 0, 0)
        self.main_widget.setLayout(self.grid)

        self.setCentralWidget(self.main_widget)
        self.show()


if __name__ == "__main__":
    main_window = Demo(dummy=dummy)
    sys.exit(main_window.app.exec_())
