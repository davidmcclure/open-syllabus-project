


def requires_attr(attr):

    """
    If the instance doesn't have a defined value for a key, return None.

    :param attr: The syllabus path.
    """

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if getattr(self, attr, None):
                return func(self, *args, **kwargs)
            else: return None
        return wrapper
    return decorator
