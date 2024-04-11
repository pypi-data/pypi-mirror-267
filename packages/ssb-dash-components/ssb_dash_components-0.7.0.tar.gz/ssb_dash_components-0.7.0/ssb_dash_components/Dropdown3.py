# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dropdown3(Component):
    """A Dropdown3 component.


Keyword arguments:

- id (string; optional)

- ariaLabel (string; optional)

- className (string; optional)

- description (string; optional):
    Add explanation text.

- error (boolean; optional)

- errorMessage (string; optional)

- header (string; default '')

- icon (dict; optional)

- items (list of dicts; default [{ id: '', title: '' }])

    `items` is a list of dicts with keys:

    - disabled (boolean; optional)

    - id (string; optional)

    - title (string; optional)

- largeSize (boolean; optional)

- open (boolean; default False)

- placeholder (string; default '-- Select --')

- searchable (boolean; default False)

- selectedItem (dict; optional)

- showDescription (boolean; optional):
    Set True to show glossary.

- tabIndex (number; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ssb_dash_components'
    _type = 'Dropdown3'
    @_explicitize_args
    def __init__(self, ariaLabel=Component.UNDEFINED, className=Component.UNDEFINED, error=Component.UNDEFINED, errorMessage=Component.UNDEFINED, header=Component.UNDEFINED, icon=Component.UNDEFINED, items=Component.UNDEFINED, open=Component.UNDEFINED, placeholder=Component.UNDEFINED, searchable=Component.UNDEFINED, selectedItem=Component.UNDEFINED, tabIndex=Component.UNDEFINED, id=Component.UNDEFINED, largeSize=Component.UNDEFINED, showDescription=Component.UNDEFINED, description=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'ariaLabel', 'className', 'description', 'error', 'errorMessage', 'header', 'icon', 'items', 'largeSize', 'open', 'placeholder', 'searchable', 'selectedItem', 'showDescription', 'tabIndex']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ariaLabel', 'className', 'description', 'error', 'errorMessage', 'header', 'icon', 'items', 'largeSize', 'open', 'placeholder', 'searchable', 'selectedItem', 'showDescription', 'tabIndex']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Dropdown3, self).__init__(**args)
