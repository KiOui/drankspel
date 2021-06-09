

def get_intent_by_name(intent_list: list, intent_name: str):
    for intent in intent_list:
        if intent.display_name == intent_name:
            return intent
    return None
