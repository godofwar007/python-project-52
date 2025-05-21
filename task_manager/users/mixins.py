from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id == self.kwargs["pk"]

    def handle_no_permission(self):
        messages.error(
            self.request, _("You have no rights to change another user")
        )
        return redirect("users")
