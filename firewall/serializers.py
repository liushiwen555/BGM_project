from rest_framework import serializers
from firewall.models import Firewall


class FirewallSerializer(serializers.ModelSerializer):
    responsible_user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Firewall
        fields = ('id', 'dev_name', 'ip', 'version', 'responsible_user', 'status')


class FirewallCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Firewall
        fields = ('dev_name', 'dev_code', 'dev_location', 'responsible_user')
