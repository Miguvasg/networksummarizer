import ipaddress

def get_networks() -> list[ipaddress.IPv4Network]:
    try:
        user_info = input('Ingresa las redes separadas por coma:\n')
        return [ipaddress.ip_network(network) for network in user_info.replace(' ', '').split(',')]
    except Exception as error:
        print(f'\nError: {error}\n')
        get_networks()
