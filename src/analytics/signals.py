# TO create the Custom Signals. In these we can create the signals such that every time the object is viewed signals are said to be passed
#instead of calling the model in every view

from django.dispatch import Signal

object_view_signal=Signal(providing_args=['instance','request']) #Instance belongs to the Product with the title having a Partiular id
