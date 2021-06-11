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

    def create(self, validated_data):
        """Create method."""
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update method."""
        return super().update(instance, validated_data)

    @staticmethod
    def _to_camel_case(text):
        """Convert a piece of text to camel case."""
        s = text.replace("-", " ").replace("_", " ")
        s = s.split()
        if len(text) == 0:
            return text
        return s[0] + "".join(i.capitalize() for i in s[1:])


class DialogflowOutputContextSerializer(CamelCaseSerializer):
    """Dialogflow Output Context serializer."""

    name = serializers.CharField()
    # parameters = DialogflowParameterSerializer()


class DialogflowIntentSerializer(CamelCaseSerializer):
    """Dialogflow Intent serializer."""

    name = serializers.CharField()
    display_name = serializers.CharField(source="displayName")


class DialogflowQuerySerializer(CamelCaseSerializer):
    """Dialogflow Query serializer."""

    query_text = serializers.CharField(source="queryText")
    # parameters = DialogflowParameterSerializer()
    all_required_params_present = serializers.BooleanField(source="allRequiredParamsPresent")
    output_contexts = DialogflowOutputContextSerializer(many=True, source="outputContexts")
    intent = DialogflowIntentSerializer()
    intent_detection_confidence = serializers.FloatField(source="intentDetectionConfidence")
    language_code = serializers.CharField(source="languageCode")


class DialogflowRequestSerializer(CamelCaseSerializer):
    """Dialogflow Request serializer."""

    response_id = serializers.CharField(source="responseId")
    query_result = DialogflowQuerySerializer(many=False, source="queryResult")
    # original_detect_intent_request
    session = serializers.CharField()


class DialogflowResponseSerializer(CamelCaseSerializer):
    """Dialogflow Response serializer."""

    fulfillment_text = serializers.CharField(source="fullfillmentText")
