# CardShuffle

This project came to be because traditional card shuffling methods are either:
- Not very effective (e.g. they need to be repeated a large number of times before the deck of cards has a reasonable chance of being shuffled).
- Damaging do the cards (e.g. the cards are repeatedly and excessively bent).

This project implements an algorithm that generates a random permutation for a deck of `n` cards and then gives step-by-step instructions on how to obtain that shuffle by either placing the cards on stacks or placing existing stacks on top of each other.

# Usage

Simply run the script as you would run any other script (`python card_shuffle.py` for instance). 

You will be asked to input the number of cards to be shuffled.

Then a sequence of instructions will be printed to the console. These instructions are either:
- Place the next card onto a new stack.
- Place the next card onto an existing stack.
- Place an existing stack on top of another existing stack.

Simply take the deck of cards in your hand and follow the instructions by placing the top card from the deck as instructed. 
It is advised to have ample space on the table. A deck of `n` cards will tipically use up to `n/3` stacks simultaneously.

NOTE: When 2 stacks are combined the number of stacks decreases by 1. The indices of the stacks also change.

E.g. You are instructed to place stack 2 over stack 4. After doing this, since stack 2 no longer "exists", the stack that was in the 3rd spot is not stack 2, stack 4 is also stack 3 now and so on. 

The easyest way to remember this is to simply know that `stack i` will always mean the `i-th` stack that is currently on the table.

# Documentation

The `Config` section at the top of `card_shuffle.py` contains the documentation related to customizing the output.
