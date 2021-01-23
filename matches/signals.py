from django.dispatch import Signal


# in this signal like others i don't wanna just implement the receive but also implement to send the signal 
user_matches_update = Signal(providing_args=['user'])