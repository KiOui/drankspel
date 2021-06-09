def get_intent_by_name(intent_list: list, intent_name: str):
    """Get an intent by name from an intent list."""
    for intent in intent_list:
        if intent.display_name == intent_name:
            return intent
    return None
