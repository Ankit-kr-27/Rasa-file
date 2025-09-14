from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re

# Database of diseases and their symptoms
DISEASE_DB = {
    "dengue": ["fever", "headache", "joint pain", "muscle pain", "rash", "nausea", "vomiting"],
    "malaria": ["fever", "chills", "sweating", "headache", "nausea"],
    "common_cold": ["cough", "sore throat", "runny nose", "sneezing"],
}

# Disease prevention tips
PREVENTION_DB = {
    "dengue": "Eliminate standing water, use mosquito repellents, wear full-sleeve clothes, and use mosquito nets.",
    "malaria": "Use mosquito nets, take antimalarial precautions, and avoid mosquito bites.",
    "common_cold": "Wash hands regularly, avoid close contact with sick people, and maintain hygiene.",
}

class ActionPredictDisease(Action):

    def name(self) -> Text:
        return "action_predict_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_msg = tracker.latest_message.get('text', '').lower()
        predicted_diseases = []

        # Normalize the message (remove punctuation)
        user_msg_clean = re.sub(r'[^\w\s]', '', user_msg)

        for disease, symptoms in DISEASE_DB.items():
            for symptom in symptoms:
                # Use word boundary matching to catch similar phrases
                if re.search(rf'\b{re.escape(symptom.lower())}\b', user_msg_clean):
                    predicted_diseases.append(disease)
                    break  # Avoid duplicate addition

        if predicted_diseases:
            response = ""
            for disease in predicted_diseases:
                response += f"You might have {disease.capitalize()}. Prevention: {PREVENTION_DB[disease]}\n\n"
            response += "⚠ Please consult a doctor for proper diagnosis and treatment."
        else:
            response = "Sorry, I couldn't predict the disease based on these symptoms. ⚠ Please consult a doctor."

        dispatcher.utter_message(text=response)
        return []
