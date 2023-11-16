from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "name": user.get_full_name(),
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "roles": user.get_all_permissions(),
        }
        return Response(data)
