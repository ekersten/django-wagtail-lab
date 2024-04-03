from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from wagtail.images.exceptions import InvalidFilterSpecError
from wagtail.images.models import SourceImageIOError
from wagtail.images.views.serve import ServeView as BaseServeView


class ServeView(BaseServeView):
    def get(self, request, image_id, filter_spec, filename=None):
        image = get_object_or_404(self.model, id=image_id)

        # Get/generate the rendition
        try:
            rendition = image.get_rendition(filter_spec)
        except SourceImageIOError:
            return HttpResponse("Source image file not found", content_type="text/plain", status=410)
        except InvalidFilterSpecError:
            return HttpResponse(
                "Invalid filter spec: " + filter_spec,
                content_type="text/plain",
                status=400,
            )

        return getattr(self, self.action)(rendition)
