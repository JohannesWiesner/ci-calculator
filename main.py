import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from collections import OrderedDict
import re
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

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
    
    def run(self):
        self.set_z_value()
        self.calculate_statistics()
        self.calculate_confidence_intervals()

    def get_plot_data(self):

        plotdata = self.parameters
        plotdata["plot_ci"] = self.intervals["ci"] / 2

        if self.parameters["hypothesis"] == "Äquivalenzhypothese":
            plotdata["plot_errorbar_normvalue"] = self.parameters["normvalue"]
            plotdata["plot_ci_lower"] = self.intervals["ci_lower"]
            plotdata["plot_ci_upper"] = self.intervals["ci_upper"]

        elif self.parameters["hypothesis"] == "Regression zur Mitte":
            plotdata["plot_errorbar_normvalue"] = self.statistics["normvalue_regression"]
            plotdata["plot_ci_lower"] = self.intervals["ci_lower_regression"]
            plotdata["plot_ci_upper"] = self.intervals["ci_upper_regression"]

        return plotdata

class ParameterFormular(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.parameterlist = [
        "Reliabilitätskoeffizient",
        "Standardabweichung des Normwertes",
        "Normmittelwert",
        "Individueller Normwert",
        "Sicherheitswahrscheinlichkeit",
        "Seitigkeit",
        "Hypothese"
        ]

        self.input_vars = list()

        self.create(self.parameterlist)

    def create(self,parameterlist):

        space = ttk.Frame(self)
        space.grid(row=0,column=1,padx=10)

        for idx,text in enumerate(parameterlist):

            label = ttk.Label(self,text=text,background='#ffffff')
            label.grid(row=idx,column=0,sticky="W")

            var = tk.StringVar(self.master)

            if text == "Reliabilitätskoeffizient":
                var.trace("w",self.validate_unit_interval_input)
                element = ttk.Entry(self,justify="left",textvariable=var)

            elif text == "Sicherheitswahrscheinlichkeit":
                var.set("95%")
                element = ttk.Combobox(self,textvariable=var,state="readonly",values=["99%","95%","90%","80%"])

            elif text == "Seitigkeit":
                var.set("einseitig")
                element = ParameterFormular.create_radiobuttons(self,var,buttonlist=["einseitig","zweiseitig"])

            elif text == "Hypothese":
                var.set("Äquivalenzhypothese")
                element = ParameterFormular.create_radiobuttons(self,var,buttonlist=["Äquivalenzhypothese","Regression zur Mitte"])

            else:
                var.trace("w",self.validate_float_input)
                element = ttk.Entry(self,justify="left",textvariable=var)
            
            self.input_vars.append(var)

            element.grid(row=idx,column=2,sticky="EW")

    @staticmethod
    def create_radiobuttons(parent,textvariable,buttonlist):
        frame = tk.Frame(parent)

        # background keyword argument seems not to exist for ttk.Radiobutton
        s = ttk.Style()
        s.configure('White.TRadiobutton',background='#ffffff')

        for text in buttonlist:

            radiobutton = ttk.Radiobutton(
                frame,
                text=text,
                value=text,
                variable=textvariable,
                style='White.TRadiobutton'
            )

            radiobutton.pack(anchor="w")

        return frame

    def validate_unit_interval_input(self,name,index,mode):
        # allow a number between 0 and 1 or an empty string
        regex = re.compile(r'^0(\.[0-9]*)?$|^1(\.0?)?$|^$')

        for var in self.input_vars:
            if name == str(var):
                if not regex.match(var.get()):
                    var.set(var.get()[:-1])
                    self.master.bell()

    def validate_float_input(self,name,index,mode):
        # allow only floating point numbers or an empty string
        regex = re.compile(r'^[+-]?((\d+\.?\d*)|(\.\d+))$|^$')

        for var in self.input_vars:
            if name == str(var):
                if not regex.match(var.get()):
                    var.set(var.get()[:-1])
                    self.master.bell()

    def check_for_input(self):
        input_check = True
        
        for var in self.input_vars:
            if not var.get():
                input_check = False
        
        return input_check

    def get_input_values(self):
        output_list = [
        float(self.input_vars[0].get()),
        float(self.input_vars[1].get()),
        float(self.input_vars[2].get()),
        float(self.input_vars[3].get()),
        self.input_vars[4].get(),
        self.input_vars[5].get(),
        self.input_vars[6].get()
        ]

        return output_list

class Navbar(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.plot_button = ttk.Button(self,text="Plotten")
        self.plot_button.pack()

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
        self.parameter_formular.pack(side="top",fill="x",padx=5,pady=5)

        self.navbar = Navbar(self.master)
        self.navbar.plot_button.configure(command=self.perform_button_action)
        self.navbar.pack(side="left",fill="x",padx=5,pady=5)

    def update_model(self):
        self.model.set_parameter_values(self.parameter_formular.get_input_values())
        self.model.run()

    # FIXME: following an object-oriented approach I originally wanted the plot window to also be a class but I didn't know how to do that
    def call_plot_window(self,plotdata):

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

        # set x-axis title
        plt.xlabel(xlabel="Skala der Normwerte")

        # don't show y-axis ticks and title
        plt.gca().axes.get_yaxis().set_visible(False)

        # create textbox
        textbox_strings = [
        "Individueller Normwert: {}".format(plotdata["normvalue"]),
        "Untere KI-Grenze: {}".format(round(plotdata["plot_ci_lower"],2)),
        "Obere KI-Grenze: {}".format(round(plotdata["plot_ci_upper"],2)),
        "Reliabilität: {}".format(plotdata["reliability"]),
        "Normmittelwert: {}".format(plotdata["mean"]),
        "Standardabweichung: {}".format(plotdata["sd"])
        ]
        
        sep = '\n'
        textbox_content = sep.join(textbox_strings)

        textbox_props = dict(boxstyle='round',facecolor='white',alpha=0.5)

        # place a text box in upper left in axes coords
        plt.text(0.01, 0.98,textbox_content,fontsize=8,transform = plt.gca().transAxes,verticalalignment='top',bbox=textbox_props)

        # create legend
        plt.legend(loc='upper right', prop={'size': 8})

        # change window icon and title
        # TODO: Make sure these methods also work under linux and MAC OS
        window_manager = plt.get_current_fig_manager()
        window_manager.window.wm_iconbitmap("app_icon.ico")
        window_manager.canvas.set_window_title('Konfidenzintervall-Rechner')

    def perform_button_action(self):
        input_check = self.parameter_formular.check_for_input()

        if input_check:
            self.update_model()
            self.call_plot_window(self.model.get_plot_data())
        else:
            messagebox.showerror("Konfidenzintervall-Rechner","Bitte fülle alle Eingabefelder aus")


    def config_system_icon(self):
        # application icon (iconbitmap-method doesn't work on linux)
        if sys.platform == "win32":
            tk.Tk.iconbitmap(self.master, "app_icon.ico")
            
        elif sys.platform == "linux":
            pass

if __name__ == "__main__":
    root = tk.Tk()

    # change default color
    root.tk_setPalette(background='#ffffff')
    # change default font settings
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=10)
    root.option_add("*Font", default_font)

    my_gui = Application(root)
    root.mainloop()