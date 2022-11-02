"""
Search termination conditions
"""

class TerminalCondition:
    """
    Condition object
    """
    def __init__(self) -> "TerminalCondition":
        self.calls = 0
        
    def clear(self):
        self.calls = 0

    def test(self, **kwargs):
        """
        Returns:
            boolean: true if a condition was satisfied
        """
        return kwargs["default"]

class ResultMatchCondition(TerminalCondition):
    """
    Tests for expected and actual result matching
    True while results match
    """
    def __init__(self, expected_result) -> "ResultMatchCondition":
        TerminalCondition.__init__(self)
        self.expected_result = expected_result

    def test(self, **kwargs):
        self.calls += 1
        return not self.expected_result == kwargs["result"]
    
    def __repr__(self) -> str:
        return "{}, termination on: {}".format(self.__name__,self.expected_result)

class NoImporvementCondition(TerminalCondition):
    """
    Tests for number off runs with no improvement in solution
    """
    def __init__(self, count) -> "NoImporvementCondition":
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

    def __repr__(self) -> str:
        return "{}, termination on: {} ineffective calls".format(self.__name__,self.max_ineffective_results)

class LoopCondition(TerminalCondition):
    """
    Loop termination condition
    """
    def __init__(self, counter) -> "LoopCondition":
        TerminalCondition.__init__(self)
        self.counter = counter

    def test(self, **kwargs):
        if self.calls < self.counter:
            self.calls += 1
            return True
        return False
    
    def __repr__(self) -> str:
        return "{}, termination on: {} calls".format(__name__,self.counter)
