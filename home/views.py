from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

def index(request):
  context = {
    'segment': 'index'
  }
  return render(request, "pages/index.html", context)

def writing_page(request):
  context = {
    'segment': 'writing',
    'answer': """One of the most debatable issues of the last century has been the extent to which international trade benefits or harms national economies. Many arguments have been made for and against free trade between nations. In this essay, I will discuss both views and state my own position.

Those who support the expansion of global free trade claim that economies grow faster when they can specialise in just a few industries in which they have a strong advantage. As a result, each region or country produces something of value to the world economy. For example, East Asia manufactures electronic goods, the Middle East exports energy, and the EU produces luxury items. Free trade proponents claim that dependence on global trade helps to strengthen international cooperation and prevent wars.

Meanwhile, opponents of free trade—sometimes called ‘protectionists’—claim that the unrestricted movement of goods and services causes damage to local communities. This is because jobs are lost when it becomes cheaper to import a product than to produce it domestically. They also argue that the vast distances travelled by food, oil, and consumer goods is harming the environment and making our lives unsustainable. Protectionists are in favour of tighter controls on the movement of goods and services in order to protect jobs and livelihoods.

In conclusion, while there are convincing arguments on both sides of the debate, a return to protectionist policies would surely be a mistake. I believe that global trade is inevitable and should not be restricted. It is no longer realistic for nations to source all of their energy, food, and manufactured goods within their own borders."""
  }
  return render(request, 'pages/writing.html', context)

def band_score_page(request):
  context ={
    'segment': 'band_score'
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