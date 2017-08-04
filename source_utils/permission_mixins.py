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
    permissions = ['is_superuser',]
    user_check_failure_path = '500'

   
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_active or request.user.account.initial_password:
            return redirect('temp_password_change')
        perm_dict = {'is_superuser': self.request.user.is_superuser,
                     'is_manager': self.request.user.is_manager,
                     'is_financial': self.request.user.is_financial,
                     'is_warehouse': self.request.user.is_warehouse,
                     'is_maintenance': self.request.user.is_maintenance,
                     'is_staff': self.request.user.is_staff,
                     'is_service': self.request.user.is_service,
        }
        if request.user.is_active:
            for priviledge in self.permissions:
                if perm_dict[priviledge]:
                    return super(SuperUserCheckMixin, self).dispatch(request, 
                    	*args, **kwargs)
        return redirect(self.user_check_failure_path)

    def get_context_data(self, **kwargs):
        context = super(SuperUserCheckMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['url_insert'] = self.url_insert
        return context


class ManagerCheckMixin(SuperUserCheckMixin):
    permissions = ['is_superuser', 'is_manager']


class StaffCheckMixin(SuperUserCheckMixin):
    permissions = ['is_superuser', 'is_staff']


class WarehouseAndManagerCheckMixin(SuperUserCheckMixin):
    permissions = ['is_superuser', 'is_manager', 'is_warehouse']
 

class MaintenanceAndManagerCheckMixin(SuperUserCheckMixin):
    permissions = ['is_superuser', 'is_manager', 'is_maintenance']


class FinanceCheckMixin(SuperUserCheckMixin):
    permissions = ['is_superuser', 'is_financial']
