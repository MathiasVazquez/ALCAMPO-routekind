
from kind.customauth.models import TemporalPassword
from kind.generics.serializers.base_seriaizer import BaseSerializer


class TemporalPasswordSerializer(BaseSerializer):
    
    class Meta:
        fields = [
            'id',
            'user',
            'status',
            'status_label',
        ]
        model = TemporalPassword