from bokeh.plotting import figure
from bokeh.io import output_file, push_notebook, show

plot = figure()
plot.circle([1,2,3], [4,6,5])

handle = show(plot, notebook_handle=True)

# Update the plot title in the earlier cell
#plot.title.text = "New Title"
#push_notebook(handle=handle)