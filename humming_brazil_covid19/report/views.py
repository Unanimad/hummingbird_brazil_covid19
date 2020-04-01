from rest_framework import viewsets
from rest_framework import permissions

from humming_brazil_covid19.report.models import Case
from humming_brazil_covid19.report.serializers import CaseSerializer


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [permissions.AllowAny]
