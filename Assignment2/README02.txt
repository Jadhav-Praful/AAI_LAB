CS5205 Advanced AI Lab - Assignment 2
=====================================

Files Included:
---------------
1. assg02.py      - Python source code for the extended scheduler.
2. README02.txt   - This help file.

Description:
------------
This program extends the assignment scheduler to handle a specific scenario where 
students exchange solutions only at 6:00 AM the next day. This means if a task 
is completed on Day D, it can only be used as a dependency for new tasks starting 
on Day D+1.

The program solves two problems based on command line arguments:
1. Determine the Earliest Completion Time given a fixed prompt limit (K).
2. Determine the Best Subscription (Minimum K) to finish within M days.

How to Run:
-----------
Prerequisites: Python 3.x

The program requires specific command line arguments to define the group size (N) 
and the target constraints, as input file values for N and K are ignored.

Usage Syntax:
python assg02.py <input_file> N <num_students> <value> <mode_flag>

Arguments:
  <input_file>    Path to the text file containing assignment data (A <id>...).
  N               Literal flag indicating the next argument is student count.
  <num_students>  Integer representing the number of students in the group.
  <value>         Integer value representing K (Prompts) OR M (Days), depending on mode.
  <mode_flag>     Operation mode:
                  --time : Calculates Earliest Completion Time (Value interpreted as K).
                  --k    : Calculates Minimum Prompts (Value interpreted as Max Days).

Examples:
---------

1. Find Earliest Completion Time
   (Scenario: 3 Students, 10 Prompts per day)
   Command:
   python assg02.py input1.txt N 3 10 --time

   Output:
   Earliest Completion Time: X Days

2. Find Best Subscription (Minimum Prompts)
   (Scenario: 3 Students, Must finish in 5 Days)
   Command:
   python assg02.py input1.txt N 3 5 --k

   Output:
   Best Subscription (Min Prompts): K = Y

Notes on Logic:
---------------
- The logic strictly enforces the "Next Day Exchange" rule. A task is considered 
  "ready" only if all its dependencies were completed in previous days.
- The prompt count (K) and group size (N) in the input text file are ignored in 
  favor of the command line arguments.
