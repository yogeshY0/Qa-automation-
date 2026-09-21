# TaskQA - Browser Automation & QA Practice

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Robocorp](https://img.shields.io/badge/Robocorp-RPA--Framework-FF4B4B?style=flat)
![Playwright](https://img.shields.io/badge/Playwright-Automated_Testing-45BA4B?style=flat&logo=playwright&logoColor=white)

A robust test automation suite built with **Robocorp** (`rpaframework`) and **Playwright**. This project demonstrates end-to-end web automation workflows, covering user authentication, dynamic data handling, pagination, and e-commerce checkout flows.

---

## 🚀 Features & Test Scenarios

- **E-Commerce Checkout Flow**: Automates user authentication, dynamic item selection, cart management, and order submission.
- **Dynamic Table Handling & Pagination**: Traverses multi-page tables dynamically while accurately handling disabled state controls.
- **Data Verification**: Interacts with dynamic DOM elements and validates extracted data against CSV sources.
- **Robocorp Task Management**: Structured execution using `tasks.py` and standard Robocorp configuration descriptors.

---

## 📁 Project Structure

```text
taskqa/
├── csv/                   # Input CSV datasets (dynamic_table.csv, static_table.csv)
├── output/                # Generated execution logs, screenshots, and traces
├── .gitignore             # Git ignore patterns
├── conda.yaml             # Conda environment definition & dependencies
├── README.md              # Project documentation
├── robot.yaml             # Robocorp configuration descriptor
└── tasks.py               # Automation task implementations
