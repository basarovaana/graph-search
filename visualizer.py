import json
import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons

with open("viz_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

algorithms = sorted(list(set(d["algo"] for d in data)))
cases = sorted(list(set(d["case"] for d in data)))
sizes = sorted(list(set(d["n"] for d in data)))

selected_algo = algorithms[0]
selected_case = cases[0]
selected_n = sizes[0]

current_step = 0

fig, ax = plt.subplots(figsize=(13, 8))

plt.subplots_adjust(left=0.22, bottom=0.15)

algo_ax = plt.axes([0.02, 0.55, 0.15, 0.25])
case_ax = plt.axes([0.02, 0.30, 0.15, 0.20])
size_ax = plt.axes([0.02, 0.10, 0.15, 0.15])

btn_prev_ax = plt.axes([0.78, 0.05, 0.08, 0.05])
btn_next_ax = plt.axes([0.88, 0.05, 0.08, 0.05])

algo_radio = RadioButtons(algo_ax, algorithms)
case_radio = RadioButtons(case_ax, cases)
size_radio = RadioButtons(size_ax, [str(x) for x in sizes])

btn_prev = Button(btn_prev_ax, "Prev")
btn_next = Button(btn_next_ax, "Next")


def get_current_entry():

    for d in data:

        if (
            d["algo"] == selected_algo
            and d["case"] == selected_case
            and d["n"] == selected_n
        ):
            return d

    return None


def draw():

    global current_step

    ax.clear()

    entry = get_current_entry()

    if entry is None:
        return

    edges = entry["edges"]
    steps = entry["steps"]
    path = entry["path"]
    directed = entry["directed"]

    current_step = min(current_step, len(steps) - 1)

    G = nx.DiGraph() if directed else nx.Graph()

    for e in edges:
        G.add_edge(e["u"], e["v"], weight=e["w"])

    pos = nx.spring_layout(G, seed=1)

    step = steps[current_step]

    visited = set(step.get("visited", []))

    current = step.get("current", -1)

    node_colors = []

    for node in G.nodes():

        if node == current:
            node_colors.append("orange")

        elif current_step == len(steps) - 1 and node in path:
            node_colors.append("limegreen")

        elif node in visited:
            node_colors.append("skyblue")

        else:
            node_colors.append("lightgray")

    path_edges = set()

    for i in range(len(path) - 1):
        path_edges.add((path[i], path[i + 1]))

    edge_colors = []

    for u, v in G.edges():

        if current_step == len(steps) - 1:

            if (u, v) in path_edges or (v, u) in path_edges:
                edge_colors.append("limegreen")
            else:
                edge_colors.append("gray")

        else:
            edge_colors.append("gray")

    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=node_colors,
        edge_color=edge_colors,
        node_size=1000,
        font_size=12,
        width=2
    )

    labels = nx.get_edge_attributes(G, "weight")

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=labels,
        ax=ax
    )

    ax.set_title(
        f"{selected_algo} | {selected_case} | n={selected_n} | step {current_step + 1}/{len(steps)}",
        fontsize=14
    )

    ax.axis("off")

    fig.canvas.draw_idle()


def change_algo(label):

    global selected_algo
    global current_step

    selected_algo = label

    current_step = 0

    draw()


def change_case(label):

    global selected_case
    global current_step

    selected_case = label

    current_step = 0

    draw()


def change_size(label):

    global selected_n
    global current_step

    selected_n = int(label)

    current_step = 0

    draw()


def next_step(event):

    global current_step

    entry = get_current_entry()

    current_step = min(
        current_step + 1,
        len(entry["steps"]) - 1
    )

    draw()


def prev_step(event):

    global current_step

    current_step = max(current_step - 1, 0)

    draw()


algo_radio.on_clicked(change_algo)
case_radio.on_clicked(change_case)
size_radio.on_clicked(change_size)

btn_next.on_clicked(next_step)
btn_prev.on_clicked(prev_step)

draw()

plt.show()