from django.urls import path, re_path
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.images.views.serve import ServeView

# from .views import ServeView

api_router = WagtailAPIRouter("wagtailapi")

api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)


urlpatterns = [
    path("cms/", api_router.urls),
    re_path(
        r"^image_serve/([^/]*)/(\d*)/([^/]*)/[^/]*$", ServeView.as_view(action="redirect"), name='wagtailimages_serve'
    ),
    # re_path(r"^image_serve/(\d*)/([^/]*)/[^/]*$", ServeView.as_view(action="redirect"), name='wagtailimages_serve'),
]
