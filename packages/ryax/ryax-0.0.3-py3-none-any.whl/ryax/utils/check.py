from pathlib import Path


def discover_action_dirs(to_dir: Path) -> list[Path]:
    collected_action_dirs = []
    for p in to_dir.rglob("*"):
        if p.name == "ryax_handler.py" or p.name == "ryax_run.py":
            collected_action_dirs.append(p.absolute().parent)
    nested_actions = []
    for action_dir in collected_action_dirs:
        for check_dir in collected_action_dirs:
            if action_dir == check_dir:
                continue
            if action_dir.is_relative_to(check_dir):
                nested_actions.append(action_dir)
                print(f"Warning: found nested action at {action_dir}. Skipping.")

    return [
        action_dir
        for action_dir in collected_action_dirs
        if action_dir not in nested_actions
    ]
