# CardShuffle

This project came to be because traditional card shuffling methods are either:
- Not very effective (e.g. they need to be repeated a large number of times before the deck of cards has a reasonable chance of being shuffled).
- Damaging do the cards (e.g. the cards are repeatedly and excessively bent).

This project implements an algorithm that generates a random permutation for a deck of `n` cards and then gives step-by-step instructions on how to obtain that shuffle by either placing the cards on stacks or placing existing stacks on top of each other.

# Usage

## `random_action_card_shuffle.py`

**This is the recommended algorithm to use. It uses much less physical space on the table and takes 30-40% less time to perform.**

Simply run the script as you would run any other script (`python random_action_card_shuffle.py` for instance). 

You will be asked to input the number of cards to be shuffled and the number of stacks to be used.

5 stacks is enough for a standard deck of 52 cards. 10 stacks is enough for massive 400+ card decks.

Then a sequence of instructions will be printed to the console. These instructions are either:
- Place the next card onto a new stack.
- Place the next card onto an existing stack.
- Place an existing stack on top of another existing stack.
- Pull out the bottom cards from the deck and place them on top of the deck (there is no exact number of cards, here is where you also introduce a bit of randomness, try to pull out between a quarter and a third of the cards).

Simply take the deck of cards in your hand and follow the instructions by placing the top card from the deck as instructed. 
It is advised to have ample space on the table. 

At the end you will be instructed to simply gather up the stacks in a random order.

NOTE: When 2 stacks are combined the number of stacks decreases by 1. The indices of the stacks to not change, where one stack disappears an empty slot remains. When instructed to create a new stack, use the first available empty slot.

E.g. You are instructed to place stack 2 over stack 4. After doing this, since stack 2 no longer "exists", the spot on the physical table where stack 2 was is now empty. You can use it next time you are asked to create a new stack.

##### Observations

- The number of steps that are necessary is usually about `1.1 * n` (give or take 10%).

- Due to human error you might forget some instructions or do some instructions multiple times. In this case you will most likely see some instructions near the end that are impossible to complete (e.g. "put stack 5 on top of stack 9" but there are only 7 stacks). I tend to perform these as best I can:
    - If I am out of cards and am instructed to add a card to a stack I just skip that instruction. 
    - If the index of the indicated stack is larger than how many stacks actually exist (e.g. you need to add a card to stack 6 but there are only 4 stacks) I simply use the last stack.

## `card_shuffle.py`

**This algorithm is an older version, it will be harder to perform by hand and take up more table space.**

**Try to use `random_action_card_shuffle.py` instead if you just want a simple way to shuffle cards.**

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

The easiest way to remember this is to simply know that `stack i` will always mean the `i-th` stack that is currently on the table.

##### Observations

- The number of stacks that end up simultaneously existing is usually somewhere between `n/3` and `n/4`.

- The number of steps that are necessary is usually about `1.5 * n` (give or take 10%).

- Due to human error you might forget some instructions or do some instructions multiple times. In this case you will most likely see some instructions near the end that are impossible to complete (e.g. "put stack 5 on top of stack 9" but there are only 7 stacks). I tend to perform these as best I can:
    - If I am out of cards and am instructed to add a card to a stack I just skip that instruction. 
    - If the index of the indicated stack is larger than how many stacks actually exist (e.g. you need to add a card to stack 6 but there are only 4 stacks) I simply use the last stack.
    - If I am left with more than 1 stack at the end of the algorithm I simply place them on top of each other in a random order since usually you dont end up with more than 2-3-4 stacks.


# Documentation

The `Config` section at the top of `card_shuffle.py` and `random_action_card_shuffle.py` contains the documentation related to customizing the output.

