from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView


class PartialViewSet(ModelViewSet):
    """
    Viewset where put requests not allowed
    """

    http_method_names = ["get", "post", "patch", "delete", "options"]

    def put(self, request, *args, **kwargs) -> None:
        self.http_method_not_allowed()


class RetrievePartialDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Api where put method not allowed
    """

    http_method_names = ["get", "post", "patch", "delete", "options"]

    def put(self, request, *args, **kwargs) -> None:
        self.http_method_not_allowed()
