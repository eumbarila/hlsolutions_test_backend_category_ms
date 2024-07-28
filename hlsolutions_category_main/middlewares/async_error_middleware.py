from django.http import JsonResponse

def async_error_middleware(view_func):
    """
    Middleware function that handles exceptions raised by the view function.

    Args:
        view_func (function): The view function to be wrapped.

    Returns:
        function: The wrapped view function.

    Raises:
        None

    """
    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({'Unknown error': str(e)}, status=500)
    return _wrapped_view