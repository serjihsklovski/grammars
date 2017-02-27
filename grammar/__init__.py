from xml.etree import ElementTree
from grammar.grammar import Grammar


def from_xml(xml_path) -> Grammar:
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

    if 'name' in root.attrib and root.attrib['name'] != '':
        grammar_name = root.attrib['name']
    else:
        grammar_name = 'unknown'

    return Grammar(
        terminals=terminals,
        non_terminals=non_terminals,
        starting_non_terminal=starting_non_terminal,
        transitions=transitions,
        restrictions=restrictions,
        name=grammar_name
    )


def save_words(gram: Grammar, output_path: str):
    """
    Writes all words of a language, described by the grammar `gram`.

    :param gram: the grammar of a language
    :param output_path: path to the output file
    """

    words = gram.generate_words()

    with open(output_path, 'w') as output:
        print('Words in language of {grammar_name}'
              .format(grammar_name=repr(gram.get_name())), file=output)
        print('It has {words_count} words:\n'.format(words_count=len(words)),
              file=output)

        for word in sorted(words):
            print(word if word != '' else '#eps', file=output)
