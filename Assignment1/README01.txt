# Assignment Scheduling - README

## Files

1. assn01.py - Main program
2. create_inputs.py - Creates sample input files
3. input1.txt - Linear chain (12 assignments)
4. input2.txt - Tree structure (12 assignments)
5. input3.txt - Complex DAG (13 assignments)
6. README01.txt - This file

## Requirements

- Python 3 or higher
- No external libraries needed

## How to Run

### Step 1: Create sample input files

```bash
python create_inputs.py
```

### Step 2: Run the assn01

```bash
python assg01.py <input-file> <required-number-of-days>
```

### Examples

```bash
python assg01.py input1.txt 5
python assg01.py input2.txt 4
python assg01.py input3.txt 6
```

## Input File Format

```
N <number-of-students>
K <prompts-per-day>
A <id> <prompts-needed> <dep1> <dep2> ... 0
```

Example:

```
N 3
K 5
A 1 2 0
A 2 4 1 0
```

- 3 students
- 5 prompts per student per day
- Assignment 1: needs 2 prompts, no dependencies
- Assignment 2: needs 4 prompts, depends on A1

## Output

The program shows:

1. Configuration summary
2. All valid schedules
3. For each schedule:
   - Day-by-day breakdown
   - Which student does which assignments
   - Prompts used per student

## How It Works

1. Reads input file
2. Uses backtracking to try all possible schedules
3. Checks dependencies before assigning work
4. Ensures prompt limits are respected
5. Prints all valid solutions

## Rules

- Assignment needs all dependencies completed first
- Each student has K prompts per day (cannot share)
- Assignment must be done in one day (no partial work)
- One assignment = one student only
- Multiple assignments per student per day is OK (if prompts allow)

## Sample Inputs

**input1.txt**:

- Each assignment depends on the previous one
- Tests sequential processing

**input2.txt**: 

- Multiple independent branches
- Tests parallel work

**input3.txt**: 

- Multiple prerequisites per assignment
- Tests constraint satisfaction


