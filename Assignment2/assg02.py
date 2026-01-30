import sys
import math

count = 0

# --- Existing Functions (Preserved) ---


def takeInput(file):
    N = 0
    K = 0
    works = {}
    with open(file, "r") as f:
        for line in f:
            line = line.split("%")[0].strip()
            if not line:
                continue
            remaining = line.split()
            if remaining[0] == "N":
                N = int(remaining[1])
            elif remaining[0] == "K":
                K = int(remaining[1])
            elif remaining[0] == "A":
                wid = int(remaining[1])
                noOfPrompt = int(remaining[2])
                dependencies = [int(x) for x in remaining[3:] if int(x) != 0]
                works[wid] = {
                    "noOfPrompt": noOfPrompt,
                    "dependencies": dependencies,
                }
    return N, K, works


def printing_schedules(schedule, works):
    global count
    count = count + 1
    print("Valid Schedule Found:")
    curr_day = 0
    for day, student, work in schedule:
        if day != curr_day:
            print(f"--- Day {day} ---")
            curr_day = day
        print(
            f"Student {student} -> Assignment {work} (Prompts: {works[work]['noOfPrompt']})"
        )
    print("=" * 45)


def valid_works_without_dependencies(works, done):
    return [
        work
        for work in works
        if work not in done and all(day in done for day in works[work]["dependencies"])
    ]


def scheduling(day, prompts, done, schedule, N, K, M, works):
    if len(done) == len(works):
        printing_schedules(schedule, works)
        return

    valid_works = valid_works_without_dependencies(works, done)
    progress = False

    for wid in valid_works:
        noOfPrompt = works[wid]["noOfPrompt"]
        for x in range(N):
            if prompts[x] >= noOfPrompt:
                new_prompts = list(prompts)
                new_prompts[x] -= noOfPrompt

                scheduling(
                    day,
                    new_prompts,
                    done | {wid},
                    schedule + [(day, x + 1, wid)],
                    N,
                    K,
                    M,
                    works,
                )
                progress = True

    if day < M:
        if not progress or valid_works:
            scheduling(day + 1, [K] * N, done, schedule, N, K, M, works)


# --- New Functions for Assignment 2 ---


def calculate_earliest_finish(N, K, works):
    """
    Simulates the schedule to find the earliest completion time.
    Constraint: Solutions are exchanged next day (6 AM), but a student
    can use their OWN solutions immediately on the same day.
    """
    # Safety Check: If any single task > K, it's impossible
    if any(w["noOfPrompt"] > K for w in works.values()):
        return float("inf")

    global_known = set()  # Knowledge shared at 6 AM
    completed_tasks = set()
    days = 0

    total_tasks = len(works)

    while len(completed_tasks) < total_tasks:
        days += 1
        day_progress = set()  # Tasks finished today

        # State for today: [Current Prompts, Current Knowledge]
        student_capacity = [K] * N
        student_knowledge = [set(global_known) for _ in range(N)]

        # Greedy Simulation for the day
        # We repeat until no student can take any more tasks today
        while True:
            progress_in_round = False

            # Find candidate tasks: Not done globally, Not done today
            # We sort by cost descending (Heuristic: Do hardest tasks first)
            candidates = [
                w for w in works if w not in completed_tasks and w not in day_progress
            ]
            candidates.sort(key=lambda x: works[x]["noOfPrompt"], reverse=True)

            for wid in candidates:
                req_prompts = works[wid]["noOfPrompt"]
                deps = set(works[wid]["dependencies"])

                # Try to find a student who can do this task
                for s in range(N):
                    # Check 1: Capacity
                    if student_capacity[s] >= req_prompts:
                        # Check 2: Dependencies (Must be in student's current knowledge)
                        if deps.issubset(student_knowledge[s]):
                            # Assign
                            student_capacity[s] -= req_prompts
                            student_knowledge[s].add(wid)
                            day_progress.add(wid)
                            progress_in_round = True
                            break  # Task assigned, move to next candidate

                if progress_in_round:
                    break  # Restart candidate scan to prioritize high cost again

            if not progress_in_round:
                break  # No more tasks can be assigned today

        # End of Day: Update Global Knowledge for 6 AM next day
        if not day_progress:
            return float("inf")  # Stuck (Deadlock or insufficient K)

        completed_tasks.update(day_progress)
        global_known.update(day_progress)

    return days


def find_best_subscription(N, MaxDays, works):
    """
    Binary Search to find minimum K (prompts) that allows finishing in MaxDays.
    """
    low = max(w["noOfPrompt"] for w in works.values())
    high = sum(w["noOfPrompt"] for w in works.values())  # Upper bound
    best_k = -1

    while low <= high:
        mid_k = (low + high) // 2
        days_needed = calculate_earliest_finish(N, mid_k, works)

        if days_needed <= MaxDays:
            best_k = mid_k
            high = mid_k - 1  # Try to find a smaller K
        else:
            low = mid_k + 1

    return best_k


# --- Main Logic ---


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        # print("  Assg 1: python assg01.py <input> <days>")
        print("  Assg 2 (Time): python assg02.py <input> N <students> <prompts> --time")
        print("  Assg 2 (Min K): python assg02.py <input> N <students> <max_days> --k")
        return

    file = sys.argv[1]

    try:
        # Parse Input (Standard)
        # Note: For Assg 2, we might ignore N/K from file, but we still read works
        N_file, K_file, works = takeInput(file)

        # Check if running Assignment 2 Extended Mode
        if len(sys.argv) >= 6 and sys.argv[2] == "N":
            # Format: file N <stud> <val> <flag>
            N_cmd = int(sys.argv[3])
            val_cmd = int(sys.argv[4])
            mode = sys.argv[5]

            if mode == "--time":
                # val_cmd is K
                print(f"Calculating Earliest Time (N={N_cmd}, K={val_cmd})...")
                days = calculate_earliest_finish(N_cmd, val_cmd, works)
                if days == float("inf"):
                    print("Impossible to complete with given constraints.")
                else:
                    print(f"Earliest Completion Time: {days} Days")

            elif mode == "--k":
                # val_cmd is Max Days
                print(
                    f"Calculating Best Subscription (N={N_cmd}, MaxDays={val_cmd})..."
                )
                k = find_best_subscription(N_cmd, val_cmd, works)
                if k == -1:
                    print("Impossible to complete within day limit.")
                else:
                    print(f"Best Subscription (Minimum Prompts): K = {k}")

        else:
            # Fallback to Assignment 1 Legacy Mode
            M = int(sys.argv[2])
            if N_file == 0 or K_file == 0 or not works:
                print("Error: Invalid input file.")
                return

            print(
                f"Solving for {len(works)} Assignments, {N_file} Students, {M} Days..."
            )
            scheduling(1, [K_file] * N_file, set(), [], N_file, K_file, M, works)
            print(f"total number of valid schedule {count}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
