from rest_framework import serializers
from .models import Campagne


class CampagneSerializer(serializers.HyperlinkedModelSerializer):
    info_grume = serializers.SerializerMethodField()

    class Meta:
        model = Campagne
        fields = ['entreprise', 'info_grume']


    def get_info_grume(self, obj):
        return_data = None
        if type(obj.info_grume) == list:
            embedded_list = []
            for item in obj.info_grume:
                embedded_dict = item.__dict__
                for key in list(embedded_dict.keys()):
                    if key.startswith('_'):
                        embedded_dict.pop(key)
                embedded_list.append(embedded_dict)
            return_data = embedded_list
        else:
            embedded_dict = obj.info_grume.__dict__
            for key in list(embedded_dict.keys()):
                if key.startswith('_'):
                    embedded_dict.pop(key)
            return_data = embedded_dict
            return return_data
        return return_data
