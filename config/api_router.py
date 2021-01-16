from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from osler.users.api.views import UserViewSet
from osler.core.api.views import PatientViewSet
from osler.demographics.api.views import DemographicsViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("user", UserViewSet)
router.register("patient", PatientViewSet)
router.register("demographics", DemographicsViewSet)

app_name = "api"
urlpatterns = router.urls
