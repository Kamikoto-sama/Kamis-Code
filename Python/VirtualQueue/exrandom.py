import random
from math import log10 as log


class RandomEvent:
    def __init__(self, max_value, *events):
        self.__max = max_value
        assert log(max_value).is_integer() and log(max_value) > 0, \
            "'max' must be a degree of 10"
        assert len(events) >= 2, "There must be more than 2 events"
        assert len(events) <= max_value, "The event count must be less than max value"
        assert sum(events) == max_value, "The sum of values must be %s" % max_value

        self.grade = [0 for _ in range(max_value)]
        self.events = events
        self.make_grade()

    def make_grade(self):
        event_index = 0
        current_count = 0
        for index in range(self.__max):
            if current_count > self.events[event_index]:
                current_count = 0
                event_index += 1
            self.grade[index] = event_index
            current_count += 1

    def event(self):
        return random.choice(self.grade)
