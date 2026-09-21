#Python - Browser Automation with Playwright
This project is a Python-based browser automation template using the RPA Framework and Playwright. It provides a structured environment for automating browser tasks, including checkpointing and table handling.

#Project Overview
This project automates tasks on the QA Practice website (https://qa-practice.razvanvancea.ro) using Playwright for browser automation. It includes features like:

Checkpointing: Save and load task progress using a state file (output/state.json).
Table Handling: Read and manipulate tables from CSV files.
Browser Automation: Perform browser interactions such as navigation, form filling, and more.
#Project Structure
tasks.py: Main script containing the automation logic.
robot.yaml: Configuration file for running tasks and managing the environment.
output: Directory for storing logs, state files, and other outputs.
conda.yaml: Defines the Python environment and dependencies.
Running the Automation
Prerequisites
Install Robocorp CLI.
Ensure you have Python and Conda installed on your system.
Steps to Run
Install dependencies:
Run the automation task:
Results
After running the automation, check the following outputs:

Logs: log.html
State File: state.json
CSV Outputs: csv
Checkpointing
The project uses checkpointing to save and resume progress:

State File: state.json
Functions:
load_state(): Load the current state.
save_state(state): Save the current state.
mark_done(state, step_name): Mark a step as completed.
is_done(state, step_name): Check if a step is completed.
Dependencies
Dependencies are managed using conda.yaml. This ensures a consistent Python environment across machines.

Key Libraries
RPA Framework: For browser automation and table handling.
Playwright: For browser interactions.
JSON: For state management.
#.  Development
VS Code Setup
Install the Robocorp VS Code Extension.
Use the extension for running, debugging, and managing tasks.
#.  Directory Structure
.gitignore
.vscode/
conda.yaml
output/
tasks.py
robot.yaml
README.md


Additional Resources
Robocorp Documentation
RPA Framework
Playwright Documentation
