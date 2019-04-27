from django.contrib import messages
from django.urls import reverse, resolve


def warn_no_phone_number(get_response):
    def middleware(request):
        if request.user.is_authenticated and not (request.user.is_staff or request.user.is_superuser) \
                and request.user.phone_number is None:

            resolved = resolve(request.path_info)
            current_url = ":".join([resolved.namespace, resolved.url_name])

            if resolved.url_name is not None and current_url != "accounts:edit_profile":
                edit_profile = reverse("accounts:edit_profile")

                messages.add_message(request, messages.ERROR,
                                     "Innan du registrerar dig på jobb måste du "
                                     "<a href='%s'>lägga till ett telefonnummer.</a>" % edit_profile)

        response = get_response(request)

        return response
    return middleware


def warn_not_read_guide(get_response):
    def middleware(request):
        if request.user.is_authenticated and not (request.user.is_staff or request.user.is_superuser) \
                 and not request.user.read_guide:

            resolved = resolve(request.path_info)

            if resolved.url_name is not None and resolved.url_name != "guide":
                guide = reverse("guide")

                messages.add_message(request, messages.ERROR,
                                     "Innan du registrerar dig på jobb måste du "
                                     "<a href='%s'>läsa jobbguiden.</a>" % guide)

        response = get_response(request)

        return response
    return middleware
