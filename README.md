# Smart Home Agent LLM

## 🚀 Project Overview
This repository contains the decision-making logic for a simulated home robot. The project involves replacing a basic, hardcoded mock agent with a dynamic Large Language Model (Google's Gemini 2.5 Flash) to process natural language commands. The agent interprets plain English instructions, factors in the current state of its environment, and generates strict, actionable JSON execution plans for the robot to follow.

## 🛠️ Core Capabilities
The agent's logic is heavily engineered to handle edge cases and operate safely within a simulated home environment.

### 1. Contextual Grounding
* **Design Philosophy:** The robot must not hallucinate actions.
* **Optimization:** Before executing any move or pickup command, the LLM actively cross-references the user's request with its known environmental state, refusing to interact with objects or locations that do not exist.

### 2. Safety Guardrails
* **Design Philosophy:** A home robot must prioritize user and environmental safety.
* **Optimization:** Strict system prompts govern the model, ensuring it identifies and explicitly refuses dangerous requests (e.g., handling kitchen knives or hazardous materials) using a built-in verbal response system.

### 3. Ambiguity Resolution & Recovery
* **Design Philosophy:** No blind guessing. Hardware fails.
* **Optimization:** Vague commands (e.g., "get me something to drink") trigger the agent to ask clarifying questions. Furthermore, the physical execution loop includes hardware failure detection, safely halting operations if the simulated robot drops an item or malfunctions.

## 📊 Technical Implementation
* **Language & API:** Python, `google-generativeai` SDK.
* **Prompt Engineering:** Utilizes a highly structured system prompt enforcing JSON-only output and strict adherence to the robot's specific skill constraints (`Maps_to`, `pick`, `place`, `speak`).
* **Rate Limit Handling:** Features a custom retry loop with exponential backoff (`time.sleep`) to gracefully manage API quota limits during rapid testing cycles.

## 🔧 Installation & Usage
1. **Requirements:**
   - Python 3.x
   - Install dependencies via `pip install -r requirements.txt`

2. **Environment Setup:**
   - Create a `.env` file in the root directory.
   - Add your Gemini API key: `GEMINI_API_KEY=your_key_here`

3. **Running the Simulation:**
   - **Interactive GUI Mode:** Run `python run.py --gui` to open the visual simulator and issue plain text commands.
   - **Automated Testing:** Run `python run.py --test` to evaluate the agent against a suite of complex edge cases (ambiguous, unsafe, out-of-scope, and multi-step commands).

## ✍️ Author
* **Name:** Raj Fatehveer Singh Brar
* **Email ID:** rbrar_be23@thapar.edu
* **University:** Thapar Institute of Engineering and Technology
