import json
import random
from typing import Any, Optional

import networkx as nx
from networkx.classes import DiGraph


def build_graph(tasks: list[dict[str, Any]]) -> DiGraph:
    G = nx.DiGraph()

    for task in tasks:
        G.add_node(task["id"], duration=task["duration"], memory=task["memory"])
        for dep in task["dependencies"]:
            G.add_edge(dep, task["id"])

    return G


def find_critical_path(dag: DiGraph) -> tuple[list[int], int]:
    topological_order = list(nx.topological_sort(dag))
    longest_path_length = {node: 0 for node in dag.nodes}
    predecessor: dict[str, Optional[str]] = {node: None for node in dag.nodes}

    for node in topological_order:
        for succ in dag.successors(node):
            new_length = longest_path_length[node] + dag.nodes[node]["duration"]
            if new_length > longest_path_length[succ]:
                longest_path_length[succ] = new_length
                predecessor[succ] = node

    end_node = max(longest_path_length, key=lambda n: longest_path_length[n])
    critical_path = []
    node = end_node
    while node is not None:
        critical_path.append(node)
        node = predecessor[node]

    return list(reversed(critical_path)), longest_path_length[end_node]


def generate_task_graph(num_tasks: int, max_dependencies: Optional[int] = None, random_seed: Optional[int] = None) -> tuple[DiGraph, dict[str,Any],int,int]:
    if random_seed is None:
        random_seed = random.randint(0, 99999)
    random.seed(random_seed)

    G: DiGraph[str] = nx.DiGraph()
    tasks = [f"task{i}" for i in range(1, num_tasks + 1)]
    G.add_nodes_from(tasks)

    task_data: dict[str,Any] = {}

    if max_dependencies is None:
        max_dependencies = random.randint(1, num_tasks - 1)

    for task in tasks:
        duration = random.randint(5, 30)
        memory = random.choice([256, 512, 1024, 2048])

        if task != "task1":
            num_deps = random.randint(1, min(max_dependencies, len(tasks) - 1))  
            possible_parents = [t for t in tasks if t < task]
            selected_parents = random.sample(possible_parents, min(len(possible_parents), num_deps))
        else:
            selected_parents = []

        task_data[task] = {
            "id": task,
            "duration": duration,
            "memory": memory,
            "dependencies": selected_parents
        }

        for dep in selected_parents:
            G.add_edge(dep, task)

    return G, task_data, random_seed, max_dependencies

def save_graph_to_json(task_data: dict[str,Any], num_tasks: int, max_dependencies: int, random_seed: int) -> None:
    graph_json = {
        "graph_id": f"task_graph_ntask_{num_tasks}_max_dep_{max_dependencies}_seed_{random_seed}",
        "random_seed": random_seed,
        "max_dependencies": max_dependencies,
        "tasks": list(task_data.values())
    }

    filename = f"data/in/task_graph_{num_tasks}_{max_dependencies}_seed_{random_seed}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(graph_json, f, indent=4)

    print(f"\n Graphe saved in {filename}")
    print(f"Used seed: {random_seed}")
    print(f"Max dependencies: {max_dependencies}")
