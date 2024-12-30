from django.urls import path

from . import views

app_name = "oradja"
urlpatterns = [
    path(
        "umvdocuments/",
        views.UmvDocumentListView.as_view(),
        name="all"
    ),
    path(
        "umvdocuments/<int:pk>/",
        views.UmvDocumentDetailView.as_view(),
        name="detail"
    ),
    path(
        "umvdocuments/search/",
        views.UmvDocumentSearchView.as_view(),
        name="search"
    )
]
