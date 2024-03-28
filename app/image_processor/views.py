# You need to create this serializer
# from django.shortcuts import get_object_or_404
# from .serializers import PaletteSerializer, ClusterDataSerializer
# from .models import Palette
# from rest_framework.permissions import IsAuthenticated
import io
from rest_framework.decorators import api_view, permission_classes
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from image_utils import image
from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import status
import base64
from io import BytesIO
# from django.contrib.auth.models import User
from django.core.files.images import ImageFile

# Configure logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([])
def process_image(request):
    image_file = request.FILES.get('image')
    if image_file:
        # Ensure the file is an InMemoryUploadedFile and convert it to BytesIO
        if isinstance(image_file, InMemoryUploadedFile):
            image_bytes_io = io.BytesIO(image_file.read())
            try:
                clusters, cluster_sizes = image.process_clusters(image_bytes_io)
                return Response({
                    "message": "Received image",
                    "clusters": clusters,
                    "ratio": cluster_sizes
                })
            except Exception as e:
                return Response({"error": f"Error processing image: {str(e)}"}, status=500)
    else:
        return Response({"error": "No image file provided"}, status=400)

# @api_view(['GET'])
# @permission_classes([])
# def get_user_palettes(request):
#     test_user = get_object_or_404(User, pk=32)
#     # user_palettes = Palette.objects.filter(
#     #     user=request.user).prefetch_related('cluster_data')
#     # serializer = PaletteSerializer(user_palettes, many=True)
#     # return Response(serializer.data)
#     # Use the test user to fetch palettes
#     user_palettes = Palette.objects.filter(
#         user=test_user).prefetch_related('cluster_data')
#     serializer = PaletteSerializer(user_palettes, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_palette(request):

#     serializer = PaletteSerializer(
#         data=request.data, context={'request': request})
#     if serializer.is_valid():
#         print("request received: ", request.data)
#         try:
#             palette = serializer.save(user=request.user)
#             logger.debug(f"Palette created successfully with id {palette.id}")
#             return Response(PaletteSerializer(palette).data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             # If something goes wrong while saving, log an error
#             logger.error(f"Error saving palette: {e}")
#             return Response({"error": "Error saving palette"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     else:
#         # Log validation errors
#         logger.warning(f"Validation errors: {serializer.errors}")
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_palette(request, palette_id):
#     try:
#         palette = Palette.objects.get(id=palette_id, user=request.user)
#     except Palette.DoesNotExist:
#         return Response({'error': 'Palette not found'}, status=status.HTTP_404_NOT_FOUND)

#     # Pass `partial=True` to allow partial updates
#     serializer = PaletteSerializer(palette, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_palette(request, palette_id):
#     try:
#         logger.debug("attempting deletion")
#         palette = Palette.objects.get(id=palette_id, user=request.user)
#     except Palette.DoesNotExist:
#         return Response({'error': 'Palette not found'}, status=status.HTTP_404_NOT_FOUND)

#     palette.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
