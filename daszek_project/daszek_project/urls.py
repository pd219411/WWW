from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'daszek_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^wybory/', include('wybory.urls', namespace = "wybory")),

    url(r'^admin/', include(admin.site.urls)),
]
