from django.conf.urls import url

from agagd_core import views as agagd_views


urlpatterns = (
    url(r'$', agagd_views.index),
)
