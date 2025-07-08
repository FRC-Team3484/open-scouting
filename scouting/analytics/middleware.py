from .models import PageView


class PageViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.method == "GET"
            and not request.path.startswith("/admin")
            and not request.path.startswith("/sw.js")
            and not request.path.startswith("/favicon.ico")
            and "text/html" in response.get("Content-Type", "")
            and request.headers.get("X-Requested-With") != "XMLHttpRequest"
            and not request.headers.get("Service-Worker-Navigation-Preload")
        ):
            PageView.objects.create(url=request.path)

        return response
