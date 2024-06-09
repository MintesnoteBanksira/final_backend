from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image
from django.http import HttpResponse
from ultralytics import YOLO
import io
import os
import uuid

class DetectView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load the model
        self.model = YOLO("/Users/mintesnotebanksirabiza/Desktop/web/best.pt")

    def post(self, request, *args, **kwargs):
        # Get the image from the request
        image2 = request.FILES['image']

        # Generate a unique filename for the image
        image_filename = f'{uuid.uuid4()}.jpg'

        # Convert .webp to .jpg if necessary
        if image2.name.endswith('.webp'):
            image = Image.open(image2)
            image = image.convert('RGB')
            image.save(image_filename, 'jpeg')
        else:
            # Save the image to a file in the current directory
            with open(image_filename, 'wb+') as destination:
                for chunk in image2.chunks():
                    destination.write(chunk)

        # Run inference on the image and save the result
        result = self.model.predict(image_filename, save=True, imgsz=320, conf=0.25)
      
        save_dir = result[0].save_dir

        save_dir = f'/Users/mintesnotebanksirabiza/Desktop/web/object_detection/{save_dir}/{image_filename}'
        print(save_dir)
        # Open the saved image file
        with open(save_dir, 'rb') as f:
            image_data = f.read()

        # Delete the temporary image file
        os.remove(image_filename)

        # Return the image data in the HTTP response
        return HttpResponse(image_data, content_type="image/jpg")
    
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

class CustomLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        username = request.data.get('username')
        print(username)
        password = request.data.get('password')
        print(password)
        logger.debug(f'Username: {username}')
        logger.debug(f'Password: {password}')

        if not username or not password:
            return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        logger.debug(f'Authenticated user: {user}')

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
