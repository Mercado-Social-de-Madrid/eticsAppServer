# coding=utf-8
import json

from django.core.exceptions import PermissionDenied
from tastypie.http import HttpUnauthorized, HttpForbidden


class WrongPinCode(PermissionDenied):
    """ Exception when the user enters an incorrect pincode """
    def __init__(self, wallet=None):

        response = {
            'error': 'wrong_pincode',
            'message': 'El código pin introducido no es correcto'
        }

        self.response = HttpForbidden(content=json.dumps(response), content_type='application/json')


class NotEnoughBalance(Exception):
    """ Exception when a transaction is being made but the wallet doesnt have enough cash """
    def __init__(self, wallet=None):

        response = {
            'error': 'not_enough_balance',
            'message': 'El monedero no tiene suficiente saldo disponible para realizar la operación'
        }

        self.response = HttpForbidden(content=json.dumps(response), content_type='application/json')


class ReceiverNotRegistered(Exception):
    """ Exception when a receiver of a payment is not registered in app """
    def __init__(self, wallet=None):

        response = {
            'error': 'receiver_not_registered',
            'message': 'La entidad destinataria del pago no está registrada en la app. No es posible hacer el pago'
        }

        self.response = HttpForbidden(content=json.dumps(response), content_type='application/json')


class GuestExpired(Exception):
    """ Exception when a payment sender is guest and its period is expired """
    def __init__(self, wallet=None):

        response = {
            'error': 'guest_expired',
            'message': 'Tu periodo de prueba como usuario invitado ha terminado.\n'
                       'Para hacer el pago en Etics es necesario darse de alta como socia'
        }

        self.response = HttpForbidden(content=json.dumps(response), content_type='application/json')


