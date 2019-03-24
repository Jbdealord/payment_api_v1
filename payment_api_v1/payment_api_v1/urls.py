from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from payment_api_v1.views import AccountViewSet, BalanceViewSet, PaymentViewSet


router = DefaultRouter()
router.register(r'account', AccountViewSet)
router.register(r'balance', BalanceViewSet)
router.register(r'payment', PaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Payment API v1')),
    path('api/', include(router.urls)),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
