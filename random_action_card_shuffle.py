import random
import itertools

from typing import *

############################
########## CONFIG ##########
############################

# Every N instructions a blank line will be printed.
# This makes the output look cleaner.
BLANK_LINE_EVERY_N_INSTRUCTIONS = 3

# This string will be printed when the current card should be placed onto a
# new stack.
NEW_STACK_INSTRUCTION_TEMPLATE = 'NEW'

# This string will be printed when the current card should be placed onto an
# existing stack. The index (1-based) of the stack can be referred to by using `%i`
ADD_CARD_TO_STACK_INSTRUCTION_TEMPLATE = '%i'

# This string will be printed when an existing stack should be placed on top
# of another existing stack. The index (1-based) of the stack to be placed on
# top can be referred to by using `%i`. The index (1-based) of the stack that
# will be on the bottom can be referred to by using `%j`.
PLACE_STACK_ON_TOP_OF_OTHER_STACK_INSTRUCTION_TEMPLATE = '%i OVER %j'

# This string will be printed when a random number of cards from the bottom of
# the deck should be pulled out and placed on top of the deck.
# In other words just pull some cards from the bottom and add them on top.
PULL_FROM_BOTTOM_INSTRUCTION_TEMPLATE = 'PULL'

# This string will be printed when the existing stacks need to be gathered up
# in a random order to form the final deck.
RANDOM_GATHER_INSTRUCTION_TEMPLATE = 'RANDOM GATHER'

############################
############################

print('\n'
      'Select the number of cards and stacks to use. \n'
      '5 stacks is enough for 50 cards, 10 is enough for 400. \n'
      '')

NUM_CARDS = int(input('Number of cards: '))
MAX_STACKS = int(input('Number of stacks: '))

NEW_STACK_PB = 0.1
ADD_CARD_PB = 0.3
COMBINE_STACKS_PB = 0.02

PULL_FREQUENCY = 0.1


class Stack(list):

    def push(self, item):
        self.append(item)

    def push_all(self, items):
        self.extend(items)

    def peek(self):
        return self[-1]

    def top(self):
        return self.peek()

    def bottom(self):
        return self[0]

    def below(self, item):
        pos = self.index(item)
        return self[pos-1] if pos > 0 else None

    def empty(self) -> bool:
        return len(self) == 0

    def format_deck(self) -> str:
        max_card_size = max(len(str(max(self))), 2)
        return ','.join([str(card).rjust(max_card_size + 2) for card in self])

    def copy(self) -> 'Stack':
        return Stack(super().copy())


class StepPrinter:

    step: int
    break_frequency: int

    new_stack_template: str
    add_to_stack_template: str
    combine_stacks_template: str
    pull_from_bottom_template: str
    random_gather_template: str

    def __init__(self,
                 step: int = 1,
                 break_frequency: int = float('inf'),
                 new_stack_template: str = 'CREATE NEW STACK',
                 add_to_stack_template: str = 'ADD CARD TO STACK %i',
                 combine_stacks_template: str = 'PLACE STACK %i OVER STACK %j',
                 pull_from_bottom_template: str = 'PULL FROM THE BOTTOM',
                 random_gather_template: str = 'GATHER STACKS RANDOMLY'):

        self.step = step
        self.break_frequency = break_frequency

        self.new_stack_template = new_stack_template
        self.add_to_stack_template = add_to_stack_template
        self.combine_stacks_template = combine_stacks_template
        self.pull_from_bottom_template = pull_from_bottom_template
        self.random_gather_template = random_gather_template

    def new_stack(self):
        self._print_with_step_number_and_increment(
            self.new_stack_template)

    def add_to_stack(self, i: int):
        self._print_with_step_number_and_increment(
            self.add_to_stack_template.replace('%i', f'{i}'))

    def combine_stacks(self, i: int, j: int):
        self._print_with_step_number_and_increment(
            self.combine_stacks_template.replace('%i', f'{i}').replace('%j', f'{j}'))

    def pull_from_bottom(self):
        self._print_with_step_number_and_increment(
            self.new_stack_template)

    def random_gather(self):
        self._print_with_step_number_and_increment(
            self.random_gather_template)

    def _print_with_step_number(self, step: str):
        print(f'{self.step:>3}) ', step)

    def _increment_step(self):
        if self.step % self.break_frequency == 0:
            print()
        self.step += 1

    def _print_with_step_number_and_increment(self, step: str):
        self._print_with_step_number(step)
        self._increment_step()


class StackStateTracker:

    deck_size: int
    deck: List[int]

    max_stacks: int
    stacks: List[Stack]

    step_printer: StepPrinter

    def __init__(self, max_stacks: int, deck_size: int, step_printer: StepPrinter = None):

        self.max_stacks = max_stacks
        self.stacks = [None] * max_stacks

        self.deck_size = deck_size
        self.deck = list(range(1, deck_size+1))

        self.step_printer = step_printer

    def create_new_stack(self):
        first_empty_slot = self.stacks.index(None)
        self.stacks[first_empty_slot] = Stack([self.deck.pop()])

        if self.step_printer:
            self.step_printer.new_stack()

    def add_card_to_stack(self):
        stacks = [stack for stack in self.stacks if stack is not None]
        i = random.randrange(0, len(stacks))
        stacks[i].push(self.deck.pop())

        if self.step_printer:
            self.step_printer.add_to_stack(i+1)

    def stack_over_stack(self):
        stacks = [stack for stack in self.stacks if stack is not None]
        i, j = random.sample(range(len(stacks)), 2)
        stack_top, stack_bottom = stacks[i], stacks[j]
        stack_bottom.push_all(stack_top)
        self.stacks[self.stacks.index(stack_top)] = None

        if self.step_printer:
            self.step_printer.combine_stacks(i+1, j+1)

    @property
    def num_stacks(self) -> int:
        return sum(stack is not None for stack in self.stacks)

    def print_stacks(self):
        for i, stack in enumerate(self.stacks, 1):
            print(f'{i:>2}: {stack}')


if __name__ == '__main__':

    step_printer = StepPrinter(break_frequency = BLANK_LINE_EVERY_N_INSTRUCTIONS,
                               new_stack_template = NEW_STACK_INSTRUCTION_TEMPLATE,
                               add_to_stack_template = ADD_CARD_TO_STACK_INSTRUCTION_TEMPLATE,
                               combine_stacks_template = PLACE_STACK_ON_TOP_OF_OTHER_STACK_INSTRUCTION_TEMPLATE,
                               pull_from_bottom_template = PULL_FROM_BOTTOM_INSTRUCTION_TEMPLATE,
                               random_gather_template = RANDOM_GATHER_INSTRUCTION_TEMPLATE)

    stack_state_tracker = StackStateTracker(MAX_STACKS, NUM_CARDS, step_printer = step_printer)

    pull_interval = max(int(NUM_CARDS * 0.1), 5)

    step = 0
    while stack_state_tracker.deck:
        step += 1

        if step % pull_interval == 0 and len(stack_state_tracker.deck) >= 9:

            deck_third_len = len(stack_state_tracker.deck) // 3
            deck_pull_size = random.randint(3, min(deck_third_len, 70))

            middle_pull = stack_state_tracker.deck[-deck_pull_size:].copy()
            del stack_state_tracker.deck[-deck_pull_size:]
            stack_state_tracker.deck = middle_pull + stack_state_tracker.deck

            step_printer.pull_from_bottom()
            continue

        possible_ops = []

        num_stacks = stack_state_tracker.num_stacks

        if num_stacks < stack_state_tracker.max_stacks:
            possible_ops += [stack_state_tracker.create_new_stack] * int(NEW_STACK_PB * 100)

        if num_stacks > 0:
            possible_ops += [stack_state_tracker.add_card_to_stack] * int(ADD_CARD_PB * 100)

        if num_stacks >= 2:
            possible_ops += [stack_state_tracker.stack_over_stack] * int(COMBINE_STACKS_PB * 100)

        random.choice(possible_ops)()

    random.shuffle(stack_state_tracker.stacks)
    shuffled_deck = list(itertools.chain.from_iterable([stack for stack in stack_state_tracker.stacks if stack is not None]))
    step_printer.random_gather()

    print('Done!')

