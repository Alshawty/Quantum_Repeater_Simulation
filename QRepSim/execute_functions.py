from RepeaterEnvironment import *
from bb84 import *


def simulation_run_cut_off(runs, segments, L, L_att, cut_off_range, coherence_time, swap_probability=1,
                           initial_penalty=0,
                           lin_distribution=False, result_type=0):
    """
    :param runs: amount of ebits distributed per set of parameter
    :param segments: amount of segments
    :param L: segment length
    :param L_att: attenuation length
    :param cut_off_range: cut off range to be plotted
    :param coherence_time: coherence time in s
    :param swap_probability: probability of a successful swap
    :param initial_penalty: initial penalty in time steps (int)
    :param lin_distribution: bool whether or not linear distribution is desired
    :param result_type: kind of result displayed
    :return: converted results as list
    """
    result = []
    for cut_off in cut_off_range:
        # append tuple with time passed for runs distribution and the average fidelity
        result.append(
            run_multiple_sims(runs, segments, L, L_att, cut_off, coherence_time, swap_probability, initial_penalty, lin_distribution))


    return convert_to_result(result, runs, L / c, result_type)


def simulation_run_length(runs, segments, L_range, L_att, cut_off, coherence_time, swap_probability=1,
                          initial_penalty=0,
                          lin_distribution=False, result_type=0):
    """
    :param runs: amount of ebits distributed per set of parameter
    :param segments: amount of segments
    :param L_range: range of lengths to be plotted
    :param L_att: attenuation length
    :param cut_off: int - cut off
    :param coherence_time: coherence time in s
    :param swap_probability: probability of a successful swap
    :param initial_penalty: initial penalty in time steps (int)
    :param lin_distribution: bool whether or not linear distribution is desired
    :param result_type: kind of result displayed
    :return: converted results as list
    """
    result = []
    for L in L_range:
        # append tuple with time passed for runs distribution and the average fidelity
        result.append(
            run_multiple_sims(runs, segments, L, L_att, cut_off, coherence_time, swap_probability, initial_penalty, lin_distribution))

    final_result = []
    for i in range(len(L_range)):
        final_result.append(single_result(result[i], runs, L_range[i]/c, result_type))
    return final_result
    #return convert_to_result(result, runs, L / c, result_type)

#currently unused
'''
def simulation_run_att_length(runs, segments, L, L_att_range, cut_off, coherence_time, swap_probability=1,
                              initial_penalty=0,
                              lin_distribution=False, result_type=0):
    result = []
    for L_att in L_att_range:
        # append tuple with time passed for runs distribution and the average fidelity
        result.append(
            run_multiple_sims(runs, segments, L, L_att, cut_off, coherence_time, swap_probability, initial_penalty))

    return convert_to_result(result, runs, L / c, result_type)
'''

def simulation_run_segments(runs, segments_range, L, L_att, cut_off, coherence_time, swap_probability=1,
                            initial_penalty=0,
                            lin_distribution=False, result_type=0):
    result = []
    """
    :param runs: amount of ebits distributed per set of parameter
    :param segments_range: range of segment numbers to plot
    :param L: segment length
    :param L_att: attenuation length
    :param cut_off: int, cut off
    :param coherence_time: coherence time in s
    :param swap_probability: probability of a successful swap
    :param initial_penalty: initial penalty in time steps (int)
    :param lin_distribution: bool whether or not linear distribution is desired
    :param result_type: kind of result displayed
    :return: converted results as list
    """
    for segments in segments_range:
        # append tuple with time passed for runs distribution and the average fidelity
        result.append(
            run_multiple_sims(runs, segments, L, L_att, cut_off, coherence_time, swap_probability, initial_penalty, lin_distribution))

    return convert_to_result(result, runs, L / c, result_type)

#currently unused, check for proper range design
def simulation_run_coherence_time(runs, segments, L, L_att, cut_off, coherence_time_range, swap_probability=1,
                                  initial_penalty=0,
                                  lin_distribution=False, result_type=0):
    result = []
    for coherence_time in coherence_time_range:
        # append tuple with time passed for runs distribution and the average fidelity
        result.append(
            run_multiple_sims(runs, segments, L, L_att, cut_off, coherence_time, swap_probability, initial_penalty, lin_distribution))

    return convert_to_result(result, runs, L / c, result_type)



def run_multiple_sims(runs, segments, L, L_att, cut_off, coherence_time, swap_probability=1, initial_penalty=0,
                      lin_distribution=False):
    time_passed = 0
    avg_fidelity = []
    for i in range(runs):

        sim = QRepSim(segments, L, L_att, cut_off, coherence_time, swap_probability, initial_penalty)

        # variable to store state quality
        if lin_distribution:
            avg_fidelity.append(sim.linear_distribution_loop())
        else:
            avg_fidelity.append(sim.event_loop())

        time_passed += sim.time_passed

    return time_passed, np.mean(avg_fidelity)


# function for testing purposes
'''
def analysis_test(runs, segments, L, L_att, cut_off):
    times_avg = []
    times_std = []
    for i in range(runs):
        times = []
        for j in range(runs):
            sim = QRepSim(segments, L, L_att, 1, cut_off)
            times.append(sim.event_loop())

        average = np.mean(times)
        times_avg.append(average)
        times_std.append(np.std(times))

    print(times_avg)
    print(times_std)

    results = []
    for i in range(len(times_avg)):
        results.append((times_avg[i], times_std[i]))

    return results
'''