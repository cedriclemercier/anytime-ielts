import requests, json, random

from django.conf import settings
from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

from .forms import EssayForm

from .prompts import task_achievement, coherence_and_cohesion, lexical_resource, grammatical_range_accuracy

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

sample_writing_text = """One of the most debatable issues of the last century has been the extent to which international trade benefits or harms national economies. Many arguments have been made for and against free trade between nations. In this essay, I will discuss both views and state my own position.

Those who support the expansion of global free trade claim that economies grow faster when they can specialise in just a few industries in which they have a strong advantage. As a result, each region or country produces something of value to the world economy. For example, East Asia manufactures electronic goods, the Middle East exports energy, and the EU produces luxury items. Free trade proponents claim that dependence on global trade helps to strengthen international cooperation and prevent wars.

Meanwhile, opponents of free trade—sometimes called ‘protectionists’—claim that the unrestricted movement of goods and services causes damage to local communities. This is because jobs are lost when it becomes cheaper to import a product than to produce it domestically. They also argue that the vast distances travelled by food, oil, and consumer goods is harming the environment and making our lives unsustainable. Protectionists are in favour of tighter controls on the movement of goods and services in order to protect jobs and livelihoods.

In conclusion, while there are convincing arguments on both sides of the debate, a return to protectionist policies would surely be a mistake. I believe that global trade is inevitable and should not be restricted. It is no longer realistic for nations to source all of their energy, food, and manufactured goods within their own borders."""

def index(request):
  context = {
    'segment': 'index'
  }
  return render(request, "pages/index.html", context)

@csrf_exempt
def writing_page(request):
  if (request.method == 'POST'):
    
    # form = EssayForm(request.POST)
    payload = {
      'user_answer': request.POST['user_answer'],
      'question_text': request.POST['question_text'],
      'question_type': request.POST['question_type'],
      'question_topic': request.POST['question_topic'],
      'question_topic': request.POST['question_topic'],
      }
    
    # Get feedback from ChatGPT API
    question = payload["question_text"]
    answer = payload["user_answer"]

    feedback = {'task_achievement': {},
                'coherence_and_cohesion': {},
                'lexical_resource': {},
                'grammatical_range_accuracy': {}}
    
    feedback['task_achievement'] = task_achievement(question, answer)
    feedback['coherence_and_cohesion'] = coherence_and_cohesion(question, answer)
    feedback['lexical_resource'] = lexical_resource(question, answer)
    feedback['grammatical_range_accuracy'] = grammatical_range_accuracy(question, answer)

    
    print("==============FEEDBACK DICT===============")
    print(feedback)

    # response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         temperature=0.6,
    #         messages=[
    #     {"role": "system", "content": "You are a professional IELTS examiner."},
    #     {"role": "user", "content": f'Given the question: "{question}"\n Please grade the following response: "{answer}"'},
    #   ]
    # )
    # Dummy feedback
    # response = requests.post(settings.API_URL + '/api/scoring/', json=payload).json()
    # print(response)
    
    data = payload
    data['topic'] = payload['question_topic']
    
  #   context = {
  #   'segment': 'writing',
  #   'answer': 'Type your answer here...',
  #   'question': 'Question here',
  #   'user_answer': sample_writing_text,
  #   'scored': True,
  #   'results': response,
  #   'question': data,
  #   'percentages': {
  #     'grammar': int(response['grammar_range']['score'] * 10),
  #     'lexical': int(response['lexical']['score'] * 10),
  #     'task_achievement': int(response['task_achievement']['score'] * 10),
  #     'coherence_cohesion': int(response['coherence_cohesion']['score'] * 10)
  #   }
  # }
    return render(request, 'pages/writing.html')
  
  
  
  data = requests.get(settings.API_URL + '/api/questions/').json()
  random_question = data[random.randint(1, len(data)-1)]
  random_question['question_topic'] = random_question['topic']
  random_question['user_answer'] = 'Type here...'
  
  form = EssayForm(random_question)
  # form.fields['user_answer'].required = False
  
  context = {
    'segment': 'writing',
    'answer': 'Type your answer here...',
    'question': random_question,
    'form': form
  }
  return render(request, 'pages/writing.html', context)

def band_score_page(request):
  context ={
    'segment': 'band_score',
    'answer': sample_writing_text
  }
  return render(request, 'pages/band_score.html', context)
















# Components
@login_required(login_url='/accounts/login/')
def bc_button(request):
  context = {
    'parent': 'basic_components',
    'segment': 'button'
  }
  return render(request, "pages/components/bc_button.html", context)

@login_required(login_url='/accounts/login/')
def bc_badges(request):
  context = {
    'parent': 'basic_components',
    'segment': 'badges'
  }
  return render(request, "pages/components/bc_badges.html", context)

@login_required(login_url='/accounts/login/')
def bc_breadcrumb_pagination(request):
  context = {
    'parent': 'basic_components',
    'segment': 'breadcrumbs_&_pagination'
  }
  return render(request, "pages/components/bc_breadcrumb-pagination.html", context)

@login_required(login_url='/accounts/login/')
def bc_collapse(request):
  context = {
    'parent': 'basic_components',
    'segment': 'collapse'
  }
  return render(request, "pages/components/bc_collapse.html", context)

@login_required(login_url='/accounts/login/')
def bc_tabs(request):
  context = {
    'parent': 'basic_components',
    'segment': 'navs_&_tabs'
  }
  return render(request, "pages/components/bc_tabs.html", context)

@login_required(login_url='/accounts/login/')
def bc_typography(request):
  context = {
    'parent': 'basic_components',
    'segment': 'typography'
  }
  return render(request, "pages/components/bc_typography.html", context)

@login_required(login_url='/accounts/login/')
def icon_feather(request):
  context = {
    'parent': 'basic_components',
    'segment': 'feather_icon'
  }
  return render(request, "pages/components/icon-feather.html", context)


# Forms and Tables
@login_required(login_url='/accounts/login/')
def form_elements(request):
  context = {
    'parent': 'form_components',
    'segment': 'form_elements'
  }
  return render(request, 'pages/form_elements.html', context)

@login_required(login_url='/accounts/login/')
def basic_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'basic_tables'
  }
  return render(request, 'pages/tbl_bootstrap.html', context)

# Chart and Maps
@login_required(login_url='/accounts/login/')
def morris_chart(request):
  context = {
    'parent': 'chart',
    'segment': 'morris_chart'
  }
  return render(request, 'pages/chart-morris.html', context)

@login_required(login_url='/accounts/login/')
def google_maps(request):
  context = {
    'parent': 'maps',
    'segment': 'google_maps'
  }
  return render(request, 'pages/map-google.html', context)

# Authentication
class UserRegistrationView(CreateView):
  template_name = 'accounts/auth-signup.html'
  form_class = RegistrationForm
  success_url = '/accounts/login/'

class UserLoginView(LoginView):
  template_name = 'accounts/auth-signin.html'
  form_class = LoginForm

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/auth-reset-password.html'
  form_class = UserPasswordResetForm

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/auth-password-reset-confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/auth-change-password.html'
  form_class = UserPasswordChangeForm

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

@login_required(login_url='/accounts/login/')
def profile(request):
  context = {
    'segment': 'profile',
  }
  return render(request, 'pages/profile.html', context)

@login_required(login_url='/accounts/login/')
def sample_page(request):
  context = {
    'segment': 'sample_page',
  }
  return render(request, 'pages/sample-page.html', context)