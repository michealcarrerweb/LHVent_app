from __future__ import unicode_literals

from django.conf.urls import url, include

from account.views import SignupView, LoginView, LogoutView, DeleteView
from account.views import ConfirmEmailView
from account.views import ChangePasswordView, PasswordResetView, PasswordResetTokenView
from account.views import SettingsView
from account.views import AccountViewAPI#, AccountCreateViewAPI, AccountUpdateViewAPI, AccountDeleteViewAPI

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/account', AccountViewAPI)
# router.register(r'api/account_create', AccountCreateViewAPI)
# router.register(r'api/account/1', AccountUpdateViewAPI)
# router.register(r'api/account_delete/2', AccountDeleteViewAPI)


urlpatterns = [
    url(r"^signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^login/$", LoginView.as_view(), name="account_login"),
    url(r"^logout/$", LogoutView.as_view(), name="account_logout"),
    url(r"^confirm_email/(?P<key>\w+)/$", ConfirmEmailView.as_view(), name="account_confirm_email"),
    url(r"^password/$", ChangePasswordView.as_view(), name="account_password"),
    url(r"^password/reset/$", PasswordResetView.as_view(), name="account_password_reset"),
    url(r"^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$", PasswordResetTokenView.as_view(), name="account_password_reset_token"),
    url(r"^settings/$", SettingsView.as_view(), name="account_settings"),
    url(r"^delete/$", DeleteView.as_view(), name="account_delete"),
    url(r'^', include(router.urls)),
    # url(r'^user/create/$', AccountCreateViewAPI.as_view(), name="user_create"),
    # # url(r'^users/list/$', views.UsersListView.as_view(), name="users_list"),
    # # url(r'^users/(?P<pk>\d+)/detail/$', views.UserDetailView.as_view(), name="user_detail"),
    # url(r'^users/(?P<pk>\d+)/update/$', AccountUpdateViewAPI.as_view(), name="user_update"),
    # url(r'^users/(?P<pk>\d+)/delete/$', AccountDeleteViewAPI, name="user_delete"), 

    
]
