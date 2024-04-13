# Skelescope
A simple interactive 3D skeleton viewer for Jupyter

## Development installation

Create a virtual environment and install skelescope in *editable* mode with the
optional development dependencies:

```sh
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pip install navis
pip install pandas
```

You then need to install the JavaScript dependencies and run the development server.

```sh
npm install
npm run dev
```

All is set to open `example.ipynb` in JupyterLab, VS Code, or your favorite editor
to start developing. Any change made in the `js` folder will be directly reflected
in the notebook.


### Proposed Interface (Jakob, edited pha)

```python
viewer = NeuriteViewer(
  width = "500", # non-required value. defaults to filling the widget
  height = "300"
)

# add neuron to viewer instance
viewer.loadNeuron(
  swc, # swc in JSON format
  synapses, # JSON format (position, [pre_post_annotation, graph_node_id])
  tree_topology = None
  cache_folder = None 
  name = None, # not required, defaults to "<root_id>"
  neuronColor, # not required, defaults to random color
  synapseColor, # not required
  recenter_camera=True # not required
)

# synapses are attached to the neuron as neuron.connectors.

# remove neuron from instance
viewer.deleteNeuron(
  name # can be manually assigned name or <root_id>
)

viewer.getNeuronSelection(
  names # list of all neuron names to get selection from, not required parameter
)

viewer.getSegmentSelection(
  names # list of all neuron names to get selection from, not required parameter
)

viewer.getSynapseSelection(
  names # # list of all neuron names to get synapse selection from, not required parameter
)

viewer.show() # renders the widget


```


