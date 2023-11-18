x_axis_size = 250 # sets how many data points are kept for plotting
time_between_updates = 1 # sets how often the plots update function is called, in ms
window = 1

#load data from csv to numpy array
df = pd.read_csv("MyoDataLive.csv", dtype="Int64", delimiter = ";")
print(df)
csv_data = df.to_numpy()


#vectors holding data being plotted
sensor_vectors = np.zeros((8,x_axis_size,)) # different sensor_vectors for each sensor


# Create a PyQtGraph application
app = QApplication([])

# Create a PyQtGraph plot window
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('Live Vector Plot')

# Create a list to store PlotItem objects for each vector
plots = []

# Initialize the plots with the initial data
colorList = ["#fa9189", "#fcae7c",
                      "#ffe699", "#f9ffb5", "#b3f5bc", "#d6f6ff", "#e2cbf7", "#d1bdf1"]
plot = '1'
plot_position_iterator = 1 # used to determine when to create new row or column
for vector in sensor_vectors:
    plot = win.addPlot(title=f"Channel {plot_position_iterator}")
    plot.setXRange(0,x_axis_size)
    curve = plot.plot(vector, pen=colorList[plot_position_iterator - 1])
    plots.append({'plot': plot, 'curve': curve})
    if plot_position_iterator % 2 == 0:
        win.nextRow()
    elif plot_position_iterator % 2 == 1:
        win.nextCol()
    plot_position_iterator += 1

# Function to update the plots with new data
x_value = 0
data_index = 0
def update_plots():
    global x_value
    global data_index

    if 0: #0 for normal shift left plotting, 1 for sweeping with wrap around
        for i in range(8):
            # sensor_vectors[i][x_value] = fake_data[0][i]
            sensor_vectors[i][x_value] = csv_data[data_index][i]
            plots[i]['curve'].setData(sensor_vectors[i])
            if x_value == x_axis_size - 1:
                sensor_vectors[i][0] = 0
            else:
                sensor_vectors[i][x_value+1] = 0
            plots[i]['curve'].setData(sensor_vectors[i])
        x_value += 1
        if x_value == x_axis_size:
            x_value = 0
    else:
        for i, vector in enumerate(sensor_vectors):
            sensor_vectors[i] = np.roll(sensor_vectors[i], -1)  # shift data to the left
            sensor_vectors[i][-1] = csv_data[data_index][i]  # add new data point to end
            plots[i]['curve'].setData(vector) # update plot
    data_index += 1
    if(data_index == (csv_data.size / 8) - 1): #return to start of csv file
        data_index = 0

# Create a QTimer to periodically update the plots (e.g., every 100 ms)
timer = QTimer()
timer.timeout.connect(update_plots)
timer.start(time_between_updates)

# Start the PyQtGraph application event loop
app.exec_()
