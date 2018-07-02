from django.shortcuts import render

from firewall.models import Firewall
from firewall.serializers import FirewallSerializer, FirewallCreateSerializer
from utils.core.mixins import MultiPermissionViewSetMixin, MultiSerializerViewSetMixin
from rest_framework.mixins import CreateModelMixin,ListModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet,ReadOnlyModelViewSet
# Create your views here.


class FirewallDeviceView(MultiPermissionViewSetMixin, MultiSerializerViewSetMixin,
                         CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    a = 'hello'
    serializer_class = FirewallSerializer
    serializer_action_classes = {
        'list': FirewallSerializer,
        'retrieve': FirewallSerializer,
        'create': FirewallCreateSerializer
    }
    queryset = Firewall.objects.all()

