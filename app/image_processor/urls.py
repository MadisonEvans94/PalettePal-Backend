from django.urls import path
from .views import process_image
# TODO: fix urls to be restful

urlpatterns = [
    path('image-processor/', process_image, name='image_upload'),
    # GET request to retrieve all palettes
    #     path('palettes/', get_user_palettes, name='get_user_palettes'),
    #     # POST request to create a new palette
    #     # path('palettes/', create_palette, name='create_palette'),
    #     path('palettes/create/', create_palette, name='create_palette'),

    #     # PUT request to update a specific palette
    #     path('palettes/update/<int:palette_id>/',
    #          update_palette, name='update_palette'),
    #     # DELETE request to delete a specific palette
    #     path('palettes/delete/<int:palette_id>/',
    #          delete_palette, name='delete_palette'),
]
