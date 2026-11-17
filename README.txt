SHIP LOGIC PUZZLE SOLVER
========================

ABOUT THE PROJECT
-----------------

Ship Logic Puzzle Solver is a Python-based desktop application developed using Tkinter. It provides an interactive environment for solving a ship-based logic puzzle by matching different attributes to five ship positions.

The application allows users to solve the puzzle manually or explore an automated step-by-step solution walkthrough to understand how the clues are used to determine the answers.

FEATURES
--------

1. Manual Gameplay
   - Enter answers for five different ship positions.
   - Match ship attributes based on the given clues.
   - Check whether the completed solution is correct.

2. Automated Solver
   - View an automated puzzle solution.
   - Follow the solution through individual deduction steps.
   - Navigate between previous and next steps.

3. Clue Helper
   - View the puzzle clues.
   - Navigate through the clues using previous and next buttons.

4. Solution Validation
   - Verify answers against the puzzle conditions.
   - Receive feedback when the solution is correct or incorrect.

5. Reset Functionality
   - Reset the puzzle to start again.

PUZZLE ATTRIBUTES
-----------------

Each of the five ship positions has five attributes:

- Nationality
- Departure Time
- Cargo
- Chimney Color
- Destination

TECHNOLOGIES USED
-----------------

- Python - Main programming language.
- Tkinter - Graphical User Interface (GUI).
- ttk - Themed GUI widgets.
- tkinter.messagebox - Displaying solution feedback.

PROJECT STRUCTURE
-----------------

ship-logic-puzzle-solver/
|
|-- finalized_game.py
|-- README.md


GETTING STARTED
---------------

PREREQUISITES

- Python 3.x
- Tkinter (included with most standard Python installations)

INSTALLATION

1. Clone the repository:

   git clone https://github.com/YOUR-USERNAME/ship-logic-puzzle-solver.git

2. Navigate to the project directory:

   cd ship-logic-puzzle-solver

3. Run the application:

   python finalized_game.py

On Windows, you can also use:

   py finalized_game.py


HOW TO USE
----------

1. Launch the application.
2. Select one of the available options from the main menu.

   MANUAL PLAY
   - Enter the attributes for each ship position.
   - Use the clue helper (?) to view the puzzle clues.
   - Click "Check Solution" to validate your answers.
   - Click "Reset Game" to start again.

   HOW TO SOLVE
   - Select "How to Solve" from the main menu.
   - Follow the automated deduction steps.
   - Use the Previous Step and Next Step buttons to navigate
     through the solution.


SCREENSHOTS
-----------

Application screenshots will be added here.

- Main Menu
- Manual Gameplay
- Clue Helper
- Step-by-Step Solution


LICENSE
-------

This project was developed for educational purposes.

License and redistribution permissions have not yet been specified.


DEVELOPER
---------

Developed using Python and Tkinter.