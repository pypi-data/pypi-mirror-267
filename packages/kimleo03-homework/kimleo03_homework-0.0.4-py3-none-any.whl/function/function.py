import requests
import re
def format_currency(amount, currency_symbol="$", local="en_US"):
    import babel.numbers
    return babel.numbers.format_currency(amount, currency_symbol, local=local)

def validate_email(email):
    pattern = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    #insert email in pattern part
    return re.fullmatch(pattern, email) is not None


def convert_temperature(temp, to_scale='F'):
    if to_scale.upper() == 'C':
        return (temp - 32) * 5.0/9.0
    elif to_scale.upper() == 'F':
        return temp * 9.0/5.0 + 32
    else:
        raise ValueError("Unsupported scale. Use 'C' for Celsius or 'F' for Fahrenheit.")
def merge_dictionaries(*dicts):
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result

def download_file(url, computer_filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(computer_filename, 'wb') as f:
        f.write(response.content)
