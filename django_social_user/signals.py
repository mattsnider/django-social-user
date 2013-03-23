from django.dispatch.dispatcher import Signal

django_social_user_pre_auth = Signal(providing_args=['request'])

django_social_user_post_callback = Signal(providing_args=['request'])

django_social_user_pre_callback = Signal(providing_args=['request'])
