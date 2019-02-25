from django.contrib import messages
from django.urls import reverse


def warn_no_phone_number(get_response):
    def middleware(request):
        response = get_response(request)

        if request.user.is_authenticated and request.user.phone_number is None:
            edit_profile = reverse("accounts:edit_profile")

            messages.add_message(request, messages.ERROR,
                                 "Innan du registrerar dig på jobb måste du "
                                 "<a href='%s'>lägga till ett telefonnummer.</a>" % edit_profile)

        return response

    return middleware
