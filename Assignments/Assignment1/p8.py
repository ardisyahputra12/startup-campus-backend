"""
Calculate through commands. [WEIGHT = 2]

Given two inputs:
- v: an integer between -1000 and 1000 (inclusive)
- commands: a list of strings representing command (0 <= len(command) <= 10)

Calculate the outcome of processing v through all commands in order.

List of commands with their meanings (X is always an integer, -10 < X < 10):
- add X: add current value with X
- mul X: multiple current value with X
- sub X: subtract current value with X
- reset: reset current value to initial value (v)
- stop: stop the process and return the current value

If there is no commands, returns v (as if it is not processed).

Examples
------------------------------------
Input: v = 8, commands: ["mul 2", "sub 4"]
Output: 12
Explanation:
- initial value = 8 
- step 1: mul 2 => 8 * 2 = 16
- step 2: div 4 => 16 - 4 = 12
------------------------------------
Input: v = 2, commands: ["add 3", "reset", "sub 2"]
Output: 0
Explanation:
- initial value = 2 
- step 1: add 3 => 2 + 3 = 5
- step 2: reset => reset value to 2
- step 3: sub 2 => 2 -2 = 0
-------------------------------------
Input: v = -10, commands: ["mul -3", "stop", "sub 2", "add -5"]
Output: 30
Explanation:
- initial value = -10
- step 1: mul -3 => -10 * -3 = 30
- step 2: stop => return current value (30)
-------------------------------------
"""


def calculate_through_commands(v: int, commands: list) -> int:
    """
    HINTS:
    - create a variable to represent current value, initialized equal to v
    - iterate through each command
        - for each command, separate the string operator (e.g. "add", "reset")
          and the integer X (if applicable)
        - process current value according to the operator, if operator is
          "add" and X = 5, then add current value with 5
        - note that operator "reset" doesn't have a number
    """
    pass
