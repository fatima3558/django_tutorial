from django.shortcuts import render, get_object_or_404 # import get_object_or_404 if using that shortcut

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

# only when using generic views:
from django.views import generic

# for debugging the IndexView so we don't see questions with pub_date in the future
from django.utils import timezone

from .models import Choice, Question

# Create your views here.

######## WITH GENERIC VIEWS ########
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions (not including those set to be published in the future."""
		# pub_date__lte means return the Questions that have a pubdate less than or equal to now
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5] #chaining woot

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		"""Excludes any questions that aren't published yet."""
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

# the vote url stays the same because it just changes data, there's no template associated with it

######## END REQUIRED CODE FOR USING GENERIC VIEWS ########

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template('polls/index.html')
	context = {
		'latest_question_list': latest_question_list,
	}
	return HttpResponse(template.render(context, request))
	# OR there's a shortcut:
	# return render(request, 'polls/index.html', context)
	# If we do it this way, we don't need to import loader or HttpResponse
	# from the docs:
	# The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.

def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	# return HttpResponse("You're looking at question %s." % question_id)
	### HttpResponse shortcut:
	return render(request, 'polls/detail.html', {'question': question})

	### Http404 shortcut // instead of try / except block, do
	# question = get_object_or_404(Question, pk=question_id)
	# and then the return statement using HttpResponse or the render() method

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	# return HttpResponse(response % question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
		# print(selected_choice)

		# breakpoint()

		# older python: import pdb; pdb.set_trace()
		# From the docs:
			# request.POST is a dictionary-like object that lets you access submitted data by key name. 
			# In this case, request.POST['choice'] returns the ID of the selected choice, as a string. 
			# request.POST values are always strings.

			# Note that Django also provides request.GET for accessing GET data in the same way – 
			# but we’re explicitly using request.POST in our code, to ensure that data is only altered via a POST call.

			# request.POST['choice'] will reaise KeyError if choice wasn't provided in the POST data
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# print("we added one to the votes")
	return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
	# According to docs:
	# Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
	
	# HttpResponseRedirect only takes one argument: the url to which we want to redirect
	#  From the docs: [This function] is given the name of the view that we want to pass control to 
	# and the variable portion of the URL pattern that points to that view. 
	# In this case, using the URLconf we set up in Tutorial 3, this reverse() call will return a string like
	# `'/polls/3/results/'` where the 3 is the value of question.id. This redirected URL will then call
	# the 'results' view to display the final page