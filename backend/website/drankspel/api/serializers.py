from rest_framework import serializers


class CamelCaseSerializer(serializers.Serializer):
    """Camel Case Serializer."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the CamelCaseSerializer.

        Needed for Google DialogFlow parsers.
        """
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.field_name = CamelCaseSerializer._to_camel_case(field.field_name)

    @staticmethod
    def _to_camel_case(text):
        """Convert a piece of text to camel case."""
        s = text.replace("-", " ").replace("_", " ")
        s = s.split()
        if len(text) == 0:
            return text
        return s[0] + "".join(i.capitalize() for i in s[1:])


class DialogflowResponseSerializer(CamelCaseSerializer):
    """Dialogflow Response serializer."""

    fulfillment_text = serializers.CharField(source="fullfillmentText")
