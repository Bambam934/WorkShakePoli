from django.urls import path
from . import views

urlpatterns = [
     path("", views.perfilView, name="Perfil"),                 # GET  /perfil/
     path("upload-profile-picture/", views.upload_profile_picture,
          name="upload_profile"),                               # POST /perfil/upload-profile-picture/
     path("update-color/", views.update_neon_color,
          name="update_neon_color"),                            # POST
     path("equip-skin/<int:skin_id>/", views.equip_skin,
          name="equip_skin"),                                   # POST
]
