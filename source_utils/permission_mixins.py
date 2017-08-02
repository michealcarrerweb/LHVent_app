from django.shortcuts import redirect
from django.views.generic import TemplateView


class TemporaryPassWordTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if request.user.__str__() == "AnonymousUser" or request.user.account.initial_password == None:
            return super(TemplateView, self).dispatch(request, 
                *args, **kwargs)
        else:
            return redirect('temp_password_change')        


class SuperUserCheckMixin:
    title = None
    url_insert = None
    permissions = 'request.user.is_superuser'
   
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_active or request.user.account.initial_password:
            return redirect('temp_password_change')
        if request.user.is_active:
            if self.permissions:
                return super(SuperUserCheckMixin, self).dispatch(request, 
                	*args, **kwargs)
        return redirect(self.user_check_failure_path)

    def get_context_data(self, **kwargs):
        context = super(SuperUserCheckMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['url_insert'] = self.url_insert
        return context


class ManagerCheckMixin(SuperUserCheckMixin):
    permissions = 'request.user.is_superuser or request.user.is_manager'


class StaffCheckMixin(SuperUserCheckMixin):
    permissions = 'request.user.is_staff'


class WarehouseAndManagerCheckMixin(SuperUserCheckMixin):
    permissions = 'request.user.is_superuser or request.user.is_manager or request.user.is_warehouse'
 

class MaintenanceAndManagerCheckMixin(SuperUserCheckMixin):
    permissions = 'request.user.is_superuser or request.user.is_maintenance or request.user.is_manager'


class FinanceCheckMixin(SuperUserCheckMixin):
    permissions = 'request.user.is_superuser or request.user.is_financial'
