"""
Value Learning for Zero-Sum Games. In COMP364, we call this simply the "value
learning algorithm." It is a specific type of reinforcement learning known as a
"tabular solution using temporal difference updates."

Created by Google Gemini, then edited by John MacCormack
"""


import argparse
from pathlib import Path
import tomllib

DEFAULT_GRAPH_FILE = "game_graph.toml"

DEFAULT_GRAPH_CONTENT = """[edges]
a = ["b", "c"]
b = ["c"]
c = ["z"]
z = []

[values]
a = 0.5
b = 0.4
c = 0.8
z = 0.0

[hardwired_rng]
rho = [0.88, 0.21, 0.62, 0.89, 0.48]
"""


class HardwiredRNG:
    """A hardwired pseudo-random number generator that returns a predefined sequence of numbers.
    This is useful for deterministic testing and reproducibility of simulations."""

    def __init__(self, sequence):
        self.sequence = sequence
        self._iterator = iter(self.sequence)

    def get_next_rnd(self) -> float:
        """Return the next number in the predefined sequence, if available."""
        try:
            return next(self._iterator)
        except StopIteration:
            return None


def td_zero_sum_update(v_curr: float, v_next: float, eta: float = 0.1) -> float:
    """Computes V(S_t) <- V(S_t) + eta * ((1 - V(S_{t+1})) - V(S_t))."""
    return (1 - eta) * v_curr + eta * (1 - v_next)


def parse_graph_toml(file_path: str):
    """Parses graph structure and initial node values from a TOML file."""
    with open(file_path, "rb") as f:
        data = tomllib.load(f)
    return data["edges"], data["values"], data["hardwired_rng"]["rho"]


def choose_exploratory_move(options: list, values: dict, rng: HardwiredRNG) -> str:
    """Randomly choose one of the moves that is not the current-best move"""
    best_move = choose_greedy_move(options, values)
    remaining_options = options.copy()
    remaining_options.remove(best_move)
    assert remaining_options, "No alternative moves available for exploration."
    if len(remaining_options) == 1:
        return remaining_options[0]  # Return the only alternative move
    # Consume a random number to select among the remaining options
    rho = rng.get_next_rnd()
    assert rho is not None, "Ran out of random numbers for exploratory move."
    # Use rho to select an alternative move
    return remaining_options[int(rho * len(remaining_options))]


def choose_greedy_move(options, values):
    """Choose the move with the highest value to the current player, which must
    be the lowest value for the opponent in a zero-sum game. Therefore, we
    select the move with the minimum value."""
    best_move = min(options, key=lambda x: values[x])
    return best_move


def run_single_episode(
    start_node: str,
    end_node: str,
    edges: dict,
    values: dict,
    rng: HardwiredRNG,
    epsilon: float = 0.3,
    eta: float = 0.1,
):
    """Executes a single episode trajectory dynamically from start_node to end_node,
    consuming pseudo-random numbers only when branching choices exist.
    """
    path = [start_node]
    # Stores tuple: (from_node, to_node, rho_value, move_type)
    transitions = []

    curr = start_node
    while curr != end_node:
        options = edges.get(curr, [])
        if not options:
            break  # Reached a sink state without reaching end_node

        # Rule: Consume random number ONLY if strictly more than one option
        if len(options) > 1:
            rho = rng.get_next_rnd()
            if rho is not None and rho < epsilon:
                next_node = choose_exploratory_move(
                    options, values, rng)  # Exploratory move E
                move_type = "E"
            else:
                next_node = choose_greedy_move(
                    options, values)  # Greedy move, labelled B for "best"
                move_type = "B"
        else:
            rho = None
            next_node = options[0]  # Single choice defaults to best move B
            move_type = "B"

        transitions.append((curr, next_node, rho, move_type))
        curr = next_node
        path.append(curr)

    # Record initial state values along the path
    init_vals = [values[node] for node in path]

    # Perform TD updates forwards along the trajectory. A more sophisticated
    # algorithm would do this in reverse order to propagate values more
    # efficiently, but we use a naive approach here.
    updated_vals = {}
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]

        u_val = values[u]
        v_val = values[v]

        # Update value only for greedy moves
        if transitions[i][3] == 'B':
            updated_vals[u] = td_zero_sum_update(u_val, v_val, eta)
        else:
            updated_vals[u] = None

    # Order updated values along the path (excluding terminal state which doesn't update)
    updated_vals_list = [updated_vals[node] for node in path[:-1]]

    # Mutate the primary values dictionary with the new state estimations
    for node, new_val in updated_vals.items():
        if new_val is not None:
            values[node] = new_val

    return {
        "path": path,
        "transitions": transitions,
        "init_vals": init_vals,
        "updated_vals": updated_vals_list,
    }


def simulate_episodes(
    edges: dict,
    initial_values: dict,
    hardwired_rng_seq: list,
    start_node: str = "a",
    end_node: str = "z",
    num_episodes: int = 2,
    epsilon: float = 0.3,
    eta: float = 0.1,
):
    """Simulates N=num_episode episodes sequentially over a general directed graph structure."""
    rng = HardwiredRNG(hardwired_rng_seq)
    values = initial_values.copy()
    episodes_data = []

    for _ in range(num_episodes):
        ep_data = run_single_episode(
            start_node, end_node, edges, values, rng, epsilon, eta
        )
        episodes_data.append(ep_data)

    return episodes_data


def generate_markdown(episodes_data: list) -> str:
    """Generates a structured Markdown table representation of simulated episodes."""
    md_lines = ["### Value Learning Episode Outputs\n"]

    for ep_idx, ep_data in enumerate(episodes_data, start=1):
        path = ep_data["path"]
        transitions = ep_data["transitions"]
        init_vals = ep_data["init_vals"]
        updated_vals = ep_data["updated_vals"]

        md_lines.append(f"#### Episode {ep_idx}\n")

        # Table Header
        header = ["Step", "State", "Transition", "Initial $V$", "Updated $V$"]
        md_lines.append("| " + " | ".join(header) + " |")
        md_lines.append("| " + " | ".join(["---"] * len(header)) + " |")

        # Table Rows
        for i, state in enumerate(path):
            if i < len(transitions):
                _, next_node, rho, move_type = transitions[i]
                if rho is not None:
                    trans_str = f"$\\rho_{{{i+1}}}={rho} \\xrightarrow{{{move_type}}}$ {next_node}"
                else:
                    trans_str = f"$\\xrightarrow{{{move_type}}}$ {next_node}"
            else:
                trans_str = "—"

            init_v = f"{init_vals[i]:.2f}"

            if i < len(updated_vals) and updated_vals[i] is not None:
                upd_v = f"{updated_vals[i]:.3f}"
            else:
                # Terminal state retains constant value, as do states that weren't updated due to exploratory move.
                upd_v = "—"

            row = [str(i), f"`{state}`", trans_str, init_v, upd_v]
            md_lines.append("| " + " | ".join(row) + " |")

        md_lines.append("\n---\n")

    return "\n".join(md_lines)


def generate_latex(episodes_data: list) -> str:
    """Generates LaTeX math array code corresponding to the simulated episodes data.

    Matches the quiz solution array formatting style using custom macros (\\xrB, \\xrE).
    """
    latex_lines = [
        r"\begin{displaymath}",
        r"\begin{array}{ccccccccccccccc}",
    ]

    for ep_idx, ep_data in enumerate(episodes_data, start=1):
        path = ep_data["path"]
        transitions = ep_data["transitions"]
        init_vals = ep_data["init_vals"]
        updated_vals = ep_data["updated_vals"]

        # Row 1: Episode label and Path with Transition Arrows
        path_cells = [
            rf"\text{{episode {ep_idx}}}" if ep_idx > 1 else r"\text{episode 1}"]

        # Keep track of sequential random number indexing across the whole run
        for i, state in enumerate(path):
            path_cells.append(state)
            if i < len(transitions):
                _, _, rho, move_type = transitions[i]
                macro = rf"\xr{move_type}"
                if rho is not None:
                    # e.g., \rho_1=0.88 \xrB
                    path_cells.append(rf"\rho_{{{i+1}}}={rho} {macro}")
                else:
                    path_cells.append(macro)

        row_path = " & ".join(path_cells) + r" \\"

        # Row 2: Initial State Values
        init_cells = [""]  # Align empty under "episode N"
        for i, val in enumerate(init_vals):
            init_cells.append(f"{val:.2f}" if isinstance(
                val, float) else str(val))
            if i < len(transitions):
                init_cells.append("")  # Empty cell under arrow column

        row_init = " & ".join(init_cells) + r" \\"

        # Row 3: Updated State Values (Non-terminal)
        upd_cells = [""]
        for i in range(len(path)):
            if i < len(updated_vals):
                val = updated_vals[i]
                if val is not None:
                    upd_cells.append(f"{val:.3f}".rstrip("0").rstrip("."))
                else:
                    # Value was not updated due to exploratory move
                    upd_cells.append("")
            else:
                upd_cells.append("")  # Terminal node doesn't update in table

            if i < len(transitions):
                upd_cells.append("")  # Empty cell under arrow column

        # Strip trailing empty cells for cleaner LaTeX
        while upd_cells and upd_cells[-1] == "":
            upd_cells.pop()

        row_upd = " & ".join(upd_cells) + r" \\"

        # Combine episode rows
        latex_lines.append(row_path)
        latex_lines.append(row_init)
        latex_lines.append(row_upd)

        # Spacer between episodes
        if ep_idx < len(episodes_data):
            latex_lines.append(r" \\")

    latex_lines.append(r"\end{array}")
    latex_lines.append(r"\end{displaymath}")

    return "\n".join(latex_lines)


def main():
    """Main function to parse arguments, run simulations, and generate outputs."""
    parser = argparse.ArgumentParser(
        description="Simulate value learning episodes and generate outputs.")
    parser.add_argument("-t", "--toml", type=str, default=DEFAULT_GRAPH_FILE,
                        help="Path to the TOML file containing graph structure and initial values.")
    parser.add_argument("-eps", "--epsilon", type=float,
                        help="Exploration probability.")
    parser.add_argument("-eta", "--eta", type=float,
                        help="Learning rate for TD updates.")
    args = parser.parse_args()

    toml_path = Path(args.toml)
    if args.toml == DEFAULT_GRAPH_FILE and not toml_path.exists():
        toml_path.write_text(DEFAULT_GRAPH_CONTENT, encoding="utf-8")
        print(
            f"Default TOML file '{DEFAULT_GRAPH_FILE}' created with sample graph structure and values.")

    edges, values, hardwired_rng_seq = parse_graph_toml(toml_path)
    epsilon = args.epsilon if args.epsilon is not None else 0.3
    eta = args.eta if args.eta is not None else 0.1
    sim_data = simulate_episodes(
        edges, values, hardwired_rng_seq, epsilon=epsilon, eta=eta)

    md_output = generate_markdown(sim_data)
    latex_output = generate_latex(sim_data)

    # Print Markdown to console
    print(md_output)

    # Save to files
    Path("episodes_output.md").write_text(md_output, encoding="utf-8")
    Path("episodes_output.tex").write_text(latex_output, encoding="utf-8")


if __name__ == "__main__":
    main()
