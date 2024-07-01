# Minesweeper with Propositional Logic

This project is part of the Artificial Intelligence course at the Master's Degree program in Applied Computer Science (Machine Learning and Big Data) at Parthenope University of Naples. This project uses the logic implementation made from the book [Artificial Intelligence: A Modern Approach](https://aima.cs.berkeley.edu/), the source code is available [here](https://github.com/aimacode/aima-python), but it is also present in the current repository. <br>
The graphical interface was taken ready-made from [this](https://cdn.cs50.net/ai/2020/spring/projects/1/minesweeper.zip) repository, but has been minimally modified.


## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Background](#background)
- [Knowledge Representation](#Knowledge-Representation)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

This Minesweeper project leverages propositional logic to enhance the classic game experience. The primary goal was to apply concepts from artificial intelligence to a familiar game, utilizing logic-based techniques to improve the decision-making process within the game. This project is part of the curriculum for the AI course at Parthenope University and showcases the integration of AI principles in game development.

## Features

- **Propositional Logic Integration:** Uses propositional logic to solve the Minesweeper game more efficiently.
- **Object-Oriented Design:** Refactored the original code to be more modular and object-oriented, improving maintainability and readability.
- **Enhanced GUI:** The graphical user interface has been slightly modified to enhance the user experience while maintaining the core functionality.

## Background
Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells – where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.

The goal of the game is to flag (i.e., identify) each of the mines. In many implementations of the game, including the one in this project, the player can flag a mine by right-clicking on a cell (or two-finger clicking, depending on the computer).
## Knowledge Representation
The AI's knowledge is represented as the following logical sentence:

{A, B, C, D, E, F, G, H} = 1

where {A, B, C etc.} are a set of cells, and the number 1 is the count of mines among those cells. This representation allows the following inferences to be made, e.g.:

{D, E} = 0 This implies that none of D, E contain mines, i.e. all are safe cells.

{A, B, C} = 3 This implies that all cells A, B, C contain a mine.

Furthermore, in general when we have two sentences where sentence A is a subset of sentence B, a new sentence can be infered:

setB - setA = countB - countA

Hence while playing minesweeper and clicking on cells, logical sentences are added to the AI's knowledge base. Often as a new sentence is added to the knowledge base, further inferences can be made allowing the identification of mines or safe spaces.
## Installation

To get started with this project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/RenatoEsposito1999/LogicalMinesweeper.git
2. Navigate to the project directory:
   ```bash
   cd LogicalMinesweeper
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
## Usage
To run the Minesweeper game, execute the following command:
```bash
python minesweeper.py
```
The game interface will launch, and you can start playing by clicking on the cells. The AI will assist you in making logical decisions based on the propositional logic implemented in the game.

## License
This project is licensed under the   Apache License. See the [LICENSE](https://github.com/RenatoEsposito1999/LogicalMinesweeper/blob/main/LICENSE) file for details.

