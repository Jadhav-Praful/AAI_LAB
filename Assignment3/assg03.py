import sys
import heapq

# Global counters for comparison
nodes_visited_astar = 0
nodes_visited_dfbb = 0
nodes_visited_dfs = 0


def takeInput(file):
    works = {}
    try:
        with open(file, "r") as f:
            for line in f:
                line = line.split("%")[0].strip()
                if not line:
                    continue
                parts = line.split()
                if parts[0] == "A":
                    wid = int(parts[1])
                    prompts = int(parts[2])
                    deps = [int(x) for x in parts[3:] if int(x) != 0]
                    # ChatGPT (Even), Gemini (Odd)
                    llm_type = "chatgpt" if wid % 2 == 0 else "gemini"
                    works[wid] = {"prompts": prompts, "deps": deps, "type": llm_type}
    except FileNotFoundError:
        print(f"Error: File {file} not found.")
        sys.exit(1)
    return works


def get_critical_path_heuristic(done_tasks, works):
    """Longest remaining dependency chain estimate (h)."""
    remaining = [w for w in works if w not in done_tasks]
    if not remaining:
        return 0
    memo = {}

    def get_depth(wid):
        if wid in done_tasks:
            return 0
        if wid in memo:
            return memo[wid]
        children = [o for o in works if wid in works[o]["deps"]]
        memo[wid] = 1 + (max(get_depth(c) for c in children) if children else 0)
        return memo[wid]

    return max(get_depth(w) for w in remaining)


def get_possible_daily_combos(N, K_chat, K_gem, done, works, case_b):
    available = [
        w for w in works if w not in done and all(d in done for d in works[w]["deps"])
    ]
    valid_combos = []

    def backtrack(idx, cur_chat, cur_gem, student_busy, current_tasks):
        if idx == len(available):
            if current_tasks:
                valid_combos.append(frozenset(current_tasks))
            return

        # Skip
        backtrack(idx + 1, cur_chat, cur_gem, student_busy, current_tasks)

        # Take
        wid = available[idx]
        task = works[wid]
        is_chat = task["type"] == "chatgpt"
        cost = task["prompts"]

        if (is_chat and cur_chat >= cost) or (not is_chat and cur_gem >= cost):
            for s in range(N):
                if not case_b and student_busy[s]:
                    continue
                new_busy = list(student_busy)
                new_busy[s] = True
                nc = cur_chat - cost if is_chat else cur_chat
                ng = cur_gem - cost if not is_chat else cur_gem
                backtrack(idx + 1, nc, ng, new_busy, current_tasks + [wid])
                break  # Symmetry breaking

    backtrack(0, K_chat, K_gem, [False] * N, [])
    return list(set(valid_combos)) if valid_combos else [frozenset()]


# --- Algorithms ---


def solve_astar(N, K_chat, K_gem, works, case_b):
    global nodes_visited_astar
    nodes_visited_astar = 0
    pq = [(get_critical_path_heuristic(set(), works), 0, frozenset())]
    visited = {frozenset(): 0}

    while pq:
        f, days, done = heapq.heappop(pq)
        nodes_visited_astar += 1
        if len(done) == len(works):
            return days

        for combo in get_possible_daily_combos(N, K_chat, K_gem, done, works, case_b):
            if not combo:
                continue
            new_done = done | combo
            new_days = days + 1
            if new_done not in visited or visited[new_done] > new_days:
                visited[new_done] = new_days
                h = get_critical_path_heuristic(new_done, works)
                heapq.heappush(pq, (new_days + h, new_days, new_done))
    return float("inf")


def solve_dfbb(N, K_chat, K_gem, works, case_b):
    global nodes_visited_dfbb
    nodes_visited_dfbb = 0
    best_days = float("inf")
    visited = {}

    def dfs_search(done, days):
        nonlocal best_days
        global nodes_visited_dfbb
        nodes_visited_dfbb += 1

        h = get_critical_path_heuristic(done, works)
        if days + h >= best_days:
            return

        if len(done) == len(works):
            best_days = min(best_days, days)
            return

        state_key = frozenset(done)
        if state_key in visited and visited[state_key] <= days:
            return
        visited[state_key] = days

        combos = get_possible_daily_combos(N, K_chat, K_gem, done, works, case_b)
        combos.sort(key=len, reverse=True)  # Greedy heuristic

        for combo in combos:
            if not combo:
                continue
            dfs_search(done | combo, days + 1)

    dfs_search(set(), 0)
    return best_days


def solve_dfs(N, K_chat, K_gem, works, case_b):
    """Standard DFS without Branch & Bound pruning (still uses state memoization)."""
    global nodes_visited_dfs
    nodes_visited_dfs = 0
    visited = {}

    def dfs_search(done, days):
        global nodes_visited_dfs
        nodes_visited_dfs += 1

        if len(done) == len(works):
            return days

        state_key = frozenset(done)
        if state_key in visited and visited[state_key] <= days:
            return float("inf")
        visited[state_key] = days

        min_res = float("inf")
        combos = get_possible_daily_combos(N, K_chat, K_gem, done, works, case_b)
        for combo in combos:
            if not combo:
                continue
            res = dfs_search(done | combo, days + 1)
            min_res = min(min_res, res)
        return min_res

    return dfs_search(set(), 0)


def compare_algorithms(N, k_chat, k_gem, works):
    """Prints a comparison table for node counts across algorithms."""
    print("\n" + "=" * 60)
    print(f"{'ALGORITHM COMPARISON':^60}")
    print("=" * 60)
    print(f"{'Case':<10} | {'Algo':<8} | {'Result':<10} | {'Nodes Visited':<15}")
    print("-" * 60)

    for label, case_b in [("Case-A", False), ("Case-B", True)]:
        # Run A*
        res_astar = solve_astar(N, k_chat, k_gem, works, case_b)
        print(f"{label:<10} | {'A*':<8} | {res_astar:<10} | {nodes_visited_astar:<15}")

        # Run DFBB
        res_dfbb = solve_dfbb(N, k_chat, k_gem, works, case_b)
        print(f"{label:<10} | {'DFBB':<8} | {res_dfbb:<10} | {nodes_visited_dfbb:<15}")

        # Run DFS
        res_dfs = solve_dfs(N, k_chat, k_gem, works, case_b)
        print(f"{label:<10} | {'DFS':<8} | {res_dfs:<10} | {nodes_visited_dfs:<15}")
        print("-" * 60)


def main():
    if len(sys.argv) < 8:
        print("Usage: python assg.py <input> N <students> <c1> <c2> --time/--k <val>")
        return

    file = sys.argv[1]
    students = int(sys.argv[3])
    c1, c2 = int(sys.argv[4]), int(sys.argv[5])
    mode = sys.argv[6]
    val = sys.argv[7]

    works = takeInput(file)

    if mode == "--time":
        k_val = int(val)
        compare_algorithms(students, k_val, k_val, works)

    elif mode == "--k":
        max_days = int(val)
        # Find minimum cost using A* for verification
        min_cost = float("inf")
        # Example range search for K values
        for k_chat in range(1, 10):
            for k_gem in range(1, 10):
                if solve_astar(students, k_chat, k_gem, works, False) <= max_days:
                    cost = k_chat * c1 + k_gem * c2
                    if cost < min_cost:
                        min_cost = cost
        print(f"\nObjective: Find Minimum Subscription Cost for {max_days} days limit")
        print(f"Result: {min_cost}")
        # Compare node counts for one of the feasible K pairs
        # compare_algorithms(students, 5, 5, works) # Example call


if __name__ == "__main__":
    main()
