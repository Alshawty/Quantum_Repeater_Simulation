from RepeaterEnvironment import *
import pytest


def test_find_furthest_connection():
    Sim = QRepSim(10, 20, 22, 10, 1)

    for i in range(len(Sim.stations) - 1):
        Sim.stations[i].right_station = Sim.stations[i + 1]

    furthest_block = Sim.find_furthest_connection(0)

    assert furthest_block == Sim.stations[-1]
    assert furthest_block.id == 10


# currently not needed
def test_swap_all():
    '''
    Sim = QRepSim(10, 20, 22, 1, 10)

    Sim.segments_time = [-1, 2, -1, 3, 0, 4, 0, -1, 2, 1]
    Sim.occupied = [False, True, False, True, True, True, False, False, True, True]
    Sim.blocks[3].right_block = Sim.blocks[6]
    Sim.blocks[8].right_block = Sim.blocks[9]
    Sim.blocks[8].right_block = Sim.blocks[10]


    Sim.swap_all()

    assert Sim.segments_time == [-1, 2, -1, 7, 0, 0, 0, -1, 3, 0]
    assert Sim.occupied == [False, True, False, True, False, False, False, False, True, False]
    '''
    pass


def test_swap_possible():
    Sim = QRepSim(10, 20, 22, 10, 1)
    Sim.segments = [Segment(-1, False), Segment(2, True), Segment(-1, False), Segment(3, True), Segment(0, True),
                    Segment(4, True), Segment(0, False), Segment(-1, False), Segment(2, True), Segment(1, True)]

    Sim.stations[3].right_station = Sim.stations[5]
    Sim.stations[5].left_station = Sim.stations[3]
    Sim.stations[5].right_station = Sim.stations[6]
    Sim.stations[6].left_station = Sim.stations[5]

    Sim.swap_possible(3)
    time_test = [-1, 2, -1, 7, 0, 0, 0, -1, 2, 1]
    for i in range(len(time_test)):
        assert Sim.segments[i].time == time_test[i]
    occ_test = [False, True, False, True, True, False, False, False, True, True]
    for i in range(len(occ_test)):
        assert Sim.segments[i].occupied == occ_test[i]
    assert Sim.stations[3].right_station == Sim.stations[6] and Sim.stations[5].right_station is None
    assert Sim.stations[6].left_station == Sim.stations[3]


def test_swap():
    Sim = QRepSim(10, 20, 22, 10, 1)
    Sim.segments = [Segment(-1, False), Segment(2, True), Segment(-1, False), Segment(3, True), Segment(0, True),
                    Segment(4, True), Segment(0, False), Segment(-1, False), Segment(2, True), Segment(1, True)]

    Sim.stations[3].right_station = Sim.stations[5]
    Sim.stations[5].left_station = Sim.stations[3]
    Sim.stations[5].right_station = Sim.stations[6]
    Sim.stations[6].left_station = Sim.stations[5]

    Sim.swap(3)

    time_test = [-1, 2, -1, 7, 0, 0, 0, -1, 2, 1]
    for i in range(len(time_test)):
        assert Sim.segments[i].time == time_test[i]
    occ_test = [False, True, False, True, True, False, False, False, True, True]
    for i in range(len(occ_test)):
        assert Sim.segments[i].occupied == occ_test[i]
    assert Sim.stations[3].right_station == Sim.stations[6] and Sim.stations[5].right_station is None
    assert Sim.stations[6].left_station == Sim.stations[3]


def test_discard_current():
    Sim = QRepSim(8, 20, 22, 10, 1)
    Sim.segments = [Segment(11, True), Segment(0, False), Segment(4, True), Segment(10, True), Segment(0, False),
                    Segment(0, False), Segment(0, True), Segment(-1, False)]

    Sim.discard_current(3)
    time_test = [11, 0, 4, -1, -1, -1, 0, -1]
    for i in range(len(time_test)):
        assert Sim.segments[i].time == time_test[i]


def test_discard():
    Sim = QRepSim(8, 20, 22, 10, 1)
    Sim.segments = [Segment(11, True), Segment(0, False), Segment(4, True), Segment(10, True), Segment(0, False),
                    Segment(0, False), Segment(0, True), Segment(-1, False)]

    Sim.discard(3)

    time_test = [11, 0, 4, -1, -1, -1, 0, -1]
    for i in range(len(time_test)):
        assert Sim.segments[i].time == time_test[i]


def test_discard_single():
    Sim = QRepSim(8, 20, 22, 10, 1)

    Sim.segments = [Segment(11, True), Segment(0, False), Segment(4, True), Segment(10, True), Segment(0, False),
                    Segment(0, False), Segment(0, True), Segment(-1, False)]

    Sim.discard(0)
    Sim.discard(3)

    assert (not Sim.segments[0].occupied) and (not Sim.segments[3].occupied)
    assert Sim.segments[0].time == -1 and Sim.segments[3].time == -1
    assert (Sim.stations[0].right_station is None) and (Sim.stations[3].right_station is None) and (
                Sim.stations[3].left_station is None)


def test_entangle():
    Sim = QRepSim(10, 20, 22, 10, 1)

    for i in range(0, len(Sim.stations) - 1, 2):
        Sim.entangle(i)

    assert (Sim.stations[0].right_station == Sim.stations[1]) and (Sim.stations[1].left_station == Sim.stations[0])
    assert (Sim.stations[1].right_station is None) and (Sim.stations[0].left_station is None)

    assert (Sim.stations[8].right_station == Sim.stations[9]) and (Sim.stations[9].left_station == Sim.stations[8])
    assert (Sim.stations[9].right_station is None) and (Sim.stations[8].left_station is None)


def test_entangle_single():
    Sim = QRepSim(10, 20, 22, 10, 1)

    Sim.priority_queue = [Task(2, 2), Task(3, 2), Task(5, 6),
                          Task(8, 8)]

    task_to_check = Sim.priority_queue[0]
    assert Sim.entanglement_task() == task_to_check
    assert Sim.segments[2].time == 0 and Sim.segments[3].time != 0
    assert len(Sim.priority_queue) == 3
    assert Sim.stations[2].right_station == Sim.stations[3]


# function currently unused
def test_find_unoccupied_min():
    pass


def test_discard_above_cut_off():
    Sim = QRepSim(8, 20, 22, 10, 1)
    Sim.segments = [Segment(11, True), Segment(0, False), Segment(4, True), Segment(10, True), Segment(0, True),
                    Segment(9, True), Segment(-1, False), Segment(10, False)]

    Sim.discard_above_cut_off()
    time_test = [-1, -1, 4, 10, 0, 9, -1, 10]
    for i in range(len(time_test)):
        assert Sim.segments[i].time == time_test[i]
    occ_test = [False, False, True, True, True, True, False, False]
    for i in range(len(occ_test)):
        assert Sim.segments[i].occupied == occ_test[i]


def test_discard_future():
    Sim = QRepSim(8, 20, 22, 10, 1)

    Sim.priority_queue = [Task(2, 5), Task(5, 7)]
    Sim.segments = [Segment(3, True), Segment(0, False), Segment(-1, True), Segment(6, True), Segment(0, True),
                    Segment(-1, True), Segment(4, False), Segment(0, False)]
    Sim.discard_future()

    time_test = [3, 0, -1, -1, 0, -1, 4, 0]
    for i in range(len(time_test)):
        assert Sim.segments[i].time == time_test[i]


def test_update_segment_time():
    Sim = QRepSim(8, 20, 22, 10, 1)

    for i in range(0, len(Sim.segments), 2):
        Sim.segments[i] = i
    Sim.segments = [Segment(0, False), Segment(-1, True), Segment(2, True), Segment(-1, False), Segment(4, True),
                    Segment(-1, False), Segment(6, False), Segment(-1, True)]
    Sim.occupied = [False, True, True, False, True, False, False, True]

    Sim.update_segment_time(2, [0])

    assert Sim.segments[0].time == 0 and Sim.segments[2].time == 4 and Sim.segments[4].time == 6 and Sim.segments[
        6].time == 6 and Sim.segments[7].time == -1


def test_entanglement_task():
    Sim = QRepSim(8, 20, 22, 10, 1, initial_penalty=2)
    Sim.priority_queue = [Task(2, 3), Task(3, 3), Task(4, 5)]

    assert Sim.entanglement_task().segments[0] == 2
    assert Sim.stations[2].right_station == Sim.stations[3] and Sim.stations[3].left_station == Sim.stations[2]
    assert Sim.segments[2].time == 2


def test_update_task_times():
    Sim = QRepSim(10, 20, 22, 10, 1)

    Sim.priority_queue = [Task(2, 2), Task(3, 4), Task(5, 6),
                          Task(8, 8)]

    Sim.update_task_times(2)

    assert Sim.priority_queue[0].time == 0 and Sim.priority_queue[1].time == 2 and Sim.priority_queue[2].time == 4 and \
           Sim.priority_queue[3].time == 6


def test_linear_loop():
    Sim = QRepSim(10, 20, 22, 10, 1)

    Sim.event_loop()

    assert not Sim.priority_queue
    assert Sim.segments[0].time >= 0
    assert Sim.segments[5].time == 0


def test_event_loop():
    Sim = QRepSim(10, 20, 22, 10, 1)

    Sim.event_loop()
    assert True
    assert not Sim.priority_queue
    assert Sim.segments[0].time >= 0
    assert Sim.segments[5].time == 0
