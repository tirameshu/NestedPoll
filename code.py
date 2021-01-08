"""
Contains logic of nested poll
Interactive CLI
"""

# Global messages
duplicate_option_msg = "Option already exists!\n"
option_added_msg = "Option added successfully!\n"
enquire_parent_option_msg = "Please enter parent option to nest under.\n"
option_no_exist_msg = "Option does not exist!\n"
must_have_one_child_msg = "Parent options must have at least one child!\n"

def prompt(msg):
    # send msg to user and expects reply
    reply = input(msg)
    # add timeout???? TODO
    return reply

class Poll():
    def __init__(self):
        self.name = ""
        self.options = {} # {option1: { option1.1: vote1.1, option1.2: vote1.2 } ... }

    def add_option(self, layer, option): # returns msg
        if not layer: # layer = 0
            if option in self.options:
                return duplicate_option_msg

            self.options[option] = {} # parent always has a child
            return option_added_msg

        # ask for parent option to nest under
        parent_option = prompt(enquire_parent_option_msg)
        if parent_option not in self.options:
            return option_no_exist_msg

    def visualise_poll(self):
        visual = ""
        index = 1
        for parent_option in self.options:
            visual += "{id}. {op} |".format(id=index, op=parent_option)

            children = self.options[parent_option]
            if len(children) == 0:
                return must_have_one_child_msg
            elif len(children) == 1:
                child = list(children.keys())[0]
                visual += " - {op}: {count}\n".format(op=child, count=children[child])
            else:
                children_options = list(children.keys())
                spaces_needed = visual.index("|") - 1
                padding = " " * spaces_needed

                half = len(children_options) // 2

                top = children_options[:half]
                if len(children_options) % 2: # odd
                    middle = children_options[half]
                    visual += " - {op}: {count}\n".format(op=middle, count=children[middle])
                    bottom = children_options[half+1:]
                else:
                    bottom = children_options[half:]
                lines = ""

                for child in top:
                    line = padding + "| - {op}: {count}\n".format(op=child, count=children[child])
                    lines += line
                visual = lines + visual
                for child in bottom:
                    line = padding + "| - {op}: {count}\n".format(op=child, count=children[child])
                    visual += line



"""
           | - sdfsdfa
           | - sdfsdfa
1. option1 |
           | - sdfsdf
           | - sdfsdf
"""
