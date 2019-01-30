import sys
import tkinter as tk
from tkinter import ttk
from collections import OrderedDict
import re
import math

# TODO check wich modules are used in the end
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from scipy.stats import norm
from scipy.stats import zscore

class Model:

    def __init__(self):

        self.parameters = OrderedDict({
            "reliability": None,
            "sd": None,
            "mean": None,
            "normvalue": None,
            "confidence_level": None,
            "question": None,
            "hypothesis": None
        })

        self.statistics = OrderedDict({
            "z_value": None,
            "se": None,
            "set": None,
            "normvalue_regression": None
            })

        self.intervals = OrderedDict({
            "ci_lower": None,
            "ci_upper": None,
            "ci_lower_regression": None,
            "ci_upper_regression": None,
            "ci": None,
            "ci_regression": None,
            })

        self.plotdata = dict()

    def set_parameter_values(self, value_list):
        keys = self.parameters.keys()
        self.parameters.update(zip(keys, value_list))

    # FIXME: Any way to make this code smaller and more readable?
    # Idea: Maybe use sql-database?
    def set_z_value(self):
        if self.parameters["question"] == "einseitig" and self.parameters["confidence_level"] == "80%":
            self.statistics["z_value"] = 0.8416

        elif self.parameters["question"] == "einseitig" and self.parameters["confidence_level"] == "90%":
            self.statistics["z_value"] = 1.282

        elif self.parameters["question"] == "einseitig" and self.parameters["confidence_level"] == "95%":
            self.statistics["z_value"] = 1.645

        elif self.parameters["question"] == "einseitig" and self.parameters["confidence_level"] == "99%":
            self.statistics["z_value"] = 2.326

        elif self.parameters["question"] == "zweiseitig" and self.parameters["confidence_level"] == "80%":
            self.statistics["z_value"] = 1.282

        elif self.parameters["question"] == "zweiseitig" and self.parameters["confidence_level"] == "90%":
            self.statistics["z_value"] = 1.645

        elif self.parameters["question"] == "zweiseitig" and self.parameters["confidence_level"] == "95%":
            self.statistics["z_value"] = 1.96

        elif self.parameters["question"] == "zweiseitig" and self.parameters["confidence_level"] == "99%":
            self.statistics["z_value"] = 2.576

    # FIXME: z theoretically also belongs to category 'statistics' so from a logical point of view it would make more sense to integrate setting of z in this function
    #        I decided to put the setting of z-value in a separate function called set_z_value for reasons of readability
    #        In case set_z_value function can be compressed, maybe merge the two functions again to one function to follow logical reasoning
    def calculate_statistics(self):
        self.statistics["se"] = self.parameters["sd"] * math.sqrt((1-self.parameters["reliability"]))
        self.statistics["set"] = self.parameters["sd"] * math.sqrt((self.parameters["reliability"] * (1-self.parameters["reliability"])))
        self.statistics["normvalue_regression"] = self.parameters["reliability"] * self.parameters["normvalue"] + self.parameters["mean"] * (1-self.parameters["reliability"])

    def calculate_confidence_intervals(self):
        self.intervals["ci_lower"] = self.parameters["normvalue"] - self.statistics["z_value"] * self.statistics["se"]
        self.intervals["ci_upper"] = self.parameters["normvalue"] + self.statistics["z_value"] * self.statistics["se"]
        self.intervals["ci_lower_regression"] = self.statistics["normvalue_regression"] - self.statistics["z_value"] * self.statistics["set"]
        self.intervals["ci_upper_regression"] = self.statistics["normvalue_regression"] + self.statistics["z_value"] * self.statistics["set"]
        self.intervals["ci"] = self.intervals["ci_upper"] - self.intervals["ci_lower"]
        self.intervals["ci_regression"] = self.intervals["ci_upper_regression"] - self.intervals["ci_lower_regression"]
    
    def run_model(self):
        self.set_z_value()
        self.calculate_statistics()
        self.calculate_confidence_intervals()

    def return_plot_data(self):

        self.plotdata = self.parameters
        self.plotdata["plot_ci"] = self.intervals["ci"] / 2

        if self.parameters["hypothesis"] == "Äquivalenzhypothese":
            self.plotdata["plot_errorbar_normvalue"] = self.parameters["normvalue"]
            self.plotdata["plot_ci_lower"] = self.intervals["ci_lower"]
            self.plotdata["plot_ci_upper"] = self.intervals["ci_upper"]

        elif self.parameters["hypothesis"] == "Regression zur Mitte":
            self.plotdata["plot_errorbar_normvalue"] = self.statistics["normvalue_regression"]
            self.plotdata["plot_ci_lower"] = self.intervals["ci_lower_regression"]
            self.plotdata["plot_ci_upper"] = self.intervals["ci_upper_regression"]

        return self.plotdata

class ParameterFormular(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.parameterlist = [
        "Reliabilitätskoeffizient",
        "Standardabweichung des Normwertes",
        "Mittelwert des Normwertes",
        "Normwert",
        "Sicherheitswahrscheinlichkeit",
        "Fragestellung",
        "Hypothese"
        ]

        self.input_vars = list()
        self.create(self.parameterlist)

    def create(self,parameterlist):

        for idx,text in enumerate(parameterlist):

            label = ttk.Label(self,text=text)
            label.grid(row=idx,column=0,sticky="W")

            if text == "Reliabilitätskoeffizient":
                var = tk.DoubleVar(self.master)
                element = ttk.Entry(self,justify="right",textvariable=var)

            elif text == "Sicherheitswahrscheinlichkeit":
                var = tk.StringVar(self.master)
                var.set("95%")
                element = ttk.Combobox(self,textvariable=var,values=["99%","95%","90%","80%"])

            elif text == "Fragestellung":
                var = tk.StringVar(self.master)
                var.set("einseitig")
                element = ParameterFormular.createRadiobuttons(self,var,buttonlist=["einseitig","zweiseitig"])

            elif text == "Hypothese":
                var = tk.StringVar(self.master)
                var.set("Äquivalenzhypothese")
                element = ParameterFormular.createRadiobuttons(self,var,buttonlist=["Äquivalenzhypothese","Regression zur Mitte"])

            else:
                var = tk.IntVar(self.master)
                element = ttk.Entry(self,justify="right",textvariable=var)
            
            self.input_vars.append(var)
            element.grid(row=idx,column=1,sticky="EW")

    @staticmethod
    def createRadiobuttons(parent,textvariable,buttonlist):
        frame = tk.Frame(parent)

        for text in buttonlist:

            radiobutton = ttk.Radiobutton(
                frame,
                text=text,
                value=text,
                variable=textvariable,
            )

            radiobutton.pack(anchor="w")

        return frame

    def get_input_values(self):
        return [var.get() for var in self.input_vars]

class Navbar(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.plot_button = ttk.Button(self,text="Plotten")
        self.plot_button.grid(row=0,column=0,sticky="W")

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Konfidenzintervall-Rechner")
        self.master.resizable(0,0)
        self.config_system_icon()

        self.model = Model()
        self.build_view()

    def build_view(self):

        self.parameter_formular = ParameterFormular(self.master)
        self.parameter_formular.pack(side="top",fill="x")

        self.navbar = Navbar(self.master)
        self.navbar.plot_button.configure(command=self.perform_button_action)
        self.navbar.pack(side="bottom",fill="x")

    def update_model(self):
        self.model.set_parameter_values(self.parameter_formular.get_input_values())
        self.model.run_model()

    # FIXME: following an object-oriented approach I originally wanted the plot window to also be a class but I didn't know how to do that
    def callPlotWindow(self,plotdata):

        # turn on interactive mode
        plt.ion()
        
        # if there is already a plot window clear old plot
        if plt:
            plt.clf()

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
        plt.plot(x_normdist,y_normdist)

        # create logical lists which are used for 'where'-argument in fill-between method
        average = (x_normdist >= (plotdata["mean"] - 1 * plotdata["sd"])) & (x_normdist <= (plotdata["mean"] + 1 * plotdata["sd"]))
        above_and_below_average = (x_normdist >= (plotdata["mean"] - 2 * plotdata["sd"])) & (x_normdist <= (plotdata["mean"] - 1 * plotdata["sd"])) | (x_normdist >= (plotdata["mean"] + 1 * plotdata["sd"])) & (x_normdist <= (plotdata["mean"] + 2 * plotdata["sd"]))
        far_above_and_below_average = (x_normdist >= (plotdata["mean"] - 3 * plotdata["sd"])) & (x_normdist <= (plotdata["mean"] - 2 * plotdata["sd"])) | (x_normdist >= (plotdata["mean"] + 2 * plotdata["sd"])) & (x_normdist <= (plotdata["mean"] + 3 * plotdata["sd"]))

        regions = [average,
        above_and_below_average,
        far_above_and_below_average
        ]

        alpha_values = [0.75,0.5,0.25]

        region_labels = [
        "durchschnittlich",
        "unter-/überdurchschnittlich",
        "weit unter-/überdurchschnittlich"
        ]

        # shade regions under curve, use different alpha channel values and labels
        for idx,region in enumerate(regions):
            plt.fill_between(x_normdist, y_normdist,color="C0",alpha=alpha_values[idx],label=region_labels[idx],where=regions[idx])

        # plot confidence interval
        plt.errorbar(x=plotdata["plot_errorbar_normvalue"],y=0,xerr=plotdata["plot_ci"],fmt=".k",capsize=10)

        print("Konfidenzintervall",plotdata["plot_ci"])

        # set x and y axis title
        plt.xlabel(xlabel="Normwert")
        plt.ylabel(ylabel=r'$\phi_{\mu\sigma}(\mathcal{X})$')

        # set plot title
        title = "Normwert: {} Reliabilität: {} Mittelwert: {} Standardabweichung: {} Untere KI-Grenze: {} Obere KI-Grenze: {}".format(
        plotdata["normvalue"],
        plotdata["reliability"],
        plotdata["mean"],
        plotdata["sd"],
        round(plotdata["plot_ci_lower"],2),
        round(plotdata["plot_ci_upper"],2)
        )

        plt.title(label=title,loc="left")

        # create legend
        plt.legend(loc='upper right', prop={'size': 8})

        # change window icon and title
        # TODO: Make sure these methods also work under linux and MAC OS
        window_manager = plt.get_current_fig_manager()
        window_manager.window.wm_iconbitmap("app_icon.ico")
        window_manager.canvas.set_window_title('Konfidenzintervall-Rechner')

    def perform_button_action(self):
        self.update_model()
        self.callPlotWindow(self.model.return_plot_data())

    def config_system_icon(self):
        # application icon (iconbitmap-method doesn't work on linux)
        if sys.platform == "win32":
            tk.Tk.iconbitmap(self.master, "app_icon.ico")
        elif sys.platform == "linux":
            pass

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = Application(root)
    root.mainloop()