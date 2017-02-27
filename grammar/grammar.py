class Grammar:
    def __init__(self, *, terminals, non_terminals, starting_non_terminal,
                 transitions, restrictions, **kwargs):

        self._terminals = terminals
        self._non_terminals = non_terminals
        self._starting_non_terminal = starting_non_terminal
        self._transitions = transitions
        self._restrictions = restrictions
        self._name = kwargs.get('name', 'unknown')

    def get_name(self):
        return self._name

    def is_word(self, sequence: str) -> bool:
        """
        Is the taken sequence a word?

        :param sequence: str sequence
        :return: bool is a word
        """

        for non_terminal in self._non_terminals:
            if non_terminal in sequence:
                return False

        return True

    def get_terminals_count(self, sequence: str) -> int:
        """
        Counts a number of occurrences of the terminal symbols
        in the sequence.

        :param sequence: sequence
        :return: count of terminal symbols
        """

        res = 0

        for terminal in self._terminals:
            if terminal != '':
                res += sequence.count(terminal)

        return res

    def get_first_non_terminal_index(self, sequence: str) -> int:
        index = len(sequence) - 1

        for non_terminal in sorted(self._non_terminals):
            if non_terminal in sequence:
                new_index = sequence.find(non_terminal)

                if new_index < index:
                    index = new_index

        return index

    def generate_words(self) -> set:
        """
        Generates a set of words for a language.

        :return: set of words
        """

        words = set()
        max_word_length = int(self._restrictions['max-word-length'])

        def _reduce(seq):
            if self.is_word(seq):
                if len(seq) <= max_word_length and seq not in words:
                    words.add(seq)
            else:
                if self.get_terminals_count(seq) <= max_word_length:
                    first_non_terminal = seq[
                        self.get_first_non_terminal_index(seq)]

                    for transition in sorted(
                            self._transitions[first_non_terminal]):
                        _reduce(seq.replace(first_non_terminal, transition))

        for entry_transition in sorted(self._transitions[
                                           self._starting_non_terminal]):
            _reduce(entry_transition)

        return words
