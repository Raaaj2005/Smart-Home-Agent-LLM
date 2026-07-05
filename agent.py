import json

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
        self.current_state = "READY"
        self.pending_action = None
        self.fetch_words = ["bring", "get", "fetch", "grab", "need", "take", "move"]
        self.drinks = {"water": "water_bottle", "juice": "juice_box"}
        self.reading_material = {"book": "book", "newspaper": "newspaper"}
        self.danger_words = ["knife", "scissors", "fire"]
        self.object_homes = {
            "water_bottle": "kitchen_counter",
            "juice_box": "kitchen_counter",
            "book": "living_room",
            "newspaper": "dining_table"
        }

    def handle(self, command):
        text = command.lower()

        for danger in self.danger_words:
            if danger in text:
                self.robot.speak("I cannot handle dangerous objects for safety reasons.")
                self.reset_memory()
                return

        if self.current_state == "WAITING_FOR_DRINK":
            target = self.find_target(text, self.drinks)
            if target:
                self.execute_fetch_plan(target, text)
                self.reset_memory()
            else:
                self.robot.speak("I don't recognize that drink. Try water or juice.")
            return

        is_fetch_request = any(word in text for word in self.fetch_words)
        
        if is_fetch_request:
            target_drink = self.find_target(text, self.drinks)
            target_book = self.find_target(text, self.reading_material)
            
            target = target_drink or target_book

            if not target and "drink" in text:
                self.current_state = "WAITING_FOR_DRINK"
                self.robot.speak("What would you like to drink? I can get water or juice.")
                return
            elif not target:
                self.robot.speak("I understand you want me to get something, but I don't know what it is.")
                return
            
            self.execute_fetch_plan(target, text)
            return

        self.robot.speak("I am sorry, I don't understand that command.")

    def find_target(self, text, category_dictionary):
        for word, actual_object_name in category_dictionary.items():
            if word in text:
                return actual_object_name
        return None

    def execute_fetch_plan(self, target_object, user_text):
        origin = self.object_homes.get(target_object, "kitchen_counter")
        destination = "living_room"
        
        if "bedroom" in user_text:
            destination = "bedroom"
        elif "kitchen" in user_text:
            destination = "kitchen_counter"

        plan = [
            {"action": "navigate_to", "arg": origin}, 
            {"action": "pick", "arg": target_object},
            {"action": "navigate_to", "arg": destination},
            {"action": "place", "arg": destination},
            {"action": "speak", "arg": f"Here is your {target_object.replace('_', ' ')}."}
        ]
        
        for step in plan:
            fn = getattr(self.robot, step.get("action"), None)
            if fn:
                result = fn(step.get("arg"))
                print("  ", result)
                
                result_str = str(result).lower()
                if result is False or result is None or "fail" in result_str or "not sensed" in result_str or "not holding" in result_str:
                    self.robot.speak("I encountered a hardware failure or missing object. Stopping.")
                    break

    def reset_memory(self):
        self.current_state = "READY"
        self.pending_action = None