# 🦈 Shark AI Agent - Autonomous CLI Assistant

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Gemini API](https://img.shields.io/badge/Google%20GenAI-Gemini%202.0%20Flash-orange.svg)
![uv](https://img.shields.io/badge/Package%20Manager-uv-purple.svg)

A command-line interface (CLI) Artificial Intelligence agent capable of reasoning, interacting with the local file system, modifying code, and testing its own solutions. Built using the Google Gemini API and the "Agent Loop" design pattern with Function Calling.

##  Key Features

* **Reasoning Loop (Agent Loop):** The agent doesn't just respond to prompts; it maintains a conversation history and tool execution record, allowing it to iterate on a problem until it's solved (capped at 20 iterations to protect API resources).
* **Tool Calling:** Seamless integration between the LLM's intents and native Python executable functions.
* **System Interaction:**
    *  `get_files_info`: Inspects working directories.
    *  `get_file_content`: Reads the content of specific files.
    *  `write_file`: Creates or overwrites files with corrected code.
    *  `run_python_file`: Executes local scripts (like test suites) to self-verify solutions.
* **Auto-Debugging:** The agent can take a prompt like "Fix this bug", locate the broken file, rewrite the logic, and run tests until victory is confirmed.

##  Prerequisites

* Python 3.10 or higher.
* [`uv`](https://docs.astral.sh/uv/) (The blazingly fast Python package manager written in Rust).
* A valid Google Gemini API Key (from Google AI Studio).

##  Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/agent-shark-ia.git](https://github.com/yourusername/agent-shark-ia.git)
   cd agent-shark-ia
   ```

2. **Create the virtual environment and install dependencies:**
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the root of the project and add your API Key:
   ```env
   GEMINI_API_KEY=YOUR_API_KEY_HERE
   ```

##  Usage

To run the agent, use the `uv run` command passing your prompt as an argument. You can add the `--verbose` flag to see the agent's thought process and execution step-by-step.

**Basic Example:**
```bash
uv run main.py "what files are in the root?" --verbose
```

**Advanced Example (Auto-code repair):**
```bash
uv run main.py "Fix the precedence bug in the calculator app. 3 + 7 * 2 shouldn't be 20." --verbose
```

### Expected Output (Verbose Mode)
```text
User prompt: Fix the precedence bug...
--- Iteration 1 ---
 - Calling function: get_files_info
-> ['calculator.py', 'main.py', 'tests.py']
--- Iteration 2 ---
 - Calling function: get_file_content
-> [Content of calculator.py]
--- Iteration 3 ---
 - Calling function: write_file
-> File updated successfully
--- Iteration 4 ---
 - Calling function: run_python_file
-> Ran 9 tests. OK.

Final response:
I have successfully identified the PEMDAS bug in `calculator.py` where the addition operator had a higher precedence than multiplication. I updated the dictionary, ran the tests, and everything is passing now.
```

##  Project Structure

* `main.py`: CLI entry point, contains the GenAI client configuration and the core **Agent Loop**.
* `call_function.py`: The "Dispatcher" mapping the AI's tools (Function Declarations/Schemas) to executable Python functions.
* `prompts.py`: System Instructions defining the agent's personality and strict rules of engagement.
* `functions/`: Directory containing the pure logic of the tools (`write_file.py`, `get_files_info.py`, etc.).
* `calculator/`: Dummy application (broken app) used as a sandbox for the agent to repair.

## ⚠️ Notes on API Limits
This project uses the Gemini Free Tier. If you make too many complex requests or loops in a short period, you might encounter `429 RESOURCE_EXHAUSTED` errors. It is recommended to space out your tests or use a billing-enabled account (Pay-as-you-go) for intensive workloads.

---
*Built with blood, sweat, tears, and a lot of bypassed Rate Limits.* 
