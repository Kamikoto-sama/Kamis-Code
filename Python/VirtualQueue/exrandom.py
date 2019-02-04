import random
from math import log10 as log


class RandomEvent:
    def __init__(self, *events, **kwargs):
        self.__max = 100
        if kwargs.get("max", False):
            self.__max = kwargs["max"]

        assert log(self.__max).is_integer() and log(self.__max) > 0, \
            "'max' must be a degree of 10"
        assert len(events) <= self.__max, "The event count must be less than max value"
        assert sum(events) == self.__max, "The sum of values must be %s" % self.__max

        self.grade = [0 for _ in range(self.__max)]
        self.events = events
        self.make_grade()
        if kwargs.get("shuffle", False):
            random.shuffle(self.grade)

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
