# simgui
A simple GUI API (wrapper around PySide2) for Python learners to build simple yet interesting event driven apps.

![a sample GUI app](https://github.com/freemant2000/simgui/raw/main/images/simgui.png)

It provides the following features:
* Create labels, buttons, input fields and comboboxes.
* Respond to events such as button clicks and input text changes.
* Place such widgets on a grid layout easily.
* All is done using simple function calls (no need to understand classes and objects).

With these a Python learner can make GUI apps like: pacman, spade invaders, etc.

## How to use
Here is a sample GUI program.

    from simgui import *

    def on_ready():
        add_label("l1", "Name")
        add_input("i1", right=True)
        add_label("l2", "Job Title")
        add_input("i2", right=True)
        add_combo("cb1", cols=2)
        add_combo_item("cb1", "chicken")
        add_combo_item("cb1", "beef")
        add_combo_item("cb1", "beans")
        add_button("b1", "OK")
        add_button("b2", "Cancel", right=True)

    def on_click_b1():
        set_label_text("l2", 333)

    def on_edited_i1():
        set_input_text("i2", get_input_value("i1")+1)

    def on_index_changed_cb1():
        print(get_combo_text("cb1")+" is selected")

    start()  # must do this to kick start the app with the UI
