import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from .db import get_most_recent_run_info
from .utilization import calculate_utilization


class VizTk(tk.Tk):

    def __init__(self, plot_file_path: Path | None = None):
        super().__init__()
        self.plot_file_path = plot_file_path
        self.run_info = get_most_recent_run_info()
        self.title("Test Phases Timeline")
        self.fig, self.ax = plt.subplots(figsize=(20, 3 + len(self.run_info) * 0.5))  # Dynamic height based on the number of tests

        sorted_data = dict(sorted(self.run_info.items(), key=lambda x: x[0], reverse=True))
        worker_utilization, overall_utilization = calculate_utilization(sorted_data)
        earliest_start = min(phase.start for test in sorted_data.values() for phase in test.values())

        workers = set(info.worker_id for test in sorted_data.values() for info in test.values())
        colors = plt.cm.jet(np.linspace(0, 1, len(workers)))
        worker_colors = dict(zip(workers, colors))

        yticks, yticklabels = [], []
        for i, (test_name, phases) in enumerate(sorted_data.items()):
            for phase_name, phase_info in phases.items():
                relative_start = phase_info.start - earliest_start
                relative_stop = phase_info.stop - earliest_start
                worker_id = phase_info.worker_id

                self.ax.plot([relative_start, relative_stop], [i, i], color=worker_colors[worker_id], marker="o", markersize=4, label=worker_id if phase_name == "setup" else "")

                if phase_name == list(phases.keys())[0]:
                    yticks.append(i)
                    yticklabels.append(test_name)

        self.ax.set_yticks(yticks)
        self.ax.set_yticklabels(yticklabels)
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("Test Names")
        self.ax.set_title("Timeline of Test Phases per Worker")
        self.ax.grid(True)

        self.ax.text(1.0, 1.02, f"Overall Utilization: {overall_utilization:.2%}", transform=self.ax.transAxes, horizontalalignment="right", fontsize=9)
        text_position = 1.05
        for worker, utilization in worker_utilization.items():
            self.ax.text(1.0, text_position, f"{worker}: {utilization:.2%}", transform=self.ax.transAxes, horizontalalignment="right", fontsize=9)
            text_position += 0.03

        handles, labels = self.ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        legend = self.ax.legend(by_label.values(), by_label.keys(), title="Workers", loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=9)

        plt.subplots_adjust(right=0.9)  # Make space for the legend

        # Use bbox_extra_artists to include the legend in the tight layout calculation
        if self.plot_file_path is not None:
            self.plot_file_path.parent.mkdir(parents=True, exist_ok=True)
            self.fig.savefig(self.plot_file_path, bbox_extra_artists=[legend])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def destroy(self):
        self.canvas.stop_event_loop()
        super().destroy()


def visualize(plot_file_path: Path | None = None) -> None:
    """
    Visualize a timeline of test phases per worker.
    :param plot_file_path: Path to save the plot to.
    """

    root = VizTk(plot_file_path)
    root.mainloop()
