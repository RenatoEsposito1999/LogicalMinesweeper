# Minesweeper with Propositional Logic

This project is part of the Artificial Intelligence course at the Master's Degree program in Applied Computer Science (Machine Learning and Big Data) at Parthenope University of Naples. It is based on the code provided by Harvard University, available [here](https://cdn.cs50.net/ai/2020/x/projects/1/minesweeper.zip). The project has been customized to suit my use case and has been further refactored to be more object-oriented. The graphical interface has been minimally modified.

## Table of Contents
- [Introduction](#Goal-of-the-project)
- [Cell class](#cell-class)
- [Minesweeper class](#minesweeper-class)
- [Sentence class](#sentece-class)
- [Knowledge Representation](#knowledge-representation)
- [Agent class](#agent-class)
- [Inference process](#inference-process)
- [Conclusions and future developments](#conclusions-and-future-developments)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)


## Goal of the project
The goal of the project is to implement an **intelligent agent** capable of autonomously playing the *Minesweeper* game using ***propositional logic***. The code base used is the one proposed by Harvard, available at [this link](https://cdn.cs50.net/ai/2020/spring/projects/1/minesweeper.zip).  
The structure of the application, including the user interface (UI), was already provided, however, the implementation of the agent was done entirely by me.

## Introduction to Minesweeper
Minesweeper is a single-player logic game whose goal is to discover all the cells in a grid that do not contain mines.

### Minesweeper Features:
- **Deterministic**: once the mine layout is established, as each move has a predictable outcome based on this layout. However, from the player's perspective, the game can be perceived as non-deterministic due to initial uncertainty and the need to deduce the location of mines without complete information.
- **Partially observable**: the player does not have access to all the information at the beginning of the game, he can only see the cells he has discovered, while the others remain covered. Hidden information must be inferred from the available partial information.
- **Game Environment**: a grid* of hidden cells, some of which contain mines**, each discovered cell shows the number of adjacent mines.
    - '*' 6x6.
    - '**' in total there are 6 mines. 
  

## Propositional Logic
Propositional logic is a branch of logic that deals with *propositions* and their combinations through *logical connectives* such as **AND, OR, NOT**, etc. Through this logic it is possible to represent and manipulate knowledge.

### Components of Propositional Logic


**Propositions**

 Propositions are statements that can be **true** or **false**.
 - Examples of propositions: "Cell (1,1) is a mine".
 - Propositions are usually denoted by capital letters, for example,:\( C_1_1 \).
 
 **Logical Connectives**
 
 Logical connectives are operators used to combine propositions and form more complex logical expressions.
 - **AND (∧)**: The conjunction of two propositions is true only if both propositions are true.
 - **OR (∨)**: The disjunction of two propositions is true if at least one of the propositions is true.
 - **NOT (¬)**: The negation of a proposition is true if the proposition is false.
 - **IMPLIES (→)**: The implication between two propositions is false only if the first proposition is true and the second is false.
 - **IFF (↔)**: The logical equivalence between two propositions is true if both propositions are both true or both false.

**Inference Rules**

In propositional logic, through rules, such as modusponens or inference algorithms, such as **truth tables**, **forward chaining** and **backward chaining**, it is possible to deduce new propositions starting from existing propositions.


## Cell class
The `Cell` class represents a cell within the Minesweeper game, with information about its location, the presence of a mine, and the number of adjacent mines.

**Important note**: in addition to the various `set` and `get` methods, it was necessary to override the functions:

- `__eq__(self, other)`: To compare whether two cells are equal based on their position.
- `__hash__(self)`: to make the cell hashable, allowing it to be used as a key in a dictionary or as an element of a set.

## Minesweeper class


The `Minesweeper` class manages the game i.e. the initialization of the field, the placement of mines and the calculation of the number of mines adjacent to each cell.


## Sentece class

The use of traditional algorithms such as **model checking**, **forward chaining** and **backward chaining** has been avoided due to the high computational complexity associated with the numerous possible combinations in the Minesweeper game.


To show the complexity let's consider this example:
*If we suppose to know that **exactly one** of the eight variables is true*, this gives us a propositional logic sentence like the below:
    
    Or(
        And(A, Not(B), Not(C), Not(D), Not(E), Not(F), Not(G), Not(H)),
        And(Not(A), B, Not(C), Not(D), Not(E), Not(F), Not(G), Not(H)),
        And(Not(A), Not(B), C, Not(D), Not(E), Not(F), Not(G), Not(H)),
        And(Not(A), Not(B), Not(C), D, Not(E), Not(F), Not(G), Not(H)),
        And(Not(A), Not(B), Not(C), Not(D), E, Not(F), Not(G), Not(H)),
        And(Not(A), Not(B), Not(C), Not(D), Not(E), F, Not(G), Not(H)),
        And(Not(A), Not(B), Not(C), Not(D), Not(E), Not(F), G, Not(H)),
        And(Not(A), Not(B), Not(C), Not(D), Not(E), Not(F), Not(G), H)
    )
That is, a complicated expression and here we are assuming that we know that **only one** is a mine, but everything becomes much more complex if we suppose that there are 2,3,4 etc.

### Knowledge Representation
To avoid this complexity, I represent my sentences like this:

    {A, B, C, D, E, F, } = 1

Each sentence is made up of two parts: **a set of neighboring cells** on the grid and a **number** representing exactly how many of these cells are mines.

 - When the number of elements in the set is equal to the number assigned to that set then *we can infer that all the elements are
   mines*. 
 - When the number assigned to the set is 0, then *all elements in the set are not mines*.
  - When the number of elements is different from the number assigned to the set *it's no possible to generate new
   information*.


The `Sentence` class implements this behavior.


## Agent class
The `Agent` class is responsible for implementing the intelligent agent that will infer whether a cell is safe or not and therefore play automatically.


We can consider functions:
 - `mark_safe(self, cell)` and `mark_mine(self, cell)` as **TELL** operations.
 - `make_safe_move(self)` as **ASK** operations.
 - `add_knowledge(self, cell, count)` as the **inference** operation.

## Inference process
In general the sentences in the knowledge base must refer to cells for which we do not yet know whether they are mine or safe cells, this means that, once we know whether a cell is a mine or not, we can update our sentences to simplify them and potentially draw new conclusions.
To insert a new sentence to add to the KB, we must consider two sets, `set1` and `set2` for which we have the number of mines: `number1` and `number2` respectively ,then we can construct the new sentence `set2 - set1 = number2 - number1`.
If we know, for example, that `{A, B, C} = 1` and `{A, B, C, D, E} = 2`, then logically we can infer that `{D, E} = 1`. Using these set operations we can do this.

The **idea** behind this process is to arrive at sentences where the size of the set is equal to the number associated with the set, this means that set is composed of cells that are **definitely mines**, or the number is 0, i.e. the **cells are safe** .

## Conclusions and future developments
The approach used, based on the use of propositional logic to infer the presence of bombs, has proven to be effective and efficient.
By avoiding traditional algorithms such as model checking, forward chaining and backward chaining, which are unusable for problems with high complexity due to combinatorial computation, the agent can perform inference in real time.

A possible improvement could be to use **probability calculation** (based on the number of free cells and information on mine and safe cells) for when the agent has no information on the cells and is therefore forced to make random movements.

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
python runner.py
```
The game interface will launch, and you can start playing by clicking on the cells. The AI will assist you in making logical decisions based on the propositional logic implemented in the game.

## License
This project is licensed under the   Apache License. See the [LICENSE](https://github.com/RenatoEsposito1999/LogicalMinesweeper/blob/main/LICENSE) file for details.
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
python source\minesweeper.py
```
The game interface will launch, and you can start playing by clicking on the cells. The AI will assist you in making logical decisions based on the propositional logic implemented in the game.

## License
This project is licensed under the   Apache License. See the [LICENSE](https://github.com/RenatoEsposito1999/LogicalMinesweeper/blob/main/LICENSE) file for details.
