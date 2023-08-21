
from rest_framework import serializers


# class PlateFormConstDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PlatformConstantData
#         fields = '__all__'
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        except_ = kwargs.pop('except_', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if except_ is not None:
            # Drop any fields that are not specified in the `fields` argument.
            not_allowed = set(except_)
            existing = set(self.fields)
            for field_name in existing:
                if field_name in except_:
                    self.fields.pop(field_name)
