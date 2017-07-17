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
   
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_active or request.user.account.initial_password:
            return redirect('temp_password_change')
        if request.user.is_superuser:
            return super(SuperUserCheckMixin, self).dispatch(request, 
            	*args, **kwargs)
        return redirect(self.user_check_failure_path)


class ManagerCheckMixin:

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_active or request.user.account.initial_password:
            return redirect('temp_password_change')
        if request.user.is_active:
            if request.user.is_superuser or request.user.is_manager:
                return super(ManagerCheckMixin, self).dispatch(request, 
                	*args, **kwargs)
        return redirect(self.user_check_failure_path)


class StaffCheckMixin:

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_active or request.user.account.initial_password:
            return redirect('temp_password_change')
        if request.user.is_active:
            if request.user.is_staff:
                return super(StaffCheckMixin, self).dispatch(request, 
                    *args, **kwargs)
        return redirect(self.user_check_failure_path)


class WarehouseAndManagerCheckMixin:

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_active or request.user.account.initial_password:
            return redirect('temp_password_change')
        if request.user.is_active:
            if request.user.is_superuser or request.user.is_manager or \
                request.user.is_warehouse:
                return super(WarehouseAndManagerCheckMixin, self).dispatch(request, 
                	*args, **kwargs)
        return redirect(self.user_check_failure_path)
 

class MaintenanceAndManagerCheckMixin:

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_active or request.user.account.initial_password:
            return redirect('temp_password_change')
        if request.user.is_active:
            if request.user.is_superuser or request.user.is_maintenance or \
            request.user.is_manager:
                return super(MaintenanceAndManagerCheckMixin, self).dispatch(request, 
                    *args, **kwargs)
        return redirect(self.user_check_failure_path)


class FinanceCheckMixin:

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_active or request.user.account.initial_password:
            return redirect('temp_password_change')
        if request.user.is_active:
            if request.user.is_superuser or request.user.is_financial:
                return super(FinanceCheckMixin, self).dispatch(request, 
                    *args, **kwargs)
        return redirect(self.user_check_failure_path)
