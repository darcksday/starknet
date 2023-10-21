from termcolor import cprint
from common import CHAINS


def print_input_network(title='Select network', chains_disable=[], add_chains=[]):
    try:
        while True:
            chains_result = list(CHAINS.keys())

            for chain in add_chains:
                chains_result.append(chain)

            for chain in chains_result.copy():
                if chain in chains_disable:
                    chains_result.remove(chain)

            cprint(f'>>> {title}:', 'yellow')
            for index, chain in enumerate(chains_result):
                cprint(f'{index + 1}. {chain.capitalize()}', 'yellow')

            try:
                option_chain = int(input("> "))
            except ValueError:
                option_chain = 0

            if option_chain < 1 or option_chain > len(chains_result) + 1:
                cprint(f'Wrong network. Please try again.\n', 'red')
                continue
            else:
                return chains_result[option_chain - 1]
    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit
