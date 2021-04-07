from django.conf.urls import url

from agagd_core.views import beta as agagd_beta_views

urlpatterns = (
    url(r'$', agagd_beta_views.index),
)
