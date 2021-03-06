import types


def new(argument, **keywords):
    r"""
    Makes new ``argument`` with ``keywords``.

    ..  container:: example

        Makes markup with new direction:

        >>> markup = abjad.Markup('Andante assai', direction=abjad.Up).italic()
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                ^ \markup {
                    \italic
                        "Andante assai"
                    }
                d'4
                e'4
                f'4
            }

        >>> markup = abjad.new(markup, direction=abjad.Down)
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                _ \markup {
                    \italic
                        "Andante assai"
                    }
                d'4
                e'4
                f'4
            }


    ..  container:: example

        REGRESSION. Can be used to set existing properties to none:

        >>> markup = abjad.Markup('Andante assai', direction=abjad.Up).italic()
        >>> abjad.f(markup)
        ^ \markup {
            \italic
                "Andante assai"
            }

        >>> markup = abjad.new(markup, direction=None)
        >>> abjad.f(markup)
        \markup {
            \italic
                "Andante assai"
            }

    Returns new object with type equal to that of ``argument``.
    """
    import abjad
    if argument is None:
        return argument
    manager = abjad.StorageFormatManager(argument)
    template_dict = manager.get_template_dict()
    recursive_arguments = {}
    for key, value in keywords.items():
        if '__' in key:
            key, divider, subkey = key.partition('__')
            if key not in recursive_arguments:
                recursive_arguments[key] = []
            pair = (subkey, value)
            recursive_arguments[key].append(pair)
            continue
        if key in template_dict or manager.signature_accepts_kwargs:
            template_dict[key] = value
        elif isinstance(getattr(argument, key, None), types.MethodType):
            method = getattr(argument, key)
            result = method(value)
            if isinstance(result, type(argument)):
                argument = result
                manager_ = abjad.StorageFormatManager(argument)
                template_dict.update(manager_.get_template_dict())
        else:
            message = f'{type(argument)} has no key {key!r}.'
            raise KeyError(message)
    for key, pairs in recursive_arguments.items():
        recursed_object = getattr(argument, key)
        if recursed_object is None:
            continue
        recursive_template_dict = dict(pairs)
        recursed_object = new(recursed_object, **recursive_template_dict)
        if key in template_dict:
            template_dict[key] = recursed_object
    positional_values = []
    for name in manager.signature_positional_names:
        if name in template_dict:
            positional_values.append(template_dict.pop(name))
    result = type(argument)(*positional_values, **template_dict)
    for name in getattr(argument, '_private_attributes_to_copy', []):
        value = getattr(argument, name, None)
        setattr(result, name, value)
    return result
