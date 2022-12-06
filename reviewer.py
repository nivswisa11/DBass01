from enum import Enum

# "Day is an Enum with three members, MONDAY, TUESDAY, and WEDNESDAY."
#
# The first line of the class definition is the same as the first line of any class definition. The second line is where
# the magic happens. It's an Enum class, and it has three members
class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3

print(Day.MONDAY)

print(Day.MONDAY.name)

print(Day.MONDAY.value)