from django.urls import path

from . import views

# how to differentiate between a 'details' view in the polls app
# vs one in another app? Use an app_name, aka namespace
# and make sure that in any template that needs to link to one of these views,
# that you add 'polls:the_name_of_the_view' to the url template tag
app_name = 'polls'

# In mysite/urls.py, we get directed here if the url has 'polls/'
# Once we get here, this tells us to go to the views.js file in the current directory
# urlpatterns = [
# 	path('', views.index, name='index'),
# 	path('<int:question_id>/', views.detail, name='detail'),
# 	path('<int:question_id>/results/', views.results, name='results'),
# 	path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

# this reformatted list will allow us to use generic views:
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('<int:pk>/', views.DetailView.as_view(), name='detail'),
	path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
	path('<int:question_id>/vote/', views.vote, name='vote'), # just does a POST, no template associated with it, so no need to use int:pk
]

# The DetailView generic view expects the primary key value captured from the URL
# to be called "pk", so we’ve changed question_id to pk for the generic views.