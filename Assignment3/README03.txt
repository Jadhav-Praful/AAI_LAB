CS5205 ADVANCED AI LAB - ALGORITHM COMPARISON TOOL
OVERVIEW

This program is an advanced assignment scheduler designed to evaluate and
compare the performance of three fundamental AI search algorithms:

A\* (A-Star) Search

DFBB (Depth-First Branch and Bound)

DFS (Depth-First Search)

The tool calculates the Earliest Completion Time for a set of tasks under
specific dependency constraints and two distinct scheduling cases:

Case-A: Students can complete at most ONE assignment per day.

Case-B: Students can complete MULTIPLE assignments per day (within
prompt limits).

The comparison is based on the "Node Count" (number of states visited), which
measures the computational efficiency of each search strategy.

FILES INCLUDED

assg03.py : Python source code containing the algorithms and comparison logic.

input.txt : Sample input file (format described below).

README.txt : This documentation.

INPUT FILE FORMAT

The program reads assignment data from a text file. Lines starting with '%'
are ignored.

Format: A <ID> <Prompt_Cost> <Dependency_IDs> 0

Example:
A 1 2 0 % Task 1: Gemini (Odd ID), Cost 2, No Dependencies
A 2 4 1 0 % Task 2: ChatGPT (Even ID), Cost 4, Depends on A1

HOW TO RUN

Usage Syntax:
python assg03.py <input_file> N <num_students> <cost_c1> <cost_c2> --time <K_val>

Arguments:
<input_file> Path to the text file (e.g., input.txt).
N Literal flag indicating student count follows.
<num_students> Total number of students available.
<cost_c1> Cost coefficient for ChatGPT prompts.
<cost_c2> Cost coefficient for Gemini prompts.
--time Mode flag to find earliest completion time.
<K_val> The daily prompt limit per student.

Example Command:
python assg03.py input.txt N 3 10 12 --time 5

ALGORITHM LOGIC & COMPARISON

A\* SEARCH:
Uses the "Critical Path" heuristic. It estimates the remaining time by
calculating the longest dependency chain. It typically explores the
fewest nodes by prioritizing the most promising paths first.

DFBB (DEPTH-FIRST BRANCH & BOUND):
Explores deep into the tree but "prunes" (discards) any path that
already exceeds the length of the best solution found so far. It is
much more efficient than standard DFS.

DFS (DEPTH-FIRST SEARCH):
Exhaustively explores the search space. It serves as the baseline to
demonstrate how pruning and heuristics improve performance.

OUTPUT DESCRIPTION

The program generates a comparison table for both Case-A and Case-B:

Result: The optimal days found (should be identical for all algorithms).

Nodes Visited: The number of search states generated. A lower number
indicates a more efficient algorithm.
