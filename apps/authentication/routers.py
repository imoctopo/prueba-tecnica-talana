from rest_framework.routers import SimpleRouter
from .views import SignUpGenericGenericViewSet

app_name = 'authentication'
router = SimpleRouter(trailing_slash=False)
router.register(r'accounts', SignUpGenericGenericViewSet, basename='accounts')

urlpatterns = router.urls
