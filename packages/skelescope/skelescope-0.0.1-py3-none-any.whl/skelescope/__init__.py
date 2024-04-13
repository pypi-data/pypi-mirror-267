import importlib.metadata
import pathlib

import anywidget
import traitlets

try:
    __version__ = importlib.metadata.version("skelescope")   
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class Skelescope(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"
    segments = traitlets.Dict({}).tag(sync=True)
    selected_segments = traitlets.List([]).tag(sync=True)
    camera_target = traitlets.List([]).tag(sync=True)
    camera_position = traitlets.List([]).tag(sync=True)
    show_arrows = traitlets.Bool(False).tag(sync=True)
    show_branches = traitlets.Bool(True).tag(sync=True)
    show_synapses = traitlets.Bool(True).tag(sync=True)

    def add_neuron(self, swc):
        self.segments = swc
        