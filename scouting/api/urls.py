from rest_framework.routers import DefaultRouter
from .views import ScoutingReportViewSet

router = DefaultRouter()
router.register(r"reports", ScoutingReportViewSet)

urlpatterns = router.urls
