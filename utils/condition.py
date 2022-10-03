"""

"""

class TerminalCondition:
    """
    Condition object
    """
    def __init__(self):
        self.calls = 0

    def test(self, **kwargs):
        """
        Returns true while a condition is satisfied
        """
        return True

class ResultMatchCondition(TerminalCondition):
    """
    Tests for expected and actual result matching
    True while results match
    """
    def __init__(self, expected_result):
        TerminalCondition.__init__(self)
        self.expected_result = expected_result

    def test(self, **kwargs):
        self.calls += 1
        return not self.expected_result == kwargs["result"]

class NoImporvementCondition(TerminalCondition):
    """
    Tests for number off runs with no improvement in solution
    """
    def __init__(self, count):
        TerminalCondition.__init__(self)
        self.ineffective_results_count = count
        self.max_ineffective_results = count
        self.current_solution = None

    def test(self, **kwargs):
        self.calls += 1
        if self.current_solution != kwargs["result"]:
            self.ineffective_results_count = self.max_ineffective_results
            self.current_solution = kwargs["result"]
        self.ineffective_results_count -= 1

        if self.ineffective_results_count <= 0:
            return False
        return True


class LoopCondition(TerminalCondition):
    """
    Loop termination condition
    """
    def __init__(self, counter):
        TerminalCondition.__init__(self)
        self.counter = counter

    def test(self, **kwargs):
        if self.calls < self.counter:
            self.calls += 1
            return True
        return False
