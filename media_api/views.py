from rest_framework.views import APIView
from rest_framework.response import Response


class UploadMediaView(APIView):
    def post(self, request):
        return Response({"message": "Upload API"})


class DeleteMediaView(APIView):
    def delete(self, request):
        return Response({"message": "Delete API"})