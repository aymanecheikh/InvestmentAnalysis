from argparse import ArgumentParser


"""
Task List
---------------------------------------------------------
- Add parent commands
- Format help output
- Explore prefix characters
- Explore storing prefix characters in a file???
- Set default arguments
- Create a central location that stores ArgParser details
"""


parser = ArgumentParser(
    prog="Playground Interface",
    usage="%(prog)s options (program under construction)",
    description="This program will act as an interface for all my exploratory projects",
    epilog="The point of this is to build my knowledge.",
)

args = parser.parse_args()
