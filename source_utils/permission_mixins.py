from django.shortcuts import redirect


class SuperUserCheckMixin(object):

    user_check_failure_path = '403'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(SuperUserCheckMixin, self).dispatch(request, 
            	*args, **kwargs)
        return redirect(self.user_check_failure_path)


class ManagerCheckMixin(object):

    user_check_failure_path = '403'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            if request.user.is_superuser or request.user.is_manager:
                return super(ManagerCheckMixin, self).dispatch(request, 
                	*args, **kwargs)
        return redirect(self.user_check_failure_path)


class WarehouseAndManagerCheckMixin(object):

    user_check_failure_path = '403'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            if request.user.is_superuser or request.user.is_manager or \
                request.user.is_warehouse:
                return super(WarehouseAndManagerCheckMixin, self).dispatch(request, 
                	*args, **kwargs)
        return redirect(self.user_check_failure_path)
 

class MaintenanceAndManagerCheckMixin(object):

    user_check_failure_path = '403'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            if request.user.is_superuser or request.user.is_maintenance or \
            request.user.is_manager:
                return super(MaintenanceAndManagerCheckMixin, self).dispatch(request, 
                    *args, **kwargs)
        return redirect(self.user_check_failure_path)


class FinanceCheckMixin(object):

    user_check_failure_path = '403'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            if request.user.is_superuser or request.user.is_financial:
                return super(FinanceCheckMixin, self).dispatch(request, 
                    *args, **kwargs)
        return redirect(self.user_check_failure_path)

