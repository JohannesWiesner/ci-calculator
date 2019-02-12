import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib
import numpy as np
from scipy.stats import norm
from PIL import Image
import os

def callPlotWindow():

    # convert matplotlib's intern 'C0' to rgba tuple
    default_blue_hex = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
    default_blue_rgba = matplotlib.colors.to_rgba(default_blue_hex)

    def lighter(color, percent):
        # color = np.array(color)
        white = np.array([1,1,1,1])
        vector = white-color
        return color + vector * percent

    plotdata = dict()
    plotdata['sd'] = 10
    plotdata['mean'] = 50

    my_dpi =  144

    fig = plt.figure(figsize=(256/my_dpi, 256/my_dpi), dpi=my_dpi,frameon=False)

    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # create x values for normal distribution
    x_normdist = np.concatenate((
    np.linspace(plotdata["mean"] - 3 * plotdata["sd"], plotdata["mean"] - 2 * plotdata["sd"],endpoint=False),
    np.linspace(plotdata["mean"] - 2 * plotdata["sd"], plotdata["mean"] - 1 * plotdata["sd"],endpoint=False),
    np.linspace(plotdata["mean"] - 1 * plotdata["sd"], plotdata["mean"] + 1 * plotdata["sd"],endpoint=False),
    np.linspace(plotdata["mean"] + 1 * plotdata["sd"], plotdata["mean"] + 2 * plotdata["sd"],endpoint=False),
    np.linspace(plotdata["mean"] + 2 * plotdata["sd"], plotdata["mean"] + 3 * plotdata["sd"])
    ))

    # plot normal distribution curve
    y_normdist = norm.pdf(x_normdist,plotdata["mean"],plotdata["sd"])
    ax.plot(x_normdist,y_normdist)

    # create logical lists which are used for 'where'-argument in fill-between method
    average = (x_normdist >= (plotdata["mean"] - 1 * plotdata["sd"])) & (x_normdist <= (plotdata["mean"] + 1 * plotdata["sd"]))
    above_and_below_average = (x_normdist >= (plotdata["mean"] - 2 * plotdata["sd"])) & (x_normdist <= (plotdata["mean"] - 1 * plotdata["sd"])) | (x_normdist >= (plotdata["mean"] + 1 * plotdata["sd"])) & (x_normdist <= (plotdata["mean"] + 2 * plotdata["sd"]))
    far_above_and_below_average = (x_normdist >= (plotdata["mean"] - 3 * plotdata["sd"])) & (x_normdist <= (plotdata["mean"] - 2 * plotdata["sd"])) | (x_normdist >= (plotdata["mean"] + 2 * plotdata["sd"])) & (x_normdist <= (plotdata["mean"] + 3 * plotdata["sd"]))

    regions = [average,
    above_and_below_average,
    far_above_and_below_average
    ]

    colors = [
    lighter(default_blue_rgba,0.25),
    lighter(default_blue_rgba,0.5),
    lighter(default_blue_rgba,0.75)
    ]

    # shade regions under curve, use different alpha channel values and labels
    for idx,region in enumerate(regions):
        plt.fill_between(x_normdist, y_normdist,color=colors[idx],where=regions[idx])

    # save image as png
    plt.savefig('app_icon.png',dpi=my_dpi,transparent=True)

    # convert to .ico
    img = Image.open('app_icon.png')
    img.save('app_icon.ico',sizes=[(255,255)],dpi=my_dpi)

    # delete unneeded png
    os.remove('app_icon.png')

if __name__ == "__main__":
    callPlotWindow()