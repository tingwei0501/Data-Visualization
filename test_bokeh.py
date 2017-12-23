import csv
import numpy as np
import pandas as pd
from bokeh.client import push_session
from bokeh.plotting import figure, curdoc, show, output_file

from bokeh.models.widgets import Panel, Tabs


filename = input("Enter a file name: ")

file = open(filename, 'r')
csvCursor = csv.reader(file)

is_header = True
input_data = dict()
header = []

# declare figure #     
p1 = figure(toolbar_location=None)
p1.xaxis.major_label_orientation = np.pi/4
p2 = figure(toolbar_location=None)
p2.xaxis.major_label_orientation = np.pi/4
p3 = figure(toolbar_location=None)
p3.xaxis.major_label_orientation = np.pi/4

# panel #
tab1 = Panel(child=p1, title="circle")
tab2 = Panel(child=p2, title='vbar')
tab3 = Panel(child=p3, title='line')

tabs = Tabs(tabs=[ tab1, tab2, tab3 ])

start_i = end_i = 0
start_j = end_j = 0
start_k = end_k = 0

# initialize graph #
cir = p1.circle(x=[], y=[])
bar = p2.vbar(x=[],top=[], width=0.5)
lin = p3.line(x=[], y=[])

dc = cir.data_source
db = bar.data_source
dl = lin.data_source

# open a session to keep our local document in sync with server
session = push_session(curdoc())

for row in csvCursor:
    if is_header:
        # store keys in dict #
        header = row
        for i in range(len(row)):
            input_data[row[i]] = []

        # change just some things about the x-axes and y-axes
        p1.xaxis.axis_label = header[0]
        p2.xaxis.axis_label = header[0]
        p3.xaxis.axis_label = header[0]
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
print (len(input_data['Date']))   
def cir_callback():
    global start_i, end_i
    new_data = dict()
    new_data['x'] = dc.data['x'] + input_data['Date'][start_i:end_i]
    new_data['y'] = dc.data['y'] + input_data['Open'][start_i:end_i]
    
    dc.data = new_data

    start_i = end_i
    end_i += 50

def bar_callback():
    global start_j, end_j
    new_data = dict()
    new_data['x'] = db.data['x'] + input_data['Date'][start_j:end_j]
    new_data['top'] = db.data['top'] + input_data['Open'][start_j:end_j]
    
    db.data = new_data

    start_j = end_j
    end_j += 50

def lin_callback():
    global start_k, end_k
    new_data = dict()
    new_data['x'] = dl.data['x'] + input_data['Date'][start_k:end_k]
    new_data['y'] = dl.data['y'] + input_data['Open'][start_k:end_k]

    dl.data = new_data

    start_k = end_k
    end_k += 50

def close():
    # didn't finish the graph #
    if end_i>=len(input_data['Date']) and end_j>=len(input_data['Date']) and end_k>=len(input_data['Date']):
        print (end_i, end_j, end_k)
        session.close()

curdoc().add_periodic_callback(cir_callback, 50)
curdoc().add_periodic_callback(bar_callback, 50)
curdoc().add_periodic_callback(lin_callback, 50)
#curdoc().add_periodic_callback(close, 25)


session.show(tabs)

session.loop_until_closed() # run forever