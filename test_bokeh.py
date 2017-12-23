import csv
import numpy as np
import pandas as pd
from bokeh.client import push_session
from bokeh.plotting import figure, curdoc, show, output_file

from bokeh.models import HoverTool


filename = input("Enter a file name: ")

file = open(filename, 'r')
csvCursor = csv.reader(file)

is_header = True
input_data = dict()
header = []

        
p = figure(toolbar_location=None)
p.xaxis.major_label_orientation = np.pi/4

i = 0
# initialize line and circle #
#lin = p.line(x=[], y=[])
cir = p.circle(x=[], y=[])
dc = cir.data_source
#dl = lin.data_source


# open a session to keep our local document in sync with server
session = push_session(curdoc())


#test = 20
for row in csvCursor:
    if is_header:
        # store keys in dict #
        header = row
        for i in range(len(row)):
            input_data[row[i]] = []

        # change just some things about the x-axes and y-axes
        p.xaxis.axis_label = header[0]
        #p.yaxis.axis_label = header[1]

        is_header = False
    else:
        #if test>0:
        for i in range(len(row)):
            if i==0: # store year #
                tmp = row[i].split('-')
                year = ''
                for it in tmp:
                    year += it
                input_data[header[i]].append(int(year))
            else:
                input_data[header[i]].append(float(row[i]))
        #test -= 1
    
def callback():
    global i
    new_data = dict()
    new_data['x'] = dc.data['x'] + input_data['Date'][:i]
    new_data['y'] = dc.data['y'] + input_data['Open'][:i]
    
    dc.data = new_data

    i += 50

curdoc().add_periodic_callback(callback, 50)
#curdoc().add_root(p)
#source = ColumnDataSource(input_data)

#p.circle(x = input_data['Date'], y = input_data['Open'])

#output_file("legend_labels.html")
session.show(p)
session.loop_until_closed() # run forever