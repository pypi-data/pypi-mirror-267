from pathlib import Path
import sys
# to include the main lib of the tests
sys.path.append(str(Path(__file__).parent.parent))

from pynodes import Node

if __name__ == '__main__':
    class Person(Node):
        pass

    bob = Person('Bob')
    eve = Person('Eve')
    alice = Person('Alice')

    # Alice is parent of bob and eve
    alice.add_child(bob)
    alice.add_child(eve)

    alice.pretty_print(option = 'id')

