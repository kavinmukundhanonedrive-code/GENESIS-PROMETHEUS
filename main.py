from core.native_brain import NativeBrain
from core.task_manager import TaskManager


def main() -> None:
    task_manager = TaskManager()
    native_brain = NativeBrain(task_manager)

    task_id = native_brain.plan(
        title="Bootstrap project foundation",
        description="Create the initial architecture and task orchestration backbone.",
    )
    native_brain.delegate(task_id, "native")

    print("GENESIS PROMETHEUS booted successfully.")
    print(f"Task created: {task_id}")


if __name__ == "__main__":
    main()
