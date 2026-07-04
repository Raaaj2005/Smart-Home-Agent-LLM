#This is the file you have to edit and submit in the end

import json
import os
import time
import google.generativeai as genai

genai.configure(api_key="GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"})


def call_llm(system, user):
    return mock_llm(system, user)


def mock_llm(system, user):
    u = user.lower()
    if "water" in u or "drink" in u or "thirsty" in u:
        return json.dumps({"plan": [
            {"action": "navigate_to", "arg": "kitchen_counter"},
            {"action": "pick", "arg": "water_bottle"},
            {"action": "navigate_to", "arg": "living_room"},
            {"action": "place", "arg": "living_room"},
            {"action": "speak", "arg": "Here is your water."},
        ]})
    return json.dumps({"plan": [{"action": "speak", "arg": "Okay."}]})


class Agent:
    def __init__(self, robot):
        self.robot = robot

    def handle(self, command):
        system_prompt = (
            "You control a home robot. Skills: navigate_to(location), "
            "pick(object), place(location), speak(text). "
            f"Locations: {self.robot.known_locations}. "
            "Rules: "
            "1. Grounding: Refuse to interact with unknown locations or objects. "
            "2. Safety: Refuse dangerous requests using speak. "
            "3. Ambiguity: Ask for clarification if unclear using speak. "
            "4. Confirmation: Always end a successful physical plan with a speak action. "
            "Reply ONLY with a raw JSON object. Do not include markdown formatting or conversational text. "
            "Format: {\"plan\":[{\"action\":\"...\",\"arg\":\"...\"}]}"
        )
        
        full_prompt = f"{system_prompt}\nUser Command: {command}"
        
        try:
            raw_text = ""
            for attempt in range(3):
                try:
                    response = model.generate_content(full_prompt)
                    raw_text = response.text.strip()
                    break
                except Exception as e:
                    if "429" in str(e) and attempt < 2:
                        print("  [API Rate Limit hit. Pausing for 3 seconds before retry...]")
                        time.sleep(3)
                    else:
                        raise e

            if raw_text.startswith("```json"):
                raw_text = raw_text[7:-3]
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:-3]
            
            raw_text = raw_text.strip()
                
            plan = json.loads(raw_text).get("plan", [])
            
        except Exception as e:
            print(f"\n[DEBUG ERROR] {str(e)}")
            self.robot.speak("Sorry, I encountered an error processing that request.")
            return

        for step in plan:
            fn = getattr(self.robot, step.get("action"), None)
            if fn is None:
                continue
            
            result = fn(step.get("arg"))
            print("  ", result)
            
            if result is False or result is None or (isinstance(result, str) and "fail" in result.lower()):
                self.robot.speak("I encountered a hardware failure. Stopping execution.")
                break
