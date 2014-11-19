from django.core.exceptions import ValidationError


def validate_msisdn(msisdn):
    if len(str(msisdn)) < 12:
        raise ValidationError('MSISDN must have 12 or 13 digits')

    if str(msisdn)[0:2] != '55':
        raise ValidationError('MSISDN must start with 55')
