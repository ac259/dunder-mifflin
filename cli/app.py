import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Dunder Mifflin Agent Platform")
    parser.add_argument("--mode", choices=["cli", "tui"], default="tui", help="Run in CLI or Textual UI mode")
    args = parser.parse_args()

    current_dir = os.path.abspath(os.path.dirname(__file__))  # this is cli/
    project_root = os.path.abspath(os.path.join(current_dir, ".."))

    if args.mode == "cli":
        subprocess.run(["python", os.path.join(current_dir, "dunder_cli.py")])
    else:
        subprocess.run(["python", os.path.join(current_dir, "textual_ui.py")])

if __name__ == "__main__":
    main()
