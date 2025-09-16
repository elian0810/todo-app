
def formatErrors(errors):
   
    """
    Funcion que formatea los errores proporcionado por los serializadores
    """
    first_error_key =next(iter(errors))
    fisrt_error = errors[first_error_key]
   
    if isinstance(fisrt_error,dict) : custom_message_error=fisrt_error[list(fisrt_error.keys())[0]][0]
    else : custom_message_error=fisrt_error[0]
   
    if custom_message_error == 'Este campo es requerido.':
        custom_message_error = f'El campo {first_error_key} es requerido.'
    if custom_message_error == 'Este campo no puede ser nulo.':
        custom_message_error = f'El campo {first_error_key} es requerido.'
    return custom_message_error
