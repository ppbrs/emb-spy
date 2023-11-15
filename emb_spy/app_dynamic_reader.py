from __future__ import annotations

# Standard library imports
import logging
import os
import time
# Third party imports
import matplotlib.pyplot as plt
# Local application/library imports
from .backend import Backend
from ._app_reader import _AppReader


class AppDynamicReader(_AppReader):
    """A class that contains methods of the application."""

    def __call__(self, duration: float) -> list:

        self.logger.debug("App called.")

        with Backend(
                host=self.host, port=self.port, target_name=self.target_name,
                logger_suffix=self.logger_suffix, start_if_reset=self.start_if_reset) as backend:
            t_start = time.monotonic()
            t_stop = t_start + duration
            while time.monotonic() <= t_stop:
                for reg_data in self.regs_data:
                    reg_data.vals.append((time.monotonic() - t_start, backend.read_register(addr=reg_data.register.addr)))
                for s_data in self.syms_data:
                    s_data.vals.append((time.monotonic() - t_start, backend.read_memory(addr=s_data.addr, ctype=s_data.ctype)))

        # plot
        self.logger.debug("Plotting.")
        logging.getLogger().setLevel(logging.INFO)
        fig = plt.figure(os.path.basename(__file__))

        # num_subplots = len(self.regs_data) + len(self.syms_data)
        num_subplots = len(self.syms_data)
        self.logger.info("%d subplots.", num_subplots)

        axes = [fig.add_subplot(num_subplots, 1, i + 1) for i in range(num_subplots)]
        self.logger.info("axes=%s, %d subplots.", axes, num_subplots)

        i = 0
        for sym_data in self.syms_data:

            axis = axes[i]

            timestamps = [t for t, _ in sym_data.vals]
            values = [v for _, v in sym_data.vals]
            axis.plot(timestamps, values, label="symbol=" + sym_data.name)
            i += 1

        for ax in fig.get_axes():
            ax.grid(True)
            ax.legend(loc='best', fontsize='small')
        plt.show()
