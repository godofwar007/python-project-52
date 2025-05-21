from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.id == self.kwargs["pk"]

    def handle_no_permission(self):
        messages.error(
            self.request,
            "У вас нет прав для изменения другого пользователя."
        )
        return redirect("users")
