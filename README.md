This is the QRepSim project designed to simulate memory based quantum repeater systems under varying parameters.

For usage of the program on a Windows System, using the QRepSim.exe suffices. It is designed to work without any dependencies.

#################################################################

The QRepSim project requires the following libraries to run:

- Numpy
- Matplotlib

The QRepSym.py file will run the program and open the GUI.

################################################################

A short guide for interacting with the GUI:

First enter the desired parameters.
	-"Number of Segments" requires an integer > 0

	-"Length" (measured in km) a float > 0

	-"Attenuation length" requires a float > 0.

	-"cut off" requires an integer > 0

	-"coherence time" requires a float > 0

	-"swap probability" requires a float in between 0 and 1

	-"initial penality" requires an integer > 0 that is lower than the cut off


After that, you can choose the data generated for the plot:

	-"x-axis parameter" offers the three choices "cut off, segment length and segment number"

	- after that you can set the minimum and maximum value displayed by the graph. 

	-"y-axis parameter" offers the choices "bb84 secret key rate, average fidelity and raw rate"

	- ebits per simulation refers to how many entangled states will be distributed between the 2 communicating parties per data point

NOTE: Depending on the parameters chosen, the simulation might run for a longer time. 
It is advised to wait until the plot is displayed, or choose a lower ebit per simulation value.


With a click on Run simulation, the computation starts and will display the results in a plot upon completion. 

If any parameters are missing or invalid, an error message will be displayed.

NOTE: In order to run a second simulation, one has to click the button again to make it usable, then reclick to run the second simulation.
      It is possible to queue multiple simulations after each other by clicking the Button repeatedly.
