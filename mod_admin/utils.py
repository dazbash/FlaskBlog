from flask import session, abort


def protected_view(func):
    def decorator(*args, **kwargs):
        if session.get('user_id') is None:
            abort(411)
        return func(*args, **kwargs)
    return decorator
