import tkinter
from execute_functions import *

title = "Quantum Repeater Simulation"
pad = 10


width = 350
height = 750
param_column = 1
color = "light grey"
popup_window = None
Y_Options = [
    "bb84 secret key rate",
    "average fidelity",
    "raw rate"
]
X_Options = [
    "cut off",
    "segment length",
    "segment number",
]
on = True

# temporary help bar
'''
def help():
    newWindow = tkinter.Toplevel(main)
    newWindow.title("help")
    newWindow.geometry("400x400")
    line = tkinter.Label(newWindow, text="In the enter : ", bg=color)
    line.pack()
'''

main = tkinter.Tk()
main.title(title)
main.configure(bg='light gray')
main.geometry(str(width) + "x" + str(height))
main.config(cursor="arrow")

def check_parameters():
    '''
    checks whether or not all parameters have been filled
    :return: list of parameters not filled
    '''
    empty_inputs = []
    # type checks
    if str(variable_x.get()) == "cut off":
        try:
            int(nr_segments.get())
        except ValueError:
            empty_inputs.append("Number of segments")
        try:
            float(L.get())
        except ValueError:
            empty_inputs.append("Length")

    if str(variable_x.get()) == "segment length":
        try:
            int(nr_segments.get())
        except ValueError:
            empty_inputs.append("Number of segments")
        try:
            float(cut_off.get())
        except ValueError:
            empty_inputs.append("cut off")

    if str(variable_x.get()) == "segment number":
        try:
            float(L.get())
        except ValueError:
            empty_inputs.append("Length")
        try:
            float(cut_off.get())
        except ValueError:
            empty_inputs.append("cut off")
    try:
        float(L_att.get())
    except ValueError:
        empty_inputs.append("Attenuation length")

    try:
        float(coherence_time.get())
    except ValueError:
        empty_inputs.append("coherence_time")

    try:
        float(swap_probability.get())
    except ValueError:
        empty_inputs.append("swap probability")

    try:
        int(initial_penalty.get())
    except ValueError:
        empty_inputs.append("initial penalty")

    try:
        int(x_min.get())
    except ValueError:
        empty_inputs.append("minimal value for x axis")

    try:
        int(x_max.get())
    except ValueError:
        empty_inputs.append("maximal value for x axis")

    try:
        int(e_bits.get())
    except ValueError:
        empty_inputs.append("ebits per simulation")

    return empty_inputs

def check_validity():
    """
    checks for the validity of the input
    :return: list of invalid inputs
    """
    invalid_inputs = []

    if str(variable_x.get()) != "segment number":
        if int(nr_segments.get()) < 1:
            invalid_inputs.append("amount of segments has to be a positive integer")
    if str(variable_x.get()) != "segment length":
        if float(L.get()) <= 0:
            invalid_inputs.append("Length has to be a positive integer")
    if float(L_att.get()) < 1:
        invalid_inputs.append("Attenuation length has to be a positive value")
    if str(variable_x.get()) != "cut off":
        if cut_off.get() < initial_penalty.get():
            invalid_inputs.append("cut off has to be a positive integer and larger than the initial penalty")
    if not 0 <= float(swap_probability.get()) <= 1:
        invalid_inputs.append("swap probability has to be a value in between 0 and 1")
    if int(initial_penalty.get()) < 0:
        invalid_inputs.append("initial penalty has to be at least 0")
    if int(x_min.get()) < 1:
        invalid_inputs.append("minimal value for x axis has to be a positive integer")
    if int(x_max.get()) < int(x_min.get()):
        invalid_inputs.append("maximal value for x axis has to be an integer larger than the minimal value")
    if int(e_bits.get()) < 1:
        invalid_inputs.append("ebits distributed has to be a positive integer")

    if lin_distribution_eval():
        if str(variable_x.get()) == "cut off":
            if int(x_min.get()) < 2*int(nr_segments.get()) + 1:
                invalid_inputs.append("for linear distribution, a higher cutoff is required")
        else:
            if cut_off.get():
                if int(cut_off.get()) < 2*int(nr_segments.get()) + 1:
                    invalid_inputs.append("for linear distribution, a higher cutoff is required")
    return invalid_inputs




def pop_up (errors, missing):
    """
    function to pop up if some parameters are missing or invalid
    :param errors: list of errors
    :param missing: bool to check whether or not errors are missing parameters or invalid ones
    :return:
    """
    popup_window = tkinter.Toplevel()
    popup_window.title("Invalid parameters")
    popup_window.geometry(str(width) + "x" + str(height//2))
    if(missing):
        tkinter.Label(popup_window, text="These parameters are missing:",font=('Helvetica', 12, 'bold')).grid(row=0, pady=pad, padx=pad)
    else:
        tkinter.Label(popup_window, text="These inputs are invalid:", font=('Helvetica', 12, 'bold')).grid(row=0,
                                                                                                               pady=pad,
                                                                                                               padx=pad)
    for i in range(len(errors)):
        tkinter.Label(popup_window, text=errors[i]).grid(row=i+1, pady=pad, padx=pad)
    popup_window.grab_set()



def lin_distribution_eval():
    """
    checks for linear distribution
    :return: bool
    """
    if lin_distribution.get() == "False":
        return False
    if lin_distribution.get() == "True":
        return True


is_active = True
def check_then_simulate():
    """
    checks the parameters and the runs the simulation
    :return: None
    """
    inputs = check_parameters()
    global is_active
    if is_active:
        if inputs:
            pop_up(inputs, True)
        else:
            inputs = check_validity()
            if check_validity():
                pop_up(inputs, False)
            else:
                is_active = False
                start['state'] = "disabled"
                main.update()
                simulate()
                start['state'] = "normal"
                main.update()

    else:
        is_active = True




def simulate():
    """
    simulates the environment with the given parameters, then plots the results
    :return: True
    """
    x_range = [i for i in range(int(x_min.get()), int(x_max.get()))]
    results = [0 for i in range(len(x_range))]

    # get the desired y parameter
    y_option = int(Y_Options.index(str(variable_y.get())))
    if str(variable_x.get()) == "cut off":
        results = simulation_run_cut_off(int(e_bits.get()), int(nr_segments.get()), float(L.get()), float(L_att.get()),
                                         x_range,
                                         float(coherence_time.get()), float(swap_probability.get()),
                                         int(initial_penalty.get()), lin_distribution_eval(), result_type=y_option)
    if str(variable_x.get()) == "segment length":
        results = simulation_run_length(int(e_bits.get()), int(nr_segments.get()), x_range, float(L_att.get()),
                                        int(cut_off.get()),
                                        float(coherence_time.get()), float(swap_probability.get()),
                                        int(initial_penalty.get()), lin_distribution_eval(), result_type=y_option)
    if str(variable_x.get()) == "segment number":
        results = simulation_run_segments(int(e_bits.get()), x_range, float(L.get()), float(L_att.get()),
                                          int(cut_off.get()),
                                          float(coherence_time.get()), float(swap_probability.get()),
                                          int(initial_penalty.get()), lin_distribution_eval(), result_type=y_option)

    # currently unused, kept if necessary, add att_length and coherence time to options
    """
    if str(variable_x.get()) == "coherence time":
        results = simulation_run_coherence_time(int(e_bits.get()), int(nr_segments.get()), float(L.get()), float(L_att.get()),
                                                int(cut_off.get()),
                                                x_range, float(swap_probability.get()),
                                                int(initial_penalty.get()), lin_distribution_eval(),
                                                result_type=y_option)
    
    if (str(variable_x.get()) == "attenuation length"):
        results = simulation_run_att_length(100, int(nr_segments.get()), float(L.get()), x_range, int(cut_off.get()),
                                         float(coherence_time.get()), float(swap_probability.get()),
                                         int(initial_penalty.get()),  lin_distribution_eval(), result_type=y_option)
    """
    plt.scatter(x_range, [x for x in results])
    if str(variable_x.get()) == "segment length":
        plt.xlabel("segment length(km)")
    else:
        plt.xlabel(str(variable_x.get()))
    plt.ylabel(str(variable_y.get()))
    plt.show(block = False)

    return True


'''
basic parameter input
'''


parameter_frame = tkinter.LabelFrame(main, text="Please enter the desired parameters: ", bg=color)
parameter_frame.grid(row=0, column=0, rowspan=2, columnspan=10, sticky='NS', pady=pad, padx=pad)

tkinter.Label(parameter_frame, text="Number of segments: ", bg=color).grid(row=1, column=0, pady=pad)
nr_segments = tkinter.Entry(parameter_frame)
nr_segments.grid(row=1, column=param_column, pady=pad, padx=pad)

tkinter.Label(parameter_frame, text="Length: ", bg=color).grid(row=2, pady=pad, padx=pad)
L = tkinter.Entry(parameter_frame)
L.grid(row=2, column=param_column, pady=pad, padx=pad)

tkinter.Label(parameter_frame, text="Attenuation length: ", bg=color).grid(row=3, pady=pad, padx=pad)
L_att = tkinter.Entry(parameter_frame)
L_att.grid(row=3, column=param_column, pady=pad, padx=pad)

tkinter.Label(parameter_frame, text="cut off: ", bg=color).grid(row=4, pady=pad, padx=pad)
cut_off = tkinter.Entry(parameter_frame)
cut_off.grid(row=4, column=param_column, pady=pad, padx=pad)

tkinter.Label(parameter_frame, text="coherence time: ", bg=color).grid(row=5, pady=pad, padx=pad)
coherence_time = tkinter.Entry(parameter_frame)
coherence_time.grid(row=5, column=param_column, pady=pad, padx=pad)

tkinter.Label(parameter_frame, text="swap probability: ", bg=color).grid(row=6, pady=pad, padx=pad)
swap_probability = tkinter.Entry(parameter_frame)
swap_probability.grid(row=6, column=param_column, pady=pad, padx=pad)

tkinter.Label(parameter_frame, text="initial penalty: ", bg=color).grid(row=7, pady=pad, padx=pad)
initial_penalty = tkinter.Entry(parameter_frame)
initial_penalty.grid(row=7, column=param_column, pady=pad, padx=pad)

tkinter.Label(parameter_frame, text="linear distribution? ", bg=color).grid(row=8, column=0, pady=pad, padx=pad)

lin_distribution = tkinter.StringVar(parameter_frame)
lin_distribution.set("False")
linear_distribution = tkinter.OptionMenu(parameter_frame, lin_distribution, "False", "True")
linear_distribution.grid(row=8, column=1, pady=pad, padx=pad)

'''
for choosing the axis parameters
'''
axis_frame = tkinter.LabelFrame(main, text="Set axes: ", bg="light grey")
axis_frame.grid(row=9, column=0, rowspan=2, columnspan=10, sticky='NS', pady=pad, padx=pad)

tkinter.Label(axis_frame, text="y-axis parameter:", bg=color).grid(row=0, column=1, pady=pad, padx=pad)

variable_y = tkinter.StringVar(axis_frame)
variable_y.set(Y_Options[0])
yAxis = tkinter.OptionMenu(axis_frame, variable_y, *Y_Options)
yAxis.grid(row=1, column=1, pady=pad, padx=pad)

tkinter.Label(axis_frame, text="x-axis parameter", bg=color).grid(row=0, column=0, pady=pad)

variable_x = tkinter.StringVar(axis_frame)
variable_x.set(X_Options[0])
xAxis = tkinter.OptionMenu(axis_frame, variable_x, *X_Options)
xAxis.grid(row=1, column=0, pady=pad, padx=pad)

tkinter.Label(axis_frame, text="minimal value for x-axis: ", bg=color).grid(row=2, column=0, pady=pad, padx=pad)
x_min = tkinter.Entry(axis_frame)
x_min.grid(row=3, column=0, pady=pad, padx=pad)

tkinter.Label(axis_frame, text="maximal value for x-axis: ", bg=color).grid(row=4, column=0, pady=pad, padx=pad)
x_max = tkinter.Entry(axis_frame)
x_max.grid(row=5, column=0, pady=pad, padx=pad)

tkinter.Label(axis_frame, text="ebits per simulation: ", bg=color).grid(row=3, column=1, pady=pad, padx=pad)
e_bits = tkinter.Entry(axis_frame)
e_bits.grid(row=4, column=1, pady=pad, padx=pad)

"""
default button for testing
default_start = tkinter.Button(main,  text="Default run", bg="green", fg="black", command=default_sim,
                          font=("DejaVu", "18", "bold"))
default_start.grid(row=6, column=2)
"""
is_active = True
start = tkinter.Button(main, text="Run simulation", bg="dimgray", fg="black", command=check_then_simulate,
                       font=("DejaVu", "18", "bold"))
start.grid(row=15, column=4)

main.mainloop()
