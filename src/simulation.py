"""
    File name: simulation.py
    Author: Tor Kristian
    Date created: 07/09/2020
    Date last modified: 28/09/2020
    Python Version: 3.8
"""
from math import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from lib.Algorithms import *
from lib.function_prot import *
from time import sleep


class Simulation:

    def __init__(self, dt, func, mu, update_time, v_ix, v_iy, n, x_lim, y_lim, plot, x, y):
        self.dt = dt
        self.fig = plt.figure()
        self.ax = [0] * 2
        if plot:
            self.ax[0] = self.fig.add_subplot(121, projection='3d')
            self.ax[1] = self.fig.add_subplot(122, projection='3d')
        else:
            self.fault = self.fig.add_subplot(111)
        self.e = Algo(n, mu, self.ax[0], v_ix, v_iy, func, dt, x_lim, y_lim, update_time, plot, x, y)
        self.h = Algo(n, mu, self.ax[1], v_ix, v_iy, func, dt, x_lim, y_lim, update_time, plot, x, y)
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.func = func
        self.v_ix = v_ix
        self.v_iy = v_iy
        self.x = x
        self.y = y

    def simulate(self):
        print("simulation")
        # Using linspace with limts to create the X and Y values
        X = np.linspace(self.x_lim[0], self.x_lim[1], 60)
        Y = np.linspace(self.y_lim[0], self.y_lim[1], 60)
        # Creating a meshgrid with the two linspaces above
        X, Y = np.meshgrid(X, Y)
        fun = function_prot(0.001, self.func)
        # Creating Z using the given function
        Z = fun.f(X, Y)
        # Initializing the plot using a for loop and giving them titles
        titles = ["Forward Euler", "Heun's Method"]
        for i in range(len(self.ax)):
            self.ax[i].plot_wireframe(X, Y, Z, rstride=3, cstride=3)
            self.ax[i].set_title(titles[i])
            self.ax[i].set_xlabel("X-axis")
            self.ax[i].set_ylabel("Y-axis")
            self.ax[i].set_zlabel("Z-axis")

        # Setting a initial value for t and running the while loop forever and plotting every 0.05 seconds
        t = 0
        while True:
            self.e.euler(t)
            self.h.heuns(t)
            t += 1
            plt.pause(self.dt/22)

        plt.show()


    def show_function(self):
        check = self.fig.add_subplot(111, projection='3d')
        # Using linspace with limts to create the X and Y values
        X = np.linspace(self.x_lim[0], self.x_lim[1], 60)
        Y = np.linspace(self.y_lim[0], self.y_lim[1], 60)
        # Creating a meshgrig with the two linspaces above
        X, Y = np.meshgrid(X, Y)
        fun = function_prot(0.001, self.func)
        # Creating Z using the given function
        Z = fun.f(X, Y)
        # Initializing the plot using a for loop and giving them titles
        check.plot_wireframe(X, Y, Z, rstride=3, cstride=3)
        check.set_xlabel("X-axis")
        check.set_ylabel("Y-axis")
        check.set_zlabel("Z-axis")
        print("plotted " + self.func)
        plt.show()

    def plot_fault(self, dt, steps, time_end, x_end, y_end):
        end = time_end / dt  # Sets the total amount of steps needed to reach the end based on time_end and dt
        iterate = 0  # Counts number of iterations to be done within the while loop
        fh = [0] * steps  # Create an array of steps amount of elements
        fe = [0] * steps
        dts = [dt] * steps
        index = 0  # Used to manipulate the array at a certain index
        for i in range(0, steps):
            self.e.re_init(dt, self.v_ix, self.v_iy, self.x, self.y)
            self.h.re_init(dt, self.v_ix, self.v_iy, self.x, self.y)
            while iterate < end - 1:  # iterate untill end - 1
                self.e.euler(iterate)
                self.h.heuns(iterate)
                iterate += 1
            (xe, ye) = self.e.euler(iterate)  # Fetch the last two variables
            (xh, yh) = self.h.heuns(iterate)
            fe[index] = np.sqrt(np.power(x_end - xe, 2) + np.power(y_end - ye, 2))  # Write  the error to an array
            fh[index] = np.sqrt(np.power(x_end - xh, 2) + np.power(y_end - yh, 2))
            dts[index] = dt  # Write the dt used to an array
            dt /= 2
            print(f"FE: {fe[index]}\tFH: {fh[index]}")
            index += 1
            iterate = 0
            end = time_end / dt

        # Plot the values in a loglog plot
        self.fault.loglog(dts, fe, 'bo-', marker="*", linewidth=1, label="Euler")
        self.fault.loglog(dts, fh, 'go-', marker="*", linewidth=1, label="Heun's")
        self.fault.loglog(dts, np.power(dts, 2), 'r--', linewidth=1, label="dt^2")
        self.fault.loglog(dts, dts, 2, 'o--', linewidth=1, label="dt")
        self.fault.set_xlabel("dt")
        self.fault.set_ylabel("Error")
        self.fault.legend()
        plt.show()


if __name__ == "__main__":
    # Run an example simulation to test different
    s = Simulation(0.1, "np.sin(x)+np.cos(y)", 0.1, 1, 1, 1, 3, [1, 10], [1, 10], True, 2, 2)
    s.simulate()
