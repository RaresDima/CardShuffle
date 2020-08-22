import random

from enum import Enum

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

############################
############################


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

    def __init__(self,
                 step: int = 1,
                 break_frequency: int = float('inf'),
                 new_stack_template = 'CREATE NEW STACK',
                 add_to_stack_template = 'ADD CARD TO STACK %i',
                 combine_stacks_template = 'PLACE STACK %i OVER STACK %j'):

        self.step = step
        self.break_frequency = break_frequency

        self.new_stack_template = new_stack_template
        self.add_to_stack_template = add_to_stack_template
        self.combine_stacks_template = combine_stacks_template

    def new_stack(self):
        print(f'{self.step:>3}) ', self.new_stack_template)
        self._increment_step()

    def add_to_stack(self, i: int):
        print(f'{self.step:>3}) ', self.add_to_stack_template.replace('%i', f'{i}'))
        self._increment_step()

    def combine_stacks(self, i: int, j: int):
        print(f'{self.step:>3}) ', self.combine_stacks_template.replace('%i', f'{i}').replace('%j', f'{j}'))
        self._increment_step()

    def _increment_step(self):
        if self.step % self.break_frequency == 0:
            print()
        self.step += 1


NUM_CARDS = int(input('How many cards? '))

print()

deck = Stack(range(NUM_CARDS, 0, -1))

final_shuffle = deck.copy()
random.shuffle(final_shuffle)

step_printer = StepPrinter(break_frequency = BLANK_LINE_EVERY_N_INSTRUCTIONS,
                           new_stack_template = NEW_STACK_INSTRUCTION_TEMPLATE,
                           add_to_stack_template = ADD_CARD_TO_STACK_INSTRUCTION_TEMPLATE,
                           combine_stacks_template = PLACE_STACK_ON_TOP_OF_OTHER_STACK_INSTRUCTION_TEMPLATE)

n = 0

stacks = []
while not deck.empty():

    # Get next card.
    current_card = deck.pop()

    # If the current card is the bottom card in the final shuffle then obviously it can't be placed onto any stack.
    current_card_is_bottom_card = final_shuffle.bottom() == current_card
    if current_card_is_bottom_card:
        step_printer.new_stack() ; n+=1
        stacks += [Stack([current_card])]
        continue

    # Otherwise, find if it can be put onto an existing stack.
    card_placed_on_stack = False
    for i, stack in enumerate(stacks, 1):

        # Get the top card of the current stack.
        top_stack_card = stack.peek()

        # Check if the top card of the current stack should be the one below the current card in the final shuffle.
        if final_shuffle.below(current_card) == top_stack_card:
            step_printer.add_to_stack(i) ; n+=1
            stack.push(current_card)
            card_placed_on_stack = True
            break

    # If there is no stack for the current card then it becomes the first card on a new stack.
    if not card_placed_on_stack:
        step_printer.new_stack() ; n+=1
        stacks += [Stack([current_card])]

    # Check if any stacks can be placed on top of each other.
    i = 0
    while i < len(stacks):
        stack = stacks[i]

        stacks_merged = False
        for j, other_stack in enumerate(stacks):

            if other_stack is stack:
                continue

            # Check if the card that should be directly below the bottom of one stack is the top cad of another stack.
            if final_shuffle.below(other_stack.bottom()) == stack.top():
                step_printer.combine_stacks(j+1, i+1)
                stack.push_all(other_stack)
                stacks.remove(other_stack)
                stacks_merged = True
                break

        if not stacks_merged:
            i += 1

result_shuffle = stacks[0]

print('\nDone!')




