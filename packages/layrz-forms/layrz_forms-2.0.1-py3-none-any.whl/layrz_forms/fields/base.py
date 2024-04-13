""" Base class for the fields """

from typing import Any


class Field:
  """ Field abstract class """

  def __init__(self, required: bool = False) -> None:
    self.required = required

  def validate(self, key: str, value: Any, errors: dict) -> None:
    """ Validate is the field is blank or None if is required
    ---
    Arguments
      key: str
        Key of the field
      value: any
        Value to validate
      errors: dict
        Dict of errors
    """

    if self.required:
      if value is None:
        self._append_error(key=key, errors=errors, to_add={'code': 'required'})

  def _convert_to_camel(self, key: str) -> str:
    """
    Convert the key to camel case
    """
    init, *temp = key.split('_')

    field = ''.join([init, *map(str.title, temp)])
    field_items = field.split('.')

    field_final = []
    for item in field_items:
      field_final.append(''.join([item[0].lower(), item[1:]]))

    return '.'.join(field_final)

  def _append_error(self, key: str, errors: dict, to_add: dict) -> None:
    """
    Append an error to a dict of errors
    ---
    Arguments
      key: str
        Key of the error
      errors: dict
        Dict of errors
      to_add: dict
        Error to add
    """

    key = self._convert_to_camel(key=key)
    if key in errors:
      errors[key].append(to_add)
    else:
      errors[key] = [to_add]
