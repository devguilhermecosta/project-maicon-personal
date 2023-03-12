import os


def __get_variable(env_variable: str, default: str = '') -> str:
    return os.environ.get(env_variable, default)


def __str_format(variable: str | list | tuple) -> str:
    if not isinstance(variable, str):
        try:
            variable = str(variable)
        except Exception as e:
            print(e, 'Required str format.')
    return str(variable).replace('(', '').replace(')', '')


def convert_str_to_list(env_variable: str) -> list:
    format_var: str = __str_format(__get_variable(env_variable))

    data_list: list = [
        letter.strip().replace(',', '') for letter in format_var.split()
    ]

    return data_list
