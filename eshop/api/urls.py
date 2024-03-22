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
    # Product Objects
    path("product/", views.ProductCreateAPIView.as_view()),
    path("product/<int:pk>/", views.ProductGetUpdateDestroyAPIView.as_view()),
    path("products/", views.ProductListAPIView.as_view()),
    # Image Objects
    path("image/", views.ImageCreateAPIView.as_view()),
    path("image/<int:pk>/", views.ImageGetUpdateDestroyAPIView.as_view()),
    path("images/", views.ImageListAPIView.as_view()),
    # ProductImage Objects
    path("productimage/", views.ProductImageCreateAPIView.as_view()),
    path("productimage/<int:pk>/", views.ProductImageGetUpdateDestroyAPIView.as_view()),
    path("productimages/", views.ProductImageListAPIView.as_view()),
    # Order Objects
    path("order/", views.OrderCreateAPIView.as_view()),
    path("order/<int:pk>/", views.OrderGetUpdateDestroyAPIView.as_view()),
    path("orders/", views.OrderListAPIView.as_view()),
    # OrderItem Objects
    path("orderitem/", views.OrderItemCreateAPIView.as_view()),
    path("orderitem/<int:pk>/", views.OrderItemGetUpdateDestroyAPIView.as_view()),
    path("orderitems/", views.OrderItemListAPIView.as_view()),
]
