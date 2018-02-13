import os

from django.core.exceptions import ValidationError


def is_empty(value):
    return value is None or not isinstance(value, str) or value == '' or value.isspace()


class ValidationMessages:
    FIELD_IS_REQUIRED = 'To pole jest wymagane.'
    MAX_LENGTH_EXCEEDED = "%(name)s nie może przekraczać %(max_length)s znaków."
    TOO_FEW_CHARACTERS = "%(name)s musi składać się z przynajmniej %(min_length)s znaków."
    NOT_SUPPORTED_FILE_EXTENSION = "Plik powinien mieć rozszerzenie: %(allowed_extensions)s."
    SELECT_AT_LEAST_ONE_OPTION = "Zaznacz przynajmniej jedną opcję."


def validate_text_field(form, field_name, required, max_length, min_length=0):
    value = form.cleaned_data.get(field_name)

    if required and is_empty(value):
        raise ValidationError(
            ValidationMessages.FIELD_IS_REQUIRED,
            code='invalid'
        )

    lth = len(value)

    if lth > max_length:
        raise ValidationError(
            ValidationMessages.MAX_LENGTH_EXCEEDED,
            code='invalid',
            params={
                'name': form.fields.get(field_name).label,
                'max_length': max_length
            }
        )

    if lth < min_length:
        raise ValidationError(
            ValidationMessages.TOO_FEW_CHARACTERS,
            code='invalid',
            params={
                'name': form.fields.get(field_name).label,
                'min_length': min_length
            }
        )

    return value


def validate_selection_box(form, field_name):
    value = form.cleaned_data.get(field_name)
    if value is not None:
        lth = len(value)
        if lth < 1:
            raise ValidationError(
                ValidationMessages.SELECT_AT_LEAST_ONE_OPTION,
                code='invalid'
            )
    return value


def validate_file(form, field_name, required, allowed_extensions):
    value = form.cleaned_data.get(field_name)

    if required and value is None:
        raise ValidationError(
            ValidationMessages.FIELD_IS_REQUIRED,
            code='invalid'
        )

    if value is not None and value is not False:
        ext = os.path.splitext(value.name)[1]
        if not ext.lower() in allowed_extensions:
            raise ValidationError(
                ValidationMessages.NOT_SUPPORTED_FILE_EXTENSION,
                code='invalid',
                params={
                    'allowed_extensions': ", ".join(allowed_extensions)
                }
            )

    return value
