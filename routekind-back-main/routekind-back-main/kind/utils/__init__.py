
def create_dynamic_fields_serializer(serializer_class, fields):
    _fields = fields

    class DynamicFieldsSerializer(serializer_class):
        class Meta(serializer_class.Meta):
            fields = _fields
    return DynamicFieldsSerializer
