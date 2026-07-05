# Smart Home Agent LLM

## 🚀 Project Overview
This repository contains the decision-making logic for a simulated home robot. Moving away from black-box LLM APIs (like OpenAI or Gemini), this project implements a custom **Classical AI Rule-Based Engine** built entirely in Python. It utilizes a Finite State Machine (FSM) and keyword-based entity extraction to process plain English commands, resolve ambiguities, and dynamically trigger physical hardware functions within a simulated environment.

## 🧠 Architectural Highlights
This agent is built for 100% local execution, zero latency, and absolute deterministic control over the robot's actions.

### 1. Stateful Memory (FSM)
* **The Challenge:** Vague commands (e.g., "Get me a drink") usually cause stateless logic to fail. 
* **The Solution:** Implemented a short-term memory system using a finite state machine (`current_state`). If a command is ambiguous, the agent flags itself as waiting for clarification, asks the user a follow-up question, and seamlessly combines the previous context with the user's new input.

### 2. Entity Mapping & Grounding
* **The Challenge:** Translating messy human language into strict robotic parameters.
* **The Solution:** Utilizes highly efficient Python dictionaries to map natural language synonyms (e.g., "water", "juice") directly to physical simulation targets (e.g., `water_bottle`). It also hardcodes environmental grounding, matching specific items to their native coordinates (e.g., newspapers live on the `dining_table`).

### 3. Dynamic Dispatch & Recovery
* **The Challenge:** Hardcoding `if/else` statements for every physical movement is inefficient and brittle.
* **The Solution:** Uses Python's `getattr` to dynamically parse intended actions into callable simulator functions. Furthermore, a strict hardware-recovery loop intercepts failure states (e.g., dropping an item or failing to sense a target), safely halting execution and providing verbal feedback instead of blindly completing a broken task.

### 4. Safety Guardrails
* **The Challenge:** Preventing hazardous interactions in a home environment.
* **The Solution:** An array-driven filtering system intercepts dangerous keywords (e.g., "knife", "fire") at the absolute beginning of the execution pipeline, completely blocking the physical logic sequence.

## 📊 Technical Stack
* **Language:** Python 3.x
* **Core Logic:** Finite State Machines, Dictionary Mapping, Dynamic Dispatch (`getattr`)
* **Dependencies:** None (Zero external API reliance)

## 🔧 Installation & Usage
1. **Requirements:**
   - Python 3.x
   - Install dependencies via `pip install -r requirements.txt` (for the simulator UI)

2. **Running the Simulation:**
   - **Interactive GUI Mode:** Run `python run.py --gui` to open the visual simulator and issue plain text commands. Try triggering the state machine by typing: *"Get me a drink."*
   - **Automated Testing:** Run `python run.py --test` to evaluate the agent against a suite of complex edge cases (ambiguous, unsafe, missing objects, and multi-step commands).

## ✍️ Author
* **Name:** Raj Fatehveer Singh Brar
* **Email ID:** rbrar_be23@thapar.edu
* **University:** Thapar Institute of Engineering and Technology
