from django.contrib import messages
from django.views.generic.edit import DeleteView

from .permission_mixins import SuperUserCheckMixin


class DeleteViewMixin(SuperUserCheckMixin, DeleteView):
	template_name = "delete.html"
	success_message = "Item was successfully deleted"

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(DeleteViewMixin, self).delete(request, *args, **kwargs)


class ContextMixin(object):
	success_message = "%(item)s was successfully %(action)s"

	def __init__(self, *args, **kwargs):
		super(ContextMixin, self).__init__(*args, **kwargs)
		self.location = ""

	def get_context_data(self, **kwargs):
		context = super(ContextMixin, self).get_context_data(**kwargs)
		context['title'] = "{} {}".format(self.name.title(),
										  self.action.title())
		return context
