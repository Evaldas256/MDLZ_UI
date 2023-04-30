def save_to_pdf(self):
    self.xy = np.load('my_array.npy', allow_pickle=True)
    # set page size to A4 in landscape orientation
    # Set A4 size in inches

    fig, ax = plt.subplots(figsize=(11.69, 8.27))

    ax.plot(self.xy[:, 0], self.xy[:, 1])
    self.y_min = np.amin(self.xy[:, 1])
    self.y_max = np.amax(self.xy[:, 1])
    # Define the colors
    colors = {'red': 'r', 'green': 'g', 'blue': 'b'}
    # Loop through the data and plot each segment
    handles = []
    for i in range(len(self.xy) - 1):
        x = [self.xy[i][0], self.xy[i + 1][0]]
        y = [self.xy[i][1], self.xy[i + 1][1]]
        color = colors[self.xy[i][2]]

        ax.fill_between(x, self.y_min, self.y_max, color=color, alpha=0.1)

    ax.legend(labels=colors.keys(), loc='upper right')
    ax.set_title('Temperature in time')
    self.formatter = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(self.formatter)

    # self.ui.MplWidget.canvas.draw()
    # create a PdfPages object and save the figure to PDF
    with PdfPages('output.pdf') as pdf:
        pdf.savefig(orientation='portrait')
