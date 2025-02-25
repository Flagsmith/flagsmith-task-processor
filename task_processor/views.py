from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from task_processor.monitoring import get_num_waiting_tasks
from task_processor.serializers import MonitoringSerializer


@swagger_auto_schema(method="GET", responses={200: MonitoringSerializer()})
@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def monitoring(request, **kwargs):
    return Response(
        data={"waiting": get_num_waiting_tasks()},
        headers={"Content-Type": "application/json"},
    )
