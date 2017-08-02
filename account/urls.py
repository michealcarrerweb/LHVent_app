from __future__ import unicode_literals

from django.conf.urls import url, include

from account.views import SignupView, LoginView, LogoutView, DeleteView, ClientSignupView, StaffSignupView
from account.views import ConfirmEmailView
from account.views import ChangePasswordView, PasswordResetView, PasswordResetTokenView
from account.views import SettingsView, StaffUpdateView, StaffList, ClientList#, ClientDetail, StaffDetail
from account.views import AccountViewAPI, UserDetail#, AccountUpdateViewAPI, #AccountDeleteViewAPI

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/account', AccountViewAPI)
# router.register(r'api/account_create', AccountCreateViewAPI)
# router.register(r'api/account/1', AccountUpdateViewAPI)
# router.register(r'api/account_delete/2', AccountDeleteViewAPI)


urlpatterns = [
    url(r"^signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^client_signup/$", ClientSignupView.as_view(), name="client_signup"),
    url(r"^staff_signup/$", StaffSignupView.as_view(), name="staff_signup"),
    url(r"^login/$", LoginView.as_view(), name="account_login"),
    url(r"^logout/$", LogoutView.as_view(), name="account_logout"),
    url(r"^confirm_email/(?P<key>\w+)/$", ConfirmEmailView.as_view(), name="account_confirm_email"),
    url(r"^password/$", ChangePasswordView.as_view(), name="account_password"),
    url(r"^password/reset/$", PasswordResetView.as_view(), name="account_password_reset"),
    url(r"^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$", PasswordResetTokenView.as_view(), name="account_password_reset_token"),
    url(r"^settings/$", SettingsView.as_view(), name="account_settings"),
    # url(r"^delete/$", DeleteView.as_view(), name="account_delete"),
    url(r'^', include(router.urls)),
    # url(r'^user/create/$', AccountCreateViewAPI.as_view(), name="user_create"),
    # url(r'^users/(?P<pk>\d+)/delete/$', AccountDeleteViewAPI, name="user_delete"), 
    url(r'^staff/$', StaffList.as_view(), name="staff_list"),
    url(r'^clients/([-\w]+)/$', ClientList.as_view(), name="client_list"),
    url(r'^account/(?P<pk>\d+)/detail/$', UserDetail.as_view(), name="account_detail"),
    url(r'^client/(?P<pk>\d+)/update/$', SettingsView.as_view(), name="client_update"),
    url(r'^staff/(?P<pk>\d+)/update/$', StaffUpdateView.as_view(), name="staff_update"),   
]