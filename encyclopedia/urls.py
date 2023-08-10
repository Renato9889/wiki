from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/<str:title>", views.search_substring, name="search_substring"),
    path('wiki/<str:title>/', views.search, name='search'),
    path("search_title/<str:title>/", views.search_title, name="search_title"),
    path("newpage/",views.create_newpage,name="create_newpage"),
    path("search_random/",views.search_random,name="search_random"),
    path("notFound/", views.not_found, name="not_found"),
    path("editpage/",views.edit_page, name="edit_page"),
]
