from django.urls import path

from . import views


app_name = "api"
urlpatterns = [
    # AttributeName Objects
    path("attribute_name_create/", views.AttributeNameCreateAPIView.as_view()),
    path(
        "attribute_name/<int:pk>/", views.AttributeNameGetUpdateDestroyAPIView.as_view()
    ),
    path("attribute_name_list/", views.AttributeNameListAPIView.as_view()),
]
