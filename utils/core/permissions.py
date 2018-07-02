import logging
import traceback

from django.contrib.auth.models import User, Group
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

logger = logging.getLogger(__name__)


class IsOperator(BasePermission):
    """
    仅允许操作员.
    """

    def has_permission(self, request, view):
        try:
            return request.user.groups.get().name == 'Operator'
        except (AttributeError, Group.DoesNotExist, Group.MultipleObjectsReturned):
            logger.error(traceback.format_exc())
