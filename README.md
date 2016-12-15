# MFND

## Overview

A no-frills commandline interface program for making to-do lists. Clears all your tasks every night for a fresh start the next day.

- Add tasks with a short description
- Mark tasks as done
- Move tasks around the list and reorder them
- Create tasks as nested sub-tasks with a tree-like structure
- Undo/redo changes made to the list

## Setup

```
# Just clone this repository
git clone https://github.com/mes32/mfnd.git
```

## Starting the Program

```
# Run using Python3
cd mfnd
python3 mfnd
```

## Usage

```
mfnd commands:
    exit               Exit from the program
    help               Display this help screen
    pumpkin <####>     Configure hour-of-day for reset of to-do list
                       Requires 4 digits in 24-hour clock mode (default 0400)
    undo               Undo previous command
    redo               Redo previous undone command

    todo <description>   Add a new task with <description>
    todosub <P> <description>  Add a sub-task under the task at position <P>
    done <P>           Mark the task at <P> as complete
    remove <P>         Delete the task at <P>

    move <P> up        Move task at <P> up one position
    move <P> down      Move task at <P> down one position
    move <P> top       Move task at <P> to top position
    move <P> bottom    Move task at <P> to bottom position

```

## License

The code in this repository is licensed under the [MIT License](./LICENSE).