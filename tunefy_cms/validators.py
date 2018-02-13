

def is_empty(value):
    return value is None or not isinstance(value, str) or value == '' or value.isspace()


def is_max_length_exceeded(value, max_lth):
    return len(value) > max_lth


class ValidationMessages:
    FIELD_IS_REQUIRED = 'Pole jest wymagane.'
    MAX_LENGTH_EXCEEDED = "Długość pola '%s' nie może przekraczać %s znaków."
