import numpy as np
import matplotlib.pyplot as plt

'''
this file serves to calculate the analytics of the simulation results
'''

def entropy(p):
    """
    entropy function
    :param p: probability (float in between 0 and 1)
    :return: entropy
    """
    if p == 0:
        return 0
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)


def raw_rate(ebits_distributed, time, time_step):
    """
    calculates the raw rate of the simulation example
    :param ebits_distributed: amount of successfully distributed ebits
    :param time: time passed
    :param time_step: length of time step
    :return: raw rate
    """
    return ebits_distributed / (time * time_step)


def secret_key_rate(time, ebits_distributed, avg_fidelity, time_step):
    """
    calculates the secret key rate
    :param time: time passed
    :param ebits_distributed: amount of successfully distributed ebits
    :param avg_fidelity: average fidelity of the states distributed
    :param time_step: length of a single time step
    :return: secret key rate
    """
    return raw_rate(ebits_distributed, time, time_step) * (1 - entropy(avg_fidelity))


def convert_to_secret_key_rate(results, runs, time_step):
    """
    converts a list of results into secret key rates
    :param results: list of results
    :param runs: amount of successfully distributed ebits
    :param time_step: length of a single time step
    :return: list of secret key rate results
    """
    scr_list = []

    for result in results:
        scr_list.append(secret_key_rate(result[0], runs, result[1], time_step))

    return scr_list


def convert_to_raw_rate(results, runs, time_step):
    """
    converts list of results into raw rates
    :param results: list of results
    :param runs: amount of successfully distributed ebits
    :param time_step: length of a single time step
    :return: raw rates
    """
    raw_rates = []
    for result in results:
        raw_rates.append(raw_rate(runs, result[0], time_step))

    return raw_rates


def convert_to_fidelity(results):
    """
    converts list of results into fidelities
    :param results: list of results
    :return: list of fidelities
    """
    fidelities = []
    for result in results:
        fidelities.append(result[1])

    return fidelities


def single_result(result, runs, time_step, result_id):
    """
    function to calculate a result type for a single result
    :param result: list of results
    :param runs: amount of successfully distributed ebits
    :param time_step: length of a single time step
    :param result_id: type of result 0 = scr, 1 = raw rate, 2 = fidelity
    :return: the result in the desired type
    """
    # bb84
    if result_id == 0:
        return secret_key_rate(result[0], runs, result[1], time_step)
    # raw rate
    if result_id == 1:
        return raw_rate(runs, result[0], time_step)
    # fidelity
    if result_id == 2:
        return result[1]


def convert_to_result(results, runs, time_step, result_id):
    """
    function to calculate a result type for a list of results
    :param results: list of results
    :param runs: amount of successfully distributed ebits
    :param time_step: length of a single time step
    :param result_id: type of result 0 = scr, 1 = raw rate, 2 = fidelity
    :return:the results in the desired type
    """
    # bb84
    if result_id == 0:
        return convert_to_secret_key_rate(results, runs, time_step)
    # raw rate
    if result_id == 1:
        return convert_to_fidelity(results)
    # fidelity
    if result_id == 2:
        return convert_to_raw_rate(results, runs, time_step)

    else:
        print("no valid parameter given")
        return 0


def plot_data(data):
    '''
    function to quickly plot the data
    :param data: data in the form of (time steps, fidelity)
    :return: None
    '''
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    plt.plot(x_val, y_val)
