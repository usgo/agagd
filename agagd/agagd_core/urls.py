from agagd_core.views import beta as agagd_beta_views
from django.conf.urls import url

urlpatterns = (url(r"$", agagd_beta_views.index),)
