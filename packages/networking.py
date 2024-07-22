import ipaddress
import itertools
from typing import TypeAlias

IPv4Network: TypeAlias = ipaddress.IPv4Network


class NetworkSummarizer:
    """Sumariza las redes indicadas dependiendo del porcentaje de coincidencia
    que indique el usuario, por ejemplo:

    las redes 10.10.0.0/24 y 10.10.2.0/24 no son contiguas pero se pueden
    sumarizar en la red 10.10.0.0/26 si el usuario así lo requiere, esta red
    contiene 1024 direcciones IP, la suma de las direcciones IP de las redes
    10.10.0.0/24 y 10.10.2.0/24 es de 512, luego el porcentaje de coincidencia
    es 50%. Si el usuario ingresa un porcentaje mayor a 50%, las redes no se van
    a sumarizar.
    """
    
    def __init__(self, percentage: float, networks: list[IPv4Network]) -> None:
        """Inicializa el objeto con el porcentaje de coincidencia y las redes a
        sumarizar.

        Args:
            percentage (float): porcentaje de coincidencia
            networks (list[IPv4Network]): listado con las redes a sumarizar
        """
        self._hosts_percentage = percentage
        self._networks = sorted(networks)

    @property
    def aggregated_networks(self, ip_format: bool = False) -> list[str] | list[IPv4Network]:
        """Retorna una lista con las redes sumarizadas.

        Args:
            ip_format (bool, optional): si es True, retorna la lista con las
            direcciones en formato IPv4Network, de lo contrario retorna la lista
            con valores string. Defaults to False.

        Returns:
            list[str] | list[IPv4Network]: lista de redes sumarizadas
        """
        if ip_format:
            return self._networks
        return [network.compressed for network in self._networks]

    @property
    def aggregated_networks_human_readable(self) -> str:
        """Retorna las redes sumarizadas en formato legible para humanos.

        Returns:
            str: mensaje con las redes sumarizadas
        """
        return 'Redes sumarizadas:\n' + '\n'.join([network.compressed for network in self._networks])

    @staticmethod
    def _calculate_percentage(value1: float, value2: float) -> float:
        """Calcula la relación de porcentaje entre dos valores.

        Args:
            value1 (float): valor total
            value2 (float): valor a comparar

        Returns:
            float: porcentaje
        """
        return round((value2 / value1) * 100, 2)

    @staticmethod
    def _summarize_with_next(network1: IPv4Network, network2: IPv4Network) -> IPv4Network:
        """Sumariza las dos redes indicadas.

        Args:
            network1 (IPv4Network): primera red
            network2 (IPv4Network): segunda red

        Returns:
            IPv4Network: red sumarizada
        """
        if network1.prefixlen >= network2.prefixlen:
            major_network = network1
            minor_network = network2
        else:
            major_network = network2
            minor_network = network1
        max_prefix = 1
        supernet = major_network.supernet(prefixlen_diff=max_prefix)
        while not supernet.supernet_of(minor_network):
            supernet = major_network.supernet(prefixlen_diff=max_prefix)
            max_prefix += 1
        return supernet

    def _calculate_host_percentage(
            self, aggregated_network: IPv4Network, network1: IPv4Network, network2: IPv4Network
    ) -> float:
        """Calcula el porcentaje de coincidencia entrela la suma de las redes
        indicadas y la red sumarizada.

        Args:
            aggregated_network (IPv4Network): red sumarizada
            network1 (IPv4Network): primera red
            network2 (IPv4Network): segunda red

        Returns:
            float: porcentaje de coincidencia de las 2 redes no sumarizadas con
            respecto a la red sumarizada
        """
        total_hosts = aggregated_network.num_addresses
        networks_hosts = network1.num_addresses + network2.num_addresses
        return self._calculate_percentage(total_hosts, networks_hosts)

    def summarize(self) -> None:
        """Función principal de la clase, inicia la sumarización de las redes.
        """
        networks_changed = False
        for network_pairs in itertools.pairwise(self._networks):
            aggregated_network = self._summarize_with_next(network_pairs[0], network_pairs[1])
            percentage = self._calculate_host_percentage(aggregated_network, network_pairs[0], network_pairs[1])
            if percentage >= self._hosts_percentage:
                self._networks.remove(network_pairs[0])
                self._networks.remove(network_pairs[1])
                self._networks.append(aggregated_network)
                self._networks = sorted(self._networks)
                networks_changed = True
                break
        if networks_changed:
            self.summarize()
