import numpy as np
import random

# time limit so that the sim doesn't run endlessly
time_limit = 100000000
# communication time along fiber
c = 2e5


class Task:
    def __init__(self, segment, time):
        self.segments = [segment]
        self.time = time

    def __eq__(self, other):
        return self.time == other.time

    def __gt__(self, other):
        return self.time > other.time

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        return "Task for segment: " + str(self.segments) + " at time: " + str(self.time) + " |"


class Segment:
    def __init__(self, time, occupied):
        self.time = time
        self.occupied = occupied

    def __str__(self):
        return str(self.time)


class QRepeaterStation:
    def __init__(self, q_id):
        self.id = q_id
        self.left_station = None
        self.right_station = None

    def __str__(self):
        return str(self.id)


class QRepSim:
    def __init__(self, segment_number=6, L=20, L_att=22, cut_off=10, coherence_time=1, swap_probability=1,
                 initial_penalty=0):

        self.priority_queue = []
        self.stations = [QRepeaterStation(i) for i in range(segment_number + 1)]

        self.segments = []
        for i in range(segment_number):
            self.segments.append(Segment(-1, False))

        self.L = L
        self.L_att = L_att
        self.swap_probability = swap_probability
        self.initial_penalty = initial_penalty

        self.time_passed = 0
        self.max_time = 50
        self.cut_off = cut_off

        # division by thousand to change to millimeter
        self.coherence_time = coherence_time

        self.time_per_step = self.L / c
        self.tau = self.time_per_step / coherence_time

        self.transmissivity = np.exp(-self.L / self.L_att)

    # direction True = right False = left
    #currently unused, kept for good measure
    def find_furthest_connection(self, segment_index, direction=1):
        temp_station = self.stations[segment_index]
        if direction:
            while temp_station.right_station is not None:
                temp_station = temp_station.right_station
        else:
            while temp_station.left_station is not None:
                temp_station = temp_station.left_station
        return temp_station

    def swap_all(self):
        """
        function that performs all possible swaps at the current time
        :return: None
        """
        for i in range(len(self.segments)):
            if self.segments[i].time >= 0:
                self.swap_possible(i)

    def swap_possible(self, segment_index):
        """
        performs the currently possible swaps according to the new entanglement generated
        :param segment_index: index of segment with new entanglement
        :return: None
        """
        curr_station = self.stations[segment_index]
        left_station = curr_station.left_station
        right_station = curr_station.right_station

        swap_success = True
        # left-side swap
        if left_station is not None:
            # added recently, to check for failure of swap
            swap_success = self.swap(left_station.id)

            if swap_success:
                # if a connection to both sides exists, do a right-side swap as well
                if left_station.right_station.right_station is not None:
                    swap_success = self.swap(left_station.id)
        # right side swap if left-side has not been swapped

        elif right_station is not None:
            if right_station.right_station is not None:
                swap_success = self.swap(curr_station.id)

        return swap_success

    def swap(self, segment_index):
        """
        performs the swapping operation , station at segment_index is leftmost station
        :param segment_index:
        :return: bool: whether or not swap has been successful
        """

        center_station = self.stations[segment_index].right_station
        swap_success = random.random()
        if swap_success <= self.swap_probability:
            self.stations[segment_index].right_station = self.stations[segment_index].right_station.right_station
            self.stations[segment_index].right_station.left_station = self.stations[segment_index]

            self.segments[segment_index].time += self.segments[center_station.id].time

            self.segments[center_station.id].time = 0
            self.segments[center_station.id].occupied = False
            center_station.right_station = None
            center_station.left_station = None

            return True

        else:
            self.discard_current(segment_index)

            return False

    def discard_current(self, station_id):
        """
        discard the entanglement present at the right memory of the current station
        :param station_id: id of station whose ebit has to be discarded
        :return: None
        """
        right_station = self.stations[station_id].right_station
        if right_station is not None:
            if right_station.id < len(self.segments):
                self.segments[right_station.id].occupied = False
        self.discard(station_id)

    def discard(self, segment_index, time_offset=0):
        """
        discards entanglement present at given index, frees up all entanglements in between and reinstates them as tasks
        :param segment_index: index of state to be discarded
        :param time_offset: potential time offset of when the discard process has to occur
        :return: None
        """
        last_connection = segment_index
        for i in range(segment_index + 1, len(self.segments)):
            if (not self.segments[i].occupied) and self.segments[i].time >= 0:
                last_connection = i
            else:
                break
        # plus 1 cuz left connection regarded
        for j in range(segment_index, last_connection + 1):
            self.free_segment(j)

            task_time = np.random.geometric(self.transmissivity, 1)[0] + time_offset - 1
            self.add_task(j, task_time)
            self.priority_queue.sort()

    def discard_above_cut_off(self):
        """
        discards all ebits which have passed the cut_off threshold
        :return: None
        """
        for i in range(0, len(self.segments)):
            if self.segments[i].time > self.cut_off:
                self.discard(i)

    def free_segment(self, segment_index):
        """
        frees up a previously occupied segment
        :param segment_index: index of segment to become unoccupied
        :return: None
        """
        self.segments[segment_index].time = -1
        self.segments[segment_index].occupied = False

        self.stations[segment_index].right_station = None
        self.stations[segment_index + 1].left_station = None

    def entangle(self, segment_index):
        """
        creates an entanglement at a given segment
        :param segment_index: index of segment
        :return: True
        """
        # segment index of segment
        self.segments[segment_index].time = 0
        self.segments[segment_index].occupied = True

        self.stations[segment_index].right_station = self.stations[segment_index + 1]
        self.stations[segment_index + 1].left_station = self.stations[segment_index]

        return True

    # TODO CHECK AND STUFF
    def discard_future(self):
        """
        discards states which would exceed the cutoff before the next entanglement
        :return: None
        """
        time_step = self.priority_queue[0].time
        for i in range(len(self.segments)):
            if self.segments[i].time >= 0 and self.cut_off < self.segments[i].time + time_step:
                self.discard(i, (self.cut_off + 1) - self.segments[i].time)

    def update_segment_time(self, time_step, exception_indices):
        """
        increases the time of each entanglement pair according to the new time step
        :param time_step: size of time step
        :param exception_indices: indices of current new entanglement to handle as exception
        :return: None
        """
        for i in range(len(self.segments)):

            # don't update current task
            if i in exception_indices:
                continue
            # if entanglement has been generated, increase time passed
            if self.segments[i].occupied and self.segments[i].time >= 0:
                self.segments[i].time += time_step

    def entanglement_task(self):
        """
        performs most recent entanglement task
        :return: the task performed
        """
        task = self.priority_queue.pop(0)

        for segment in task.segments:
            self.entangle(segment)
            # set to initial penalty, 0 by default
            self.segments[segment].time = self.initial_penalty

        return task

    def update_task_times(self, time_step):
        """
        updates the individual task times according to the time passed since the new step
        :param time_step: size of time step
        :return: None
        """
        for task in self.priority_queue:
            task.time -= time_step

    def print_segments(self):
        """
        auxiliary print function for segments of class
        :return: None
        """
        print("[", end="")
        for segment in self.segments:
            print(segment, end=", ")
        print("]")

    def print_queue(self):
        """
        auxiliary print function for prio queue
        :return: None
        """
        for task in self.priority_queue:
            print(task)

    def linear_distribution_loop(self):
        """
        loop for a linear entanglement protocol, if entanglements aren't generated at the same time at all segments.
        First segment generates entanglement first, after success the second etc...
        :return: fidelity of the ebit generated
        """
        # set for first entanglement at 01
        curr_segment = 0
        while curr_segment < len(self.segments):
            # sample being drawn with -1, corresponds to the extra step for entanglement
            time = np.random.geometric(self.transmissivity, 1) - 1
            # increase time passed only for first segment, since swapping is ASAP and time will be accumulated
            # on the starting point only
            if self.segments[0].occupied:
                self.segments[0].time += time[0]
            self.time_passed += time[0]

            # entangle step
            self.entangle(curr_segment)
            self.print_segments()
            # set to initial penalty, 0 by default
            self.segments[curr_segment].time = self.initial_penalty

            # reset if swap unsuccessful

            # swap step
            self.update_segment_time(1, [])
            self.time_passed += 1
            if not self.swap_possible(curr_segment):
                self.discard(0)
                curr_segment = 0
                continue

            if self.segments[0].time > self.cut_off:
                self.discard(0)
                curr_segment = 0
                continue

            # temporary, because prio queue not needed for linear distribution
            self.priority_queue = []

            curr_segment += 1
            self.print_segments()
            # break if time exceeds limit
            if self.time_passed > time_limit:
                return 0

        return self.fidelity(self.segments[0].time)

    def find_time_in_queue(self, time):
        """
        checks whether or not a time step already exists within the priority queue
        :param time:
        :return: time if found, -1 if not found
        """
        if self.priority_queue:
            for i in range(len(self.priority_queue)):
                if self.priority_queue[i].time == time:
                    return i
        return -1

    def add_task(self, segment, time):
        """
        adds a task to the appropriate spot in the priority queue
        :param segment: segment to be added
        :param time: timestamp for segment
        :return: True if appended to existing task, False if new task created
        """
        same_time_index = self.find_time_in_queue(time)
        if same_time_index > -1:
            self.priority_queue[same_time_index].segments.append(segment)
            return True
        else:
            self.priority_queue.append(Task(segment, time))
            return False

    def event_loop(self):
        """
        main event loop
        creates initial entanglement times for each segment and then starts the execution of the simulation
        all segments equally likely to generate an entanglement
        :return: fidelity of the ebit generated
        """
        time = np.random.geometric(self.transmissivity, len(self.segments))

        # minus 1 to account for time step 0
        for i in range(len(time)):
            self.add_task(i, time[i] - 1)

        self.priority_queue.sort()
        while self.priority_queue:

            task = self.entanglement_task()
            time_step = task.time

            self.update_task_times(time_step)
            self.time_passed += time_step
            self.update_segment_time(time_step, task.segments)

            # discarding
            self.discard_above_cut_off()

            # next time step for swaps
            self.next_swaps()

            # break if time exceeds limit
            if self.time_passed > time_limit:
                return 0
        return self.fidelity(self.segments[0].time)

    def fidelity(self, time_spent):
        """
        calculates the fidelity of a state according to accumulated time spent in memory
        :param time_spent: time parameter
        :return: float: fidelity
        """
        return 0.5 * (1 + np.exp(- self.tau * time_spent))

    def next_swaps(self):
        """
        performs the swaps 1 time step later
        :return: None
        """
        self.update_task_times(1)
        self.time_passed += 1
        self.update_segment_time(1, [])
        self.discard_above_cut_off()
        self.swap_all()
        if self.priority_queue:
            self.discard_above_cut_off()
            self.discard_future()
