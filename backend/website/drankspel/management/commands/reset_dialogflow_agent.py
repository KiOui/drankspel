from django.core.management.base import BaseCommand
from dialogflow_v2.gapic.intents_client import IntentsClient
from django.conf import settings

from drankspel.services import get_intent_by_name
from drankspel.dialogflow.services import intent_manager


class Command(BaseCommand):
    """Command to reset the Dialogflow agent."""

    help = "Reset the Dialogflow agent"

    def add_arguments(self, parser):
        """Add arguments."""
        parser.add_argument(
            "-f", "--force", action="store_true", help="Whether or not to override intents (if already created)."
        )

    def _add_intents(self, force):
        client = IntentsClient.from_service_account_file(settings.GOOGLE_CREDENTIALS_FILE)
        parent = client.project_agent_path(settings.GOOGLE_AGENT_NAME)
        intents = client.list_intents(parent)
        for intent_name, intent in intent_manager.intents.items():
            existing_intent = get_intent_by_name(intents, intent_name)
            if existing_intent is not None or force:
                if existing_intent is not None:
                    print("Removing intent '{}'".format(intent_name))
                    client.delete_intent(existing_intent.name)
                print("Creating '{}' intent".format(intent_name))
                client.create_intent(parent, intent.to_dict())
                print("'{}' intent created successfully".format(intent_name))
            else:
                print(
                    "Skipping adding intent '{}' because it already exists (run with --force to "
                    "override)".format(intent_name)
                )

    def handle(self, *args, **kwargs):
        """Handle the command."""
        force = kwargs.get("force")
        self._add_intents(force)
