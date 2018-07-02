from rest_framework import status
from django.utils import timezone
from django.conf import settings


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        """
        在self.serializer_action_classes中找对应的serializer，self.serializer_action_classes
        是一个dict，映射action name(key)到serializer class(value)
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        如果没有找到action的入口，则回退到常规的get_serializer_class
        lookup: self.serializer_class, MyDefaultSerializer.

        Thanks gonz: http://stackoverflow.com/a/22922156/11440

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()


class MultiPermissionViewSetMixin(object):
    def get_permission_class(self):
        """
        在self.permission_action_classes中找对应的permission，self.permission_action_classes
        是一个dict，映射action name(key)到permission class(value)
        i.e.:

        class MyViewSet(MultiPermissionViewSetMixin, ViewSet):
            permission_class = MyDefaultPermission
            permission_action_classes = {
               'list': MyListPermission,
               'my_action': MyActionPermission,
            }

            @action
            def my_action:
                ...

        如果没有找到action的入口，则回退到常规的get_permission_class
        lookup: self.permission_class, MyDefaultPermission.

        Thanks gonz: http://stackoverflow.com/a/22922156/11440

        """
        try:
            return self.permission_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiPermissionViewSetMixin, self).get_permission_class()

