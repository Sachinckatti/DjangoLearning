from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class DynamicFieldSerializer(serializers.Serializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            field_set = set(fields)
            existing = set(self.fields)
            for field_name in field_set - existing:
                self.fields[field_name] = serializers.CharField(
                    max_length=1000, required=False
                )

class FooSerializer(DynamicFieldSerializer):
    x = serializers.IntegerField(required = True)
    y = serializers.IntegerField(required=False)

class QuestionSerializer(DynamicFieldSerializer):
    id = serializers.CharField(max_length=10)
    q_text = serializers.CharField(max_length=250)

