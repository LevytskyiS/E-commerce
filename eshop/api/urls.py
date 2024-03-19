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
    # Attribute Objects
    path("attributes/", views.AttributeAPIViewSet.as_view({"get": "list"})),
    path("attribute/", views.AttributeCreateAPIView.as_view()),
    path(
        "attribute/<int:pk>/",
        views.AttributeAPIViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    # Brand Objects
    path("brand/", views.BrandCreateAPIView.as_view()),
    path("brand/<int:pk>/", views.BrandGetUpdateDestroyAPIView.as_view()),
    path("brands/", views.BrandListAPIView.as_view()),
]
