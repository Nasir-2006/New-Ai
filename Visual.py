"""Interactive search-algorithm dashboard for the attack-network demo.

This replaces the notebook-style output with a standalone desktop UI that:
- runs BFS, DFS, UCS, A*, Hill Climbing, and Alpha-Beta
- shows a polished results table
- visualizes the network graph
- highlights the chosen path for each algorithm
"""

from __future__ import annotations

import heapq
import time
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


NETWORK_GRAPH = {
	"Start_Node": [("Compromised_PC", 2), ("Web_Server", 4), ("Firewall", 5)],
	"Compromised_PC": [("Honeypot", 1)],
	"Honeypot": [],
	"Web_Server": [("Internal_Router", 3)],
	"Firewall": [("Internal_Router", 1)],
	"Internal_Router": [("Database", 2), ("Target_Asset", 7)],
	"Database": [("Target_Asset", 3)],
	"Target_Asset": [],
}

HEURISTICS = {
	"Start_Node": 10,
	"Compromised_PC": 5,
	"Honeypot": 2,
	"Web_Server": 6,
	"Firewall": 7,
	"Internal_Router": 4,
	"Database": 2,
	"Target_Asset": 0,
}

ALGORITHM_DESCRIPTIONS = {
	"BFS": "Explores by level. Reliable for shortest path in unweighted graphs.",
	"DFS": "Follows the deepest branch first. Fast to start, but not always optimal.",
	"UCS": "Expands the least-cost frontier first. Finds optimal weighted paths.",
	"A*": "Balances path cost and heuristic guidance for efficient optimal search.",
	"Hill Climbing": "Greedy local improvement. Can get trapped by local maxima.",
	"Alpha-Beta": "Minimax with pruning. Useful for adversarial planning.",
}


@dataclass
class SearchResult:
	algorithm: str
	path: str
	cost: int
	expanded: int
	exec_ms: float
	status: str


def get_path_cost(path: list[str]) -> int:
	cost = 0
	for index in range(len(path) - 1):
		current = path[index]
		next_node = path[index + 1]
		for neighbor, weight in NETWORK_GRAPH[current]:
			if neighbor == next_node:
				cost += weight
				break
	return cost


def run_bfs(start: str, goal: str):
	start_time = time.time()
	queue = [[start]]
	visited = set()
	expanded = 0

	while queue:
		path = queue.pop(0)
		node = path[-1]
		if node in visited:
			continue
		expanded += 1
		if node == goal:
			return " -> ".join(path), get_path_cost(path), expanded, (time.time() - start_time) * 1000
		visited.add(node)
		for neighbor, _ in NETWORK_GRAPH[node]:
			new_path = list(path)
			new_path.append(neighbor)
			queue.append(new_path)

	return "No Path", 0, expanded, (time.time() - start_time) * 1000


def run_dfs(start: str, goal: str):
	start_time = time.time()
	stack = [[start]]
	visited = set()
	expanded = 0

	while stack:
		path = stack.pop()
		node = path[-1]
		if node in visited:
			continue
		expanded += 1
		if node == goal:
			return " -> ".join(path), get_path_cost(path), expanded, (time.time() - start_time) * 1000
		visited.add(node)
		for neighbor, _ in reversed(NETWORK_GRAPH[node]):
			new_path = list(path)
			new_path.append(neighbor)
			stack.append(new_path)

	return "No Path", 0, expanded, (time.time() - start_time) * 1000


def run_ucs(start: str, goal: str):
	start_time = time.time()
	pq = [(0, [start])]
	visited = set()
	expanded = 0

	while pq:
		cost, path = heapq.heappop(pq)
		node = path[-1]
		if node in visited:
			continue
		expanded += 1
		if node == goal:
			return " -> ".join(path), cost, expanded, (time.time() - start_time) * 1000
		visited.add(node)
		for neighbor, weight in NETWORK_GRAPH[node]:
			if neighbor not in visited:
				heapq.heappush(pq, (cost + weight, path + [neighbor]))

	return "No Path", 0, expanded, (time.time() - start_time) * 1000


def run_astar(start: str, goal: str):
	start_time = time.time()
	pq = [(HEURISTICS[start], 0, [start])]
	visited = set()
	expanded = 0

	while pq:
		f_score, g_cost, path = heapq.heappop(pq)
		node = path[-1]
		if node in visited:
			continue
		expanded += 1
		if node == goal:
			return " -> ".join(path), g_cost, expanded, (time.time() - start_time) * 1000
		visited.add(node)
		for neighbor, weight in NETWORK_GRAPH[node]:
			if neighbor not in visited:
				new_g = g_cost + weight
				new_f = new_g + HEURISTICS[neighbor]
				heapq.heappush(pq, (new_f, new_g, path + [neighbor]))

	return "No Path", 0, expanded, (time.time() - start_time) * 1000


def run_hill_climbing(start: str, goal: str):
	start_time = time.time()
	current = start
	path = [start]
	expanded = 0

	while current != goal:
		expanded += 1
		neighbors = NETWORK_GRAPH[current]
		if not neighbors:
			break

		best_neighbor = None
		best_h = float("inf")
		for neighbor, _ in neighbors:
			if HEURISTICS[neighbor] < best_h:
				best_h = HEURISTICS[neighbor]
				best_neighbor = neighbor

		if best_h >= HEURISTICS[current]:
			break

		current = best_neighbor
		path.append(current)

	cost = get_path_cost(path)
	if current == goal:
		return " -> ".join(path), cost, expanded, (time.time() - start_time) * 1000
	return f"TRAPPED at {current} (Local Max)", cost, expanded, (time.time() - start_time) * 1000


def alpha_beta_search(node: str, depth: int, is_attacker: bool, alpha: float, beta: float, expanded_counter: list[int]):
	expanded_counter[0] += 1
	if depth == 0 or not NETWORK_GRAPH[node] or node == "Target_Asset":
		return HEURISTICS[node], [node]

	best_path = []
	if is_attacker:
		max_eval = float("-inf")
		for neighbor, _ in NETWORK_GRAPH[node]:
			eval_score, path = alpha_beta_search(neighbor, depth - 1, False, alpha, beta, expanded_counter)
			eval_score = -eval_score
			if eval_score > max_eval:
				max_eval = eval_score
				best_path = [node] + path
			alpha = max(alpha, eval_score)
			if beta <= alpha:
				break
		return -max_eval, best_path

	min_eval = float("inf")
	for neighbor, _ in NETWORK_GRAPH[node]:
		eval_score, path = alpha_beta_search(neighbor, depth - 1, True, alpha, beta, expanded_counter)
		eval_score = -eval_score
		if eval_score < min_eval:
			min_eval = eval_score
			best_path = [node] + path
		beta = min(beta, eval_score)
		if beta <= alpha:
			break
	return -min_eval, best_path


def run_adversarial_agent(start: str, goal: str):
	start_time = time.time()
	expanded_counter = [0]
	_, path = alpha_beta_search(start, 4, True, float("-inf"), float("inf"), expanded_counter)
	final_path = []
	for node in path:
		final_path.append(node)
		if node == goal:
			break
	exec_time = (time.time() - start_time) * 1000
	return " -> ".join(final_path), get_path_cost(final_path), expanded_counter[0], exec_time


class SearchDashboard:
	def __init__(self, root: tk.Tk):
		self.root = root
		self.root.title("Attack Network Search Lab")
		self.root.geometry("1500x940")
		self.root.minsize(1320, 840)
		self.root.configure(bg="#0a1020")

		self.results: list[SearchResult] = []
		self.figure = None
		self.graph_canvas = None

		self._setup_style()
		self._build_ui()
		self._render_network_graph(highlight_path=None)

	def _setup_style(self):
		style = ttk.Style()
		style.theme_use("clam")

		style.configure("App.TFrame", background="#0a1020")
		style.configure("Card.TFrame", background="#10182f", relief="flat")
		style.configure("Panel.TFrame", background="#0f1730")
		style.configure("Accent.TFrame", background="#16213f")

		style.configure(
			"Header.TLabel",
			background="#0a1020",
			foreground="#f4f7fb",
			font=("Segoe UI Semibold", 26, "bold"),
		)
		style.configure(
			"SubHeader.TLabel",
			background="#0a1020",
			foreground="#9fb0d3",
			font=("Segoe UI", 11),
		)
		style.configure(
			"Section.TLabel",
			background="#10182f",
			foreground="#f4f7fb",
			font=("Segoe UI Semibold", 13, "bold"),
		)
		style.configure(
			"CardTitle.TLabel",
			background="#10182f",
			foreground="#dce6ff",
			font=("Segoe UI Semibold", 10),
		)
		style.configure(
			"CardValue.TLabel",
			background="#10182f",
			foreground="#ffffff",
			font=("Segoe UI Semibold", 20, "bold"),
		)
		style.configure(
			"Muted.TLabel",
			background="#10182f",
			foreground="#a9b7db",
			font=("Segoe UI", 9),
		)
		style.configure(
			"TButton",
			background="#3a7afe",
			foreground="white",
			font=("Segoe UI Semibold", 10, "bold"),
			padding=10,
			borderwidth=0,
		)
		style.map(
			"TButton",
			background=[("active", "#5a8cff"), ("pressed", "#2a63e8")],
			foreground=[("disabled", "#8a97b8")],
		)
		style.configure(
			"Treeview",
			background="#0f1730",
			fieldbackground="#0f1730",
			foreground="#e7eeff",
			rowheight=32,
			bordercolor="#223055",
			lightcolor="#223055",
			darkcolor="#223055",
			font=("Segoe UI", 10),
		)
		style.configure(
			"Treeview.Heading",
			background="#16213f",
			foreground="#f4f7fb",
			relief="flat",
			font=("Segoe UI Semibold", 10, "bold"),
		)
		style.map("Treeview", background=[("selected", "#294d9b")])
		style.configure("TCombobox", fieldbackground="#0f1730", background="#0f1730", foreground="#e7eeff")

	def _build_ui(self):
		container = ttk.Frame(self.root, style="App.TFrame", padding=18)
		container.pack(fill="both", expand=True)

		header = ttk.Frame(container, style="App.TFrame")
		header.pack(fill="x", pady=(0, 14))

		title_block = ttk.Frame(header, style="App.TFrame")
		title_block.pack(side="left", fill="x", expand=True)

		ttk.Label(title_block, text="Attack Network Search Lab", style="Header.TLabel").pack(anchor="w")
		ttk.Label(
			title_block,
			text="An interactive command-center for comparing uninformed, informed, local, and adversarial search on the same topology.",
			style="SubHeader.TLabel",
		).pack(anchor="w", pady=(6, 0))

		controls = ttk.Frame(header, style="App.TFrame")
		controls.pack(side="right")

		self.start_var = tk.StringVar(value="Start_Node")
		self.goal_var = tk.StringVar(value="Target_Asset")

		start_combo = ttk.Combobox(controls, textvariable=self.start_var, values=list(NETWORK_GRAPH.keys()), width=18, state="readonly")
		goal_combo = ttk.Combobox(controls, textvariable=self.goal_var, values=list(NETWORK_GRAPH.keys()), width=18, state="readonly")
		start_combo.grid(row=0, column=0, padx=(0, 10))
		goal_combo.grid(row=0, column=1, padx=(0, 10))

		ttk.Button(controls, text="Run All Algorithms", command=self.run_all).grid(row=0, column=2, padx=(0, 10))
		ttk.Button(controls, text="Reset View", command=self.reset_view).grid(row=0, column=3)

		metrics = ttk.Frame(container, style="App.TFrame")
		metrics.pack(fill="x", pady=(0, 14))
		self.metric_cards = {}
		card_specs = [
			("Topology Nodes", str(len(NETWORK_GRAPH)), "States in the attack graph"),
			("Heuristic Hints", str(len(HEURISTICS)), "Nodes scored by estimate"),
			("Best Default Route", "A* / UCS", "Strongest baseline solutions"),
			("Trap Node", "Honeypot", "Designed to mislead greedy search"),
		]
		for index, (label, value, subtitle) in enumerate(card_specs):
			card = ttk.Frame(metrics, style="Card.TFrame", padding=16)
			card.grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 12, 0))
			metrics.columnconfigure(index, weight=1)
			ttk.Label(card, text=label, style="CardTitle.TLabel").pack(anchor="w")
			ttk.Label(card, text=value, style="CardValue.TLabel").pack(anchor="w", pady=(6, 0))
			ttk.Label(card, text=subtitle, style="Muted.TLabel", wraplength=250).pack(anchor="w", pady=(8, 0))
			self.metric_cards[label] = card

		body = ttk.PanedWindow(container, orient=tk.HORIZONTAL)
		body.pack(fill="both", expand=True)

		left_panel = ttk.Frame(body, style="Panel.TFrame", padding=16)
		right_panel = ttk.Frame(body, style="Panel.TFrame", padding=16)
		body.add(left_panel, weight=1)
		body.add(right_panel, weight=3)

		algo_panel = ttk.Frame(left_panel, style="Card.TFrame", padding=16)
		algo_panel.pack(fill="x")
		ttk.Label(algo_panel, text="Algorithm Intelligence", style="Section.TLabel").pack(anchor="w")
		self.algo_desc = tk.StringVar(value="Choose a route and run the suite to compare exploration styles.")
		ttk.Label(algo_panel, textvariable=self.algo_desc, style="Muted.TLabel", wraplength=330, justify="left").pack(anchor="w", pady=(10, 0))

		path_panel = ttk.Frame(left_panel, style="Card.TFrame", padding=16)
		path_panel.pack(fill="both", expand=True, pady=(14, 0))
		ttk.Label(path_panel, text="Live Route Summary", style="Section.TLabel").pack(anchor="w")
		self.summary_text = tk.Text(
			path_panel,
			height=16,
			wrap="word",
			bg="#0f1730",
			fg="#e7eeff",
			insertbackground="#ffffff",
			relief="flat",
			font=("Segoe UI", 10),
			padx=12,
			pady=12,
			borderwidth=0,
		)
		self.summary_text.pack(fill="both", expand=True, pady=(10, 0))
		self.summary_text.insert("1.0", self._build_intro_text())
		self.summary_text.config(state="disabled")

		graph_card = ttk.Frame(right_panel, style="Card.TFrame", padding=16)
		graph_card.pack(fill="both", expand=True)
		ttk.Label(graph_card, text="Network Topology Explorer", style="Section.TLabel").pack(anchor="w")
		self.graph_host = ttk.Frame(graph_card, style="Card.TFrame")
		self.graph_host.pack(fill="both", expand=True, pady=(10, 10))

		table_card = ttk.Frame(right_panel, style="Card.TFrame", padding=16)
		table_card.pack(fill="x", pady=(14, 0))
		table_header = ttk.Frame(table_card, style="Card.TFrame")
		table_header.pack(fill="x")
		ttk.Label(table_header, text="Comparative Performance Table", style="Section.TLabel").pack(side="left")
		self.status_var = tk.StringVar(value="Ready to evaluate the search strategies.")
		ttk.Label(table_header, textvariable=self.status_var, style="Muted.TLabel").pack(side="right")

		columns = ("Algorithm", "Path", "Cost", "Expanded", "Time")
		self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=10)
		self.tree.pack(fill="both", expand=True, pady=(10, 0))
		for column in columns:
			self.tree.heading(column, text=column)
		self.tree.column("Algorithm", width=140, anchor="w")
		self.tree.column("Path", width=540, anchor="w")
		self.tree.column("Cost", width=80, anchor="center")
		self.tree.column("Expanded", width=110, anchor="center")
		self.tree.column("Time", width=110, anchor="center")

		self.tree.tag_configure("best", background="#123b2f")
		self.tree.tag_configure("trap", background="#3b2330")
		self.tree.tag_configure("normal", background="#0f1730")

	def _build_intro_text(self) -> str:
		lines = [
			"Welcome to the attack-network search dashboard.",
			"",
			"What to expect:",
			"- BFS and DFS show classic uninformed traversal patterns.",
			"- UCS and A* prioritize lower-cost paths and usually reach the target efficiently.",
			"- Hill Climbing can be baited into the Honeypot trap because of its low heuristic value.",
			"- Alpha-Beta models adversarial planning with pruning.",
			"",
			"Use the selectors at the top to change the start or goal node, then run the full comparison suite.",
		]
		return "\n".join(lines)

	def reset_view(self):
		self.start_var.set("Start_Node")
		self.goal_var.set("Target_Asset")
		self.algo_desc.set("Choose a route and run the suite to compare exploration styles.")
		self.status_var.set("Ready to evaluate the search strategies.")
		self._set_summary(self._build_intro_text())
		self._render_network_graph(highlight_path=None)
		for item in self.tree.get_children():
			self.tree.delete(item)

	def _set_summary(self, text: str):
		self.summary_text.config(state="normal")
		self.summary_text.delete("1.0", tk.END)
		self.summary_text.insert("1.0", text)
		self.summary_text.config(state="disabled")

	def run_all(self):
		start_node = self.start_var.get()
		goal_node = self.goal_var.get()

		if start_node == goal_node:
			self.status_var.set("Start and goal are identical; pick two different nodes for a meaningful comparison.")
			return

		methods = [
			("BFS", run_bfs),
			("DFS", run_dfs),
			("UCS", run_ucs),
			("A*", run_astar),
			("Hill Climbing", run_hill_climbing),
			("Alpha-Beta", run_adversarial_agent),
		]

		self.results = []
		for item in self.tree.get_children():
			self.tree.delete(item)

		for name, method in methods:
			path, cost, expanded, exec_ms = method(start_node, goal_node)
			status = "Goal Reached" if goal_node in path else ("Trapped" if "TRAPPED" in path else "No Path")
			result = SearchResult(name, path, cost, expanded, exec_ms, status)
			self.results.append(result)

		best_result = self._best_result()

		for result in self.results:
			tags = ["normal"]
			if result.algorithm == best_result.algorithm:
				tags = ["best"]
			if result.status == "Trapped":
				tags = ["trap"]
			self.tree.insert(
				"",
				tk.END,
				values=(
					result.algorithm,
					result.path,
					result.cost,
					result.expanded,
					f"{result.exec_ms:.2f}",
				),
				tags=tuple(tags),
			)

		chosen_path = self._path_list(best_result.path)
		self._render_network_graph(highlight_path=chosen_path)
		self._update_summary(start_node, goal_node)
		self.status_var.set(f"Best observed route: {best_result.algorithm} with cost {best_result.cost}.")
		self.algo_desc.set(ALGORITHM_DESCRIPTIONS.get(best_result.algorithm, ""))

	def _best_result(self) -> SearchResult:
		candidates = [r for r in self.results if r.status == "Goal Reached"]
		if candidates:
			return min(candidates, key=lambda item: (item.cost, item.expanded, item.exec_ms))
		return min(self.results, key=lambda item: (item.cost if item.cost > 0 else 10**9, item.expanded, item.exec_ms))

	def _path_list(self, path_string: str) -> list[str]:
		if path_string.startswith("TRAPPED") or path_string == "No Path":
			return []
		return [part.strip() for part in path_string.split("->")]

	def _update_summary(self, start_node: str, goal_node: str):
		lines = [
			f"Start node: {start_node}",
			f"Goal node: {goal_node}",
			"",
			"Algorithm breakdown:",
		]
		for result in self.results:
			lines.append(
				f"- {result.algorithm}: {result.path} | cost={result.cost} | expanded={result.expanded} | time={result.exec_ms:.2f} ms"
			)
		best = self._best_result()
		lines.extend([
			"",
			f"Highlighted winner: {best.algorithm}",
			f"Why it stands out: lowest observed cost, efficient expansion count, and a clean goal reach.",
		])
		self._set_summary("\n".join(lines))

	def _render_network_graph(self, highlight_path: list[str] | None):
		if self.graph_canvas is not None:
			self.graph_canvas.get_tk_widget().destroy()

		graph = nx.DiGraph()
		for node, edges in NETWORK_GRAPH.items():
			for neighbor, weight in edges:
				graph.add_edge(node, neighbor, weight=weight)

		self.figure = plt.figure(figsize=(11.2, 6.6), dpi=100)
		self.figure.patch.set_facecolor("#10182f")
		axis = self.figure.add_subplot(111)
		axis.set_facecolor("#10182f")
		axis.axis("off")

		positions = nx.spring_layout(graph, seed=42, k=0.9)
		default_nodes = [node for node in graph.nodes if node not in (highlight_path or [])]
		highlighted_nodes = highlight_path or []

		nx.draw_networkx_nodes(
			graph,
			positions,
			nodelist=default_nodes,
			node_color="#2d4f8b",
			node_size=2400,
			edgecolors="#9bc2ff",
			linewidths=1.2,
			ax=axis,
		)
		if highlighted_nodes:
			nx.draw_networkx_nodes(
				graph,
				positions,
				nodelist=highlighted_nodes,
				node_color="#ffb703",
				node_size=2600,
				edgecolors="#ffffff",
				linewidths=1.8,
				ax=axis,
			)

		edge_colors = []
		edge_widths = []
		for start, end in graph.edges():
			if highlight_path and any(start == highlight_path[index] and end == highlight_path[index + 1] for index in range(len(highlight_path) - 1)):
				edge_colors.append("#ffb703")
				edge_widths.append(3.4)
			else:
				edge_colors.append("#6c7da8")
				edge_widths.append(1.5)

		nx.draw_networkx_edges(graph, positions, edge_color=edge_colors, width=edge_widths, arrows=True, arrowstyle="-|>", arrowsize=16, ax=axis)
		nx.draw_networkx_labels(graph, positions, font_color="#f4f7fb", font_size=10, font_weight="bold", ax=axis)
		edge_labels = nx.get_edge_attributes(graph, "weight")
		nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels, font_color="#dce6ff", font_size=9, ax=axis)
		axis.set_title(
			"Visual Representation of the Attack Network Topology",
			fontsize=15,
			fontweight="bold",
			color="#f4f7fb",
			pad=18,
		)

		self.graph_canvas = FigureCanvasTkAgg(self.figure, master=self.graph_host)
		self.graph_canvas.draw()
		self.graph_canvas.get_tk_widget().pack(fill="both", expand=True)


def main():
	root = tk.Tk()
	SearchDashboard(root)
	root.mainloop()


if __name__ == "__main__":
	main()
