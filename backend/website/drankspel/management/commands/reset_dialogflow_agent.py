from django.core.management.base import BaseCommand
from dialogflow_v2.gapic.intents_client import IntentsClient
from django.conf import settings

from drankspel.services import get_intent_by_name


class ResetDialogflowCommand(BaseCommand):
    """Command to reset the Dialogflow agent."""

    help = "Reset the Dialogflow agent"

    def add_arguments(self, parser):
        """Add arguments."""
        parser.add_argument(
            "-f", "--force", action="store_true", help="Whether or not to override intents (if already created)."
        )

    def handle(self, *args, **kwargs):
        """Handle the command."""
        force = kwargs.get("force")
        client = IntentsClient.from_service_account_file(settings.GOOGLE_CREDENTIALS_FILE)
        parent = client.project_agent_path(settings.GOOGLE_AGENT_NAME)
        intents = client.list_intents(parent)
        existing_intent = get_intent_by_name(intents, "Random drinking game")
        if existing_intent is None or force:
            if existing_intent is not None:
                print("Removing intent 'Random drinking game'")
                client.delete_intent(existing_intent.name)
            random_drinking_game_intent = {
                "display_name": "Random drinking game",
                "webhook_state": True,
                "training_phrases": [{"parts": [{"text": settings.GOOGLE_INTENT_TRAINING_PHRASE}]}],
            }
            print("Creating 'Random drinking game' intent")
            client.create_intent(parent, random_drinking_game_intent)
            print("'Random drinking game' intent created successfully")
        else:
            print(
                "Skipping adding intent 'Random drinking game' because it already exists (run with --force to "
                "override)"
            )
