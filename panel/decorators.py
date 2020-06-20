from django.http import HttpResponse


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                # if group in allowed_roles:
            for role in allowed_roles:
                if group == role:
                    return view_func(request, *args, **kwargs)
            return HttpResponse("You are not authorized to view this page")
            # return view_func(request, *args, **kwargs)

        return wrapper_function

    return decorator