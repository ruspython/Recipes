from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       # Examples:
                       url(r'^login/$', 'loginsys.views.login'),
                       url(r'^logout/$', 'loginsys.views.logout'),
                       url(r'^register/$', 'loginsys.views.register'),
                       url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
                           {'post_reset_redirect': '/auth/password_reset/done/',
                            'template_name': 'registration/password_reset_form.html'}, name='password_reset'),
                       url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done',
                           {'template_name': 'registration/password_reset_done.html'}),
                       url(r'^password_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           'django.contrib.auth.views.password_reset_confirm',
                           {'post_reset_redirect': '/auth/reset_done/', 'template_name': 'registration/password_reset_confirm.html'}),
                       url(r'^reset_done/$', 'django.contrib.auth.views.password_reset_complete',
                           {'template_name': 'registration/password_reset_complete.html'}),

)
