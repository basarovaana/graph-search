import time
import math
import random

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

    if path[0] == start:
        return path
    else:
        return []

def bfs(graph, start, end):
    visited = [False] * graph.v_count
    parent = [None] * graph.v_count
    queue = [start]
    visited[start] = True
    while queue:
        u = queue.pop(0)
        if u == end:
            break
        for v, w in graph.adj[u]:
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
            for v, w in graph.adj[u]:
                if not visited[v]:
                    parent[v] = u
                    stack.append(v)
    return reconstruct_path(parent, start, end)


def dijkstra(graph, start, end):
    dist = [float('inf')] * graph.v_count
    parent = [None] * graph.v_count
    visited = [False] * graph.v_count
    dist[start] = 0
    for _ in range(graph.v_count):
        min_d = float('inf')
        u = -1
        for i in range(graph.v_count):
            if not visited[i] and dist[i] < min_d:
                min_d = dist[i];
                u = i
        if u == -1 or u == end: break
        visited[u] = True
        for v, w in graph.adj[u]:
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w;
                parent[v] = u
    return reconstruct_path(parent, start, end)


def bellman_ford(graph, start, end):
    dist = [float('inf')] * graph.v_count
    parent = [None] * graph.v_count
    dist[start] = 0
    for _ in range(graph.v_count - 1):
        for u in range(graph.v_count):
            for v, w in graph.adj[u]:
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w;
                    parent[v] = u
    return reconstruct_path(parent, start, end)


def get_best_case(n):
    g = Graph(n)
    for i in range(n - 1): g.add_edge(i, i + 1, 1)
    return g


def get_worst_case(n):
    g = Graph(n, directed=True)
    for i in range(n):
        for j in range(n):
            if i != j: g.add_edge(i, j, random.randint(1, 10))
    return g


def get_random_case(n):
    g = Graph(n)
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.3: g.add_edge(i, j, random.randint(1, 20))
    return g


def run_bench():
    sizes = [10, 50, 100, 200]
    algos = [("BFS", bfs), ("DFS", dfs), ("Dijkstra", dijkstra), ("Bellman-Ford", bellman_ford)]
    cases = [("Best", get_best_case), ("Worst", get_worst_case), ("Random", get_random_case)]

    header = f"{'Algorithm':<15} | {'Type':<7} | {'N':<5} | {'Time (s)':<12} | {'Error %':<7}"
    print("\n" + header)
    print("-" * len(header))

    for n in sizes:
        for c_name, gen_func in cases:
            g = gen_func(n)
            for a_name, a_func in algos:
                for _ in range(3): a_func(g, 0, n - 1)

                results = []
                for _ in range(10):
                    t0 = time.perf_counter()
                    a_func(g, 0, n - 1)
                    results.append(time.perf_counter() - t0)

                avg = sum(results) / len(results)

                total = 0
                for x in results:
                    total += (x - avg) ** 2

                variance = total / len(results)

                stdev = math.sqrt(variance)

                error_p = (stdev / avg) * 100 if avg > 0 else 0

                print(f"{a_name:<15} | {c_name:<7} | {n:<5} | {avg:>12.6f} | {error_p:>6.2f}%")


if __name__ == "__main__":
    run_bench()
