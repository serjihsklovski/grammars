class Grammar:
    def __init__(self, *, terminals, non_terminals, starting_non_terminal,
                 transitions, restrictions, **kwargs):

        self._terminals = terminals
        self._non_terminals = non_terminals
        self._starting_non_terminal = starting_non_terminal
        self._transitions = transitions
        self._restrictions = restrictions
        self._name = kwargs.get('name', 'unknown')
