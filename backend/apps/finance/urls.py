from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.finance.views import (
    TuitionRuleViewSet, TuitionExemptionViewSet,
    TuitionExtensionViewSet, StudentDebtViewSet, ReceiptViewSet
)

router = DefaultRouter()
router.register(r'tuition-rules', TuitionRuleViewSet, basename='tuition-rule')
router.register(r'tuition-exemptions', TuitionExemptionViewSet, basename='tuition-exemption')
router.register(r'tuition-extensions', TuitionExtensionViewSet, basename='tuition-extension')
router.register(r'student-debts', StudentDebtViewSet, basename='student-debt')
router.register(r'receipts', ReceiptViewSet, basename='receipt')

urlpatterns = [
    path('', include(router.urls)),
]
