from django.urls import path

from . import views


app_name = "api"
urlpatterns = [
    # AttributeName Objects
    path("attributename/", views.AttributeNameCreateAPIView.as_view()),
    path(
        "attributename/<int:pk>/", views.AttributeNameGetUpdateDestroyAPIView.as_view()
    ),
    path("attributename_list/", views.AttributeNameListAPIView.as_view()),
    # AttributeValue Objects
]
