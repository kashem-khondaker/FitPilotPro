# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth.models import User
# from .serializers import UserProfileSerializer

# # Create your views here.
# # if request.user.groups.filter(name='STAFF').exists():

# class UserProfileView(APIView):
#     def get(self, request):
#         user = request.user
#         serializer = UserProfileSerializer(user)
#         return Response(serializer.data)

#     def put(self, request):
#         user = request.user
#         serializer = UserProfileSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data , status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request):
#         user = request.user
#         user.delete()
#         return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)