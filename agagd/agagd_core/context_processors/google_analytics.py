def google_analytics_tracking_id(request):
    from django.conf import settings
    return {'google_analytics_tracking_id': settings.GOOGLE_ANALYTICS_TRACKING_ID}
