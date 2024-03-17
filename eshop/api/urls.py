from django.urls import path

from . import views


app_name = "api"
urlpatterns = [
    # AttributeName Objects
    path("attributename/", views.AttributeNameCreateAPIView.as_view()),
    path(
        "attributename/<int:pk>/", views.AttributeNameGetUpdateDestroyAPIView.as_view()
    ),
    path("attributenames/", views.AttributeNameListAPIView.as_view()),
    # AttributeValue Objects
    path("attributevalue/", views.AttributeValueCreateAPIView.as_view()),
    path(
        "attributevalue/<int:pk>/",
        views.AttributeValueGetUpdateDestroyAPIView.as_view(),
    ),
    path("attributevalues/", views.AttributeValueListAPIView.as_view()),
]
