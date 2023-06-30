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

# from .prompts import task_achievement, coherence_and_cohesion, lexical_resource, grammatical_range_accuracy

import json
import os

sample_writing_text = """One of the most debatable issues of the last century has been the extent to which international trade benefits or harms national economies. Many arguments have been made for and against free trade between nations. In this essay, I will discuss both views and state my own position."""

sample_text = "Social networking sites, for instance Facebook, are teach by some to have a detrimental effect on individual people as well as society and local communities. However, while I believe that such sites are mainly beneficial to the individual, I agree that they have had a damaging effect on local communities.  With regards to individuals, the impact that online social media has had on each individual person has clear advantages. Firstly, people from different countries are brought together through such sites as Facebook whereas before the development of technology and social networking sites, people rarely had the chance to meet or communicate with anyone outside of their immediate circle or community. Secondly, Facebook also has social groups which offer individuals a chance to meet and participate in discussions with people who share common interests. On the other hand, the effect that Facebook and other social networking sites have had on societies and local communities can only be seen as negative. Rather than individual people taking part in their local community, they are instead choosing to take more interest in people online. Consequently, the people within local communities are no longer forming close or supportive relationships. Furthermore, society as a whole is becoming increasingly disjointed and fragmented as people spend more time online with people they have never met face to face and who they are unlikely to ever meet in the future. To conclude, although social networking sites have brought individuals closer together, they have not had the same effect on society or local communities. Local communities should do more to try and involve local people in local activities  in order to promote the future of community life."

def convert_seconds(seconds):
    minutes = seconds // 60  # 60 seconds in a minute
    remaining_seconds = seconds % 60

    # Format the output
    if minutes == 1:
        minutes_str = "1 minute"
    else:
        minutes_str = f"{minutes} minutes"

    if remaining_seconds == 1:
        seconds_str = "1 second"
    else:
        seconds_str = f"{remaining_seconds} seconds"

    return f"{minutes_str}, {seconds_str}"
def put_tags(text, lexical_ranges=None, grammar_ranges=None):
    # 1. Step1: Put words under tags
    words = text.split()
    # Concat arrays
    
    btn_classes = ['btn-warning', 'theme-bg']
    error_class = ['lexical', 'grammar']
    
    all_ranges = [lexical_ranges, grammar_ranges]
    second_offset = 0
    for i, curr_range in enumerate(all_ranges):
        if curr_range is None:
            continue
        for idx, (start, end) in enumerate(curr_range):
            # temp fix
            # start -= 1
            # end -= 1
            if lexical_ranges: second_offset == i
            offset = (idx * 2) + (2 * second_offset)
            print(offset)
            words[start+offset:end+offset] = [f'<button class=" {btn_classes[i]}" type="button" data-toggle="collapse" style="border:0; padding: 0;" data-target="#{error_class[i]}{idx+1}" aria-expanded="false" aria-controls="lexical{idx+1}"><span style="padding: 2px 3px" data-toggle="tooltip" title="({idx+1})"><span>'] + words[start+offset:end+offset] + [f'</button>']
        result = ' '.join(words)
    return result
    

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
    
    response = requests.post(settings.API_URL + '/api/scoring/', json=payload).json()
    
    print(response)
    # Lexical spans
    lexical_spans = None
    if "spans" in response['lexical']:
      lexical_spans = response['lexical']['spans'][0]
    grammar_spans = response['grammar_range']['spans']
    
    
    # Scores
    task_achievement_score = response['task_achievement']['score']
    coherence_cohesion_score = response['coherence_cohesion']['score']
    lexical = response['lexical']['score']
    grammar_range_score = response['grammar_range']['score']

    user_answer_corrected = put_tags(sample_text, lexical_spans, grammar_spans)
    
    
    data = payload
    data['topic'] = payload['question_topic']
    
    numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    
    context = {
    'segment': 'writing',
    'answer': 'Type your answer here...',
    'question': 'Question here',
    'user_answer': user_answer_corrected,
    'scored': True,
    'results': response,
    'question': data,
    'overall_score': response['overall_score'],
    'overall_score_letters': numbers[round(response['overall_score'])],
    'percentages': {
      'grammar': int(response['grammar_range']['score'] * 10),
      'lexical': int(response['lexical']['score'] * 10),
      'task_achievement': int(response['task_achievement']['score'] * 10),
      'coherence_cohesion': int(response['coherence_cohesion']['score'] * 10)
    }
  }
    return render(request, 'pages/writing.html', context)
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
  random_question['user_answer'] = "Social networking sites, for instance Facebook, are teach by some to have a detrimental effect on individual people as well as society and local communities. However, while I believe that such sites are mainly beneficial to the individual, I agree that they have had a damaging effect on local communities.  With regards to individuals, the impact that online social media has had on each individual person has clear advantages. Firstly, people from different countries are brought together through such sites as Facebook whereas before the development of technology and social networking sites, people rarely had the chance to meet or communicate with anyone outside of their immediate circle or community. Secondly, Facebook also has social groups which offer individuals a chance to meet and participate in discussions with people who share common interests. On the other hand, the effect that Facebook and other social networking sites have had on societies and local communities can only be seen as negative. Rather than individual people taking part in their local community, they are instead choosing to take more interest in people online. Consequently, the people within local communities are no longer forming close or supportive relationships. Furthermore, society as a whole is becoming increasingly disjointed and fragmented as people spend more time online with people they have never met face to face and who they are unlikely to ever meet in the future. To conclude, although social networking sites have brought individuals closer together, they have not had the same effect on society or local communities. Local communities should do more to try and involve local people in local activities  in order to promote the future of community life."
  
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