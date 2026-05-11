# Automating Data Cleaning with Shell and Python

## Project Description

In this project, you will build a **multi-stage data automation pipeline** using the Unix shell and Python.

You will take a folder of messy JSON files, organize them, validate their contents, clean and normalize the data, and finally merge everything into a single dataset ready for analysis or machine learning.

This project mirrors real-world data engineering workflows where automation, validation, and traceability are critical.

---

## Getting Started

These instructions will help you run the project locally using the provided starter files.

### Prerequisites

You should already be comfortable with:
- Basic Python programming
- Running commands in a Unix shell (Linux or macOS)

> ⚠️ This project is designed for **Unix-based shells** (Linux/macOS).  
> Windows Command Prompt and PowerShell are not supported.

---

### Dependencies

Python 3.8+
pandas

Shell scripts rely only on standard Unix utilities.

### Installation

1.	Clone or download the project starter repository.
2.	Open a terminal and navigate into the project directory.
3.	Install Python dependencies: `pip3 install -r requirements.txt` (**Only if pandas is not already installed on the env**)
4.  Make shell scripts executable: `chmod +x *.sh`

## Testing

This project does not include automated unit tests.

Instead, correctness is verified by running the pipeline and inspecting the outputs produced at each stage.

### Break Down Tests

You should manually verify that:

- Files are copied from json_dump/ to raw/ with cleaned filenames (json_dump/ is unchanged)
-	Invalid JSON files are routed to the invalid/ folder
-	Cleaned JSON files are written to the clean/ folder
-	Original processed files are copied to the archive/ folder after processing
-	A final CSV dataset is created in the dataset/ folder
-	Log files are written to the logs/ folder with filename as current date

These checks reflect how many real-world data pipelines are validated in practice.

## Project Instructions

> **Do not manually move files between folders.** All file movement must be done through scripts.

> **Re-runnable by design:** Every phase clears its output directory before writing and uses `cp` instead of `mv`. The `json_dump/` directory is never modified. If you make a mistake in any phase, simply fix your code and run it again.

For detailed step-by-step instructions for each phase, see the [Project Instructions](Instructions.md) page.

---

## Project Folder Structure and Pipeline Phases

- `json_dump/` — Phase 0: Incoming data. Raw input files as received. Never modified.
- `raw/` — Phase 1: Organized files after filename normalization.
- `invalid/` — Phase 2: Files that failed validation.
- `clean/` — Phase 3: Files with standardized and consistent structure.
- `archive/` — Phase 4: Copies of original files that were successfully processed.
- `dataset/` — Phase 5: Aggregated dataset ready for analysis.
- `logs/` — Cross-cutting: Execution logs for all pipeline steps.

## Built With

- Python – Core scripting language for validation and processing
- pandas – Used to merge cleaned data into a final dataset
- Bash – Used for file automation and orchestration
- Unix shell utilities – Standard tools for file navigation and scripting

## License

[License](LICENSE.txt)
