from xml.etree import ElementTree


def from_xml(xml_path):
    """
    Parses xml file describing the language grammar.
    Creates a Grammar object and returns it.

    :param xml_path: source xml-file
    :return: Grammar object
    """

    terminals = {''}
    non_terminals = set()
    starting_non_terminal = None
    transitions = {}
    restrictions = {}

    restrictions_names = {'max-word-length'}

    def _parse_terminals(terminals_xml_element):
        for terminal in terminals_xml_element:
            terminals.add(terminal.attrib['value'])

    def _parse_non_terminals(non_terminals_xml_element):
        nonlocal starting_non_terminal

        for non_terminal in non_terminals_xml_element:
            if 'starting' in non_terminal.attrib and (
                        non_terminal.attrib['starting'] == 'true'):

                starting_non_terminal = non_terminal.attrib['value']

            non_terminals.add(non_terminal.attrib['value'])

    def _parse_transitions(transitions_xml_element):
        for transition in transitions_xml_element:
            from_sym = transition.attrib['from']
            to_seq = transition.attrib['to']

            if from_sym not in transitions:
                transitions[from_sym] = []

            transitions[from_sym].append(to_seq)

    def _parse_restrictions(restrictions_xml_element):
        for restriction in restrictions_xml_element:
            if restriction.tag in restrictions_names:
                restrictions[restriction.tag] = restriction.attrib['value']

    tree = ElementTree.parse(xml_path)
    root = tree.getroot()

    actions = {
        'terminals': _parse_terminals,
        'non-terminals': _parse_non_terminals,
        'transitions': _parse_transitions,
        'restrictions': _parse_restrictions,
    }

    for child in root:
        parse_action = actions.get(child.tag, None)

        if parse_action is not None:
            parse_action(child)

    print(terminals)
    print(non_terminals)
    print(starting_non_terminal)
    print(transitions)
    print(restrictions)


def save_words(gram, output_path):
    pass
