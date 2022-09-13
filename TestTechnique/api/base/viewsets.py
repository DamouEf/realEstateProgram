
from rest_framework import viewsets, serializers
from rest_framework.pagination import PageNumberPagination , LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class BaseViewSet(viewsets.ModelViewSet):

    permission_classes = [AllowAny]

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if "Pagination-Style" in self.request.headers:
                if self.request.headers['Pagination-Style'] not in ['PageNumberPagination', 'LimitOffsetPagination']:
                    self._paginator = None
                else:
                    from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
                    module_name = 'rest_framework.pagination'
                    class_name = self.request.headers['Pagination-Style']

                    import importlib
                    module = importlib.import_module(module_name)
                    class_ = getattr(module, class_name)
                    self._paginator = class_()
            else:
                self._paginator = None
                
        return self._paginator