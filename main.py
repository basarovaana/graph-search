import heapq
import json
import math
import random
import time

T_VALUE_95 = {
    6: 2.5706,
    11: 2.2281,
    16: 2.1314,
    21: 2.0860,
    26: 2.0555,
    31: 2.0423,
    36: 2.0301,
    41: 2.0211,
    51: 2.0086,
    101: 1.9840,
}


class Graph:
    def __init__(self, vertices_count, directed=False):
        self.v_count = vertices_count
        self.directed = directed
        self.adj = [[] for _ in range(vertices_count)]

    def add_edge(self, u, v, weight=1):
        self.adj[u].append([v, weight])

        if not self.directed:
            self.adj[v].append([u, weight])


def reconstruct_path(parent, start, end):
    path = []
    curr = end

    while curr is not None:
        path.append(curr)
        curr = parent[curr]

    path.reverse()

    if path and path[0] == start:
        return path

    return []


def calculate_path_cost(graph, path):
    if not path:
        return -1

    cost = 0

    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]

        for to, weight in graph.adj[u]:
            if to == v:
                cost += weight
                break

    return cost


def bfs(graph, start, end):
    visited = [False] * graph.v_count
    parent = [None] * graph.v_count

    queue = [start]
    visited[start] = True

    while queue:
        u = queue.pop(0)

        if u == end:
            break

        for v, weight in graph.adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                queue.append(v)

    return reconstruct_path(parent, start, end)


def dfs(graph, start, end):
    visited = [False] * graph.v_count
    parent = [None] * graph.v_count

    stack = [start]

    while stack:
        u = stack.pop()

        if u == end:
            break

        if not visited[u]:
            visited[u] = True

            for v, weight in graph.adj[u]:
                if not visited[v]:
                    parent[v] = u
                    stack.append(v)

    return reconstruct_path(parent, start, end)


def dijkstra(graph, start, end):
    dist = [float("inf")] * graph.v_count
    parent = [None] * graph.v_count
    visited = [False] * graph.v_count

    dist[start] = 0

    for _ in range(graph.v_count):
        min_d = float("inf")
        u = -1

        for i in range(graph.v_count):
            if not visited[i] and dist[i] < min_d:
                min_d = dist[i]
                u = i

        if u == -1 or u == end:
            break

        visited[u] = True

        for v, weight in graph.adj[u]:
            if (
                not visited[v]
                and dist[u] + weight < dist[v]
            ):
                dist[v] = dist[u] + weight
                parent[v] = u

    return reconstruct_path(parent, start, end)


def bellman_ford(graph, start, end):
    dist = [float("inf")] * graph.v_count
    parent = [None] * graph.v_count

    dist[start] = 0

    for _ in range(graph.v_count - 1):
        for u in range(graph.v_count):
            for v, weight in graph.adj[u]:
                if (
                    dist[u] != float("inf")
                    and dist[u] + weight < dist[v]
                ):
                    dist[v] = dist[u] + weight
                    parent[v] = u

    return reconstruct_path(parent, start, end)


def astar(graph, start, end):
    def heuristic(vertex):
        return abs(vertex - end)

    dist = [float("inf")] * graph.v_count
    parent = [None] * graph.v_count
    visited = [False] * graph.v_count

    dist[start] = 0

    heap = [(heuristic(start), start)]

    while heap:
        _, u = heapq.heappop(heap)

        if u == end:
            break

        if visited[u]:
            continue

        visited[u] = True

        for v, weight in graph.adj[u]:
            if (
                not visited[v]
                and dist[u] + weight < dist[v]
            ):
                dist[v] = dist[u] + weight
                parent[v] = u

                heapq.heappush(
                    heap,
                    (dist[v] + heuristic(v), v),
                )

    return reconstruct_path(parent, start, end)


def bfs_steps(graph, start, end):
    steps = []

    visited = [False] * graph.v_count
    parent = [None] * graph.v_count

    queue = [start]
    visited[start] = True

    while queue:
        u = queue.pop(0)

        steps.append({
            "current": u,
            "visited": [
                i
                for i, value in enumerate(visited)
                if value
            ],
        })

        if u == end:
            break

        for v, weight in graph.adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                queue.append(v)

    path = reconstruct_path(parent, start, end)

    return steps, path


def dfs_steps(graph, start, end):
    steps = []

    visited = [False] * graph.v_count
    parent = [None] * graph.v_count

    stack = [start]

    while stack:
        u = stack.pop()

        if not visited[u]:
            visited[u] = True

            steps.append({
                "current": u,
                "visited": [
                    i
                    for i, value in enumerate(visited)
                    if value
                ],
            })

            if u == end:
                break

            for v, weight in graph.adj[u]:
                if not visited[v]:
                    parent[v] = u
                    stack.append(v)

    path = reconstruct_path(parent, start, end)

    return steps, path


def dijkstra_steps(graph, start, end):
    steps = []

    dist = [float("inf")] * graph.v_count
    parent = [None] * graph.v_count
    visited = [False] * graph.v_count

    dist[start] = 0

    for _ in range(graph.v_count):
        min_d = float("inf")
        u = -1

        for i in range(graph.v_count):
            if not visited[i] and dist[i] < min_d:
                min_d = dist[i]
                u = i

        if u == -1 or u == end:
            break

        visited[u] = True

        steps.append({
            "current": u,
            "visited": [
                i
                for i, value in enumerate(visited)
                if value
            ],
            "dist": [
                d if d != float("inf") else -1
                for d in dist
            ],
        })

        for v, weight in graph.adj[u]:
            if (
                not visited[v]
                and dist[u] + weight < dist[v]
            ):
                dist[v] = dist[u] + weight
                parent[v] = u

    path = reconstruct_path(parent, start, end)

    return steps, path


def bellman_ford_steps(graph, start, end):
    steps = []

    dist = [float("inf")] * graph.v_count
    parent = [None] * graph.v_count

    dist[start] = 0

    for iteration in range(graph.v_count - 1):
        updated = False

        for u in range(graph.v_count):
            for v, weight in graph.adj[u]:
                if (
                    dist[u] != float("inf")
                    and dist[u] + weight < dist[v]
                ):
                    dist[v] = dist[u] + weight
                    parent[v] = u
                    updated = True

        steps.append({
            "iteration": iteration,
            "current": -1,
            "dist": [
                d if d != float("inf") else -1
                for d in dist
            ],
        })

        if not updated:
            break

    path = reconstruct_path(parent, start, end)

    return steps, path


def astar_steps(graph, start, end):
    def heuristic(vertex):
        return abs(vertex - end)

    steps = []

    dist = [float("inf")] * graph.v_count
    parent = [None] * graph.v_count
    visited = [False] * graph.v_count

    dist[start] = 0

    heap = [(heuristic(start), start)]

    while heap:
        _, u = heapq.heappop(heap)

        if visited[u]:
            continue

        visited[u] = True

        steps.append({
            "current": u,
            "visited": [
                i
                for i, value in enumerate(visited)
                if value
            ],
            "dist": [
                d if d != float("inf") else -1
                for d in dist
            ],
        })

        if u == end:
            break

        for v, weight in graph.adj[u]:
            if (
                not visited[v]
                and dist[u] + weight < dist[v]
            ):
                dist[v] = dist[u] + weight
                parent[v] = u

                heapq.heappush(
                    heap,
                    (dist[v] + heuristic(v), v),
                )

    path = reconstruct_path(parent, start, end)

    return steps, path


def get_best_case(n):
    graph = Graph(n)

    for i in range(n - 1):
        graph.add_edge(i, i + 1, 1)

    return graph


def get_worst_case(n):
    graph = Graph(n, directed=True)

    for i in range(n):
        for j in range(n):
            if i != j:
                graph.add_edge(
                    i,
                    j,
                    random.randint(1, 10),
                )

    return graph


def get_random_case(n):
    graph = Graph(n)

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.3:
                graph.add_edge(
                    i,
                    j,
                    random.randint(1, 20),
                )

    for i in range(n - 1):
        connected = any(
            v == i + 1
            for v, weight in graph.adj[i]
        )

        if not connected:
            graph.add_edge(
                i,
                i + 1,
                random.randint(1, 20),
            )

    return graph


def get_t_value(n):
    keys = sorted(T_VALUE_95.keys())

    for key in keys:
        if n <= key:
            return T_VALUE_95[key]

    return 1.9840


def run_bench():
    sizes = [10, 50, 100, 200]

    algos = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("Dijkstra", dijkstra),
        ("Bellman-Ford", bellman_ford),
        ("A*", astar),
    ]

    cases = [
        ("Best", get_best_case),
        ("Worst", get_worst_case),
        ("Random", get_random_case),
    ]

    header = (
        f"{'Algorithm':<15} | "
        f"{'Type':<7} | "
        f"{'N':<5} | "
        f"{'Time (s)':<12} | "
        f"{'Error %':<7}"
    )

    print("\n" + header)
    print("-" * len(header))

    for n in sizes:
        for case_name, gen_func in cases:
            graph = gen_func(n)

            for algo_name, algo_func in algos:
                for _ in range(3):
                    algo_func(graph, 0, n - 1)

                results = []

                for _ in range(10):
                    start_time = time.perf_counter()

                    algo_func(graph, 0, n - 1)

                    elapsed = (
                        time.perf_counter() - start_time
                    )

                    results.append(elapsed)

                avg = sum(results) / len(results)

                variance_sum = 0

                for value in results:
                    diff = value - avg
                    variance_sum += diff ** 2

                variance = (
                    variance_sum / (len(results) - 1)
                )

                stdev = math.sqrt(variance)

                if avg > 0:
                    error_percent = (
                        stdev / avg
                    ) * 100
                else:
                    error_percent = 0

                t_value = get_t_value(len(results))

                delta = (
                    t_value
                    * stdev
                    / math.sqrt(len(results))
                )

                status = ""

                if error_percent > 5:
                    status = " HIGH ERROR"

                print(
                    f"{algo_name:<15} | "
                    f"{case_name:<7} | "
                    f"{n:<5} | "
                    f"{avg:>12.6f} | "
                    f"{delta:>12.6f} | "
                    f"{error_percent:>7.2f}%"
                    f"{status}"
                )


def export_visualization(
    filename="viz_data.json",
):
    sizes = [10, 50, 100]

    algo_steps = [
        ("BFS", bfs_steps),
        ("DFS", dfs_steps),
        ("Dijkstra", dijkstra_steps),
        ("Bellman-Ford", bellman_ford_steps),
        ("A*", astar_steps),
    ]

    cases = [
        ("Best", get_best_case),
        ("Worst", get_worst_case),
        ("Random", get_random_case),
    ]

    data = []

    for n in sizes:
        for case_name, gen_func in cases:
            graph = gen_func(n)

            edges = []
            seen = set()

            for u in range(graph.v_count):
                for v, weight in graph.adj[u]:
                    if graph.directed:
                        key = (u, v)
                    else:
                        key = (
                            min(u, v),
                            max(u, v),
                        )

                    if key not in seen:
                        seen.add(key)

                        edges.append({
                            "u": u,
                            "v": v,
                            "w": weight,
                        })

            for algo_name, algo_func in algo_steps:
                steps, path = algo_func(
                    graph,
                    0,
                    n - 1,
                )

                data.append({
                    "algo": algo_name,
                    "case": case_name,
                    "n": n,
                    "edges": edges,
                    "directed": graph.directed,
                    "steps": steps,
                    "path": path,
                    "path_cost": calculate_path_cost(
                        graph,
                        path,
                    ),
                })

                print(
                    f"  exported: "
                    f"{algo_name} / "
                    f"{case_name} / "
                    f"n={n} "
                    f"({len(steps)} steps, "
                    f"path len={len(path)})"
                )

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
        )

    print(
        f"\nСохранено в {filename} "
        f"({len(data)} записей)"
    )


if __name__ == "__main__":
    run_bench()
    export_visualization()
