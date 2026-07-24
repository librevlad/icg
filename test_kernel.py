import os
import sys

# Add C:\icg to python path for testing
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.graph import ICGGraph
from workspace.workspace import Workspace
from contracts.contract import Contract
from nodes.bash import BashNode
from nodes.gemini_cli import GeminiCLINode

def main():
    # 1. Initialize Workspace and Kernel
    workspace = Workspace("./test_workspace")
    kernel = ICGGraph(workspace=workspace, db_path=":memory:") # In-memory SQLite for testing

    # 2. Register Nodes (Executors)
    bash_node = BashNode()
    # Use a dummy echo command instead of real gemini cli for this test to avoid errors if gemini isn't installed
    gemini_node = GeminiCLINode(cli_command="echo") 

    kernel.register_node(bash_node, ["execution"])
    kernel.register_node(gemini_node, ["reasoning", "coding"])

    # 3. Create a Contract
    contract = Contract(
        id="task-123",
        task_description="List files in the current directory",
        requires=["execution"],
        inputs={"command": "dir" if os.name == 'nt' else "ls -la"}
    )

    # 4. Execute using the Kernel
    print(f"Requesting execution of contract: {contract.id}")
    try:
        results = kernel.execute(contract)
        print("\n--- Success ---")
        print("Execution Results:", results)
    except Exception as e:
        print("\n--- Failed ---")
        print(f"Error: {e}")

    # 5. Show that Memory recorded it
    print("\n--- Memory (History) ---")
    cursor = kernel.history.conn.cursor()
    cursor.execute("SELECT * FROM execution_history")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    print("\n--- Memory (Metrics) ---")
    cursor = kernel.metrics.conn.cursor()
    cursor.execute("SELECT * FROM node_metrics")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

if __name__ == "__main__":
    main()
