import unittest
import ipaddress

from packages.networking import NetworkSummarizer


class SummarizeTestCases(unittest.TestCase):

    def test_adjacent_networks(self):
        networks = ['1.1.0.0/24', '1.1.1.0/24']
        networks = [ipaddress.ip_network(network) for network in networks]
        summarizer = NetworkSummarizer(50, networks)
        summarizer.summarize()
        aggregated = summarizer.aggregated_networks
        self.assertEqual(aggregated, ['1.1.0.0/23'])

    def test_not_adjacent_networks(self):
        networks = ['1.1.0.0/24', '1.1.2.0/24']
        networks = [ipaddress.ip_network(network) for network in networks]
        summarizer = NetworkSummarizer(50, networks)
        summarizer.summarize()
        aggregated = summarizer.aggregated_networks
        self.assertEqual(aggregated, ['1.1.0.0/22'])

    def test_not_adjacent_networks_low_coincidence_percentage(self):
        networks = ['1.1.0.0/24', '1.1.2.0/24']
        networks = [ipaddress.ip_network(network) for network in networks]
        summarizer = NetworkSummarizer(75, networks)
        summarizer.summarize()
        aggregated = summarizer.aggregated_networks
        self.assertEqual(aggregated, ['1.1.0.0/24', '1.1.2.0/24'])

    def test_not_adjacent_networks_high_coincidence_percentage(self):
        networks = ['1.1.0.0/24', '1.1.2.0/24', '1.1.3.0/24']
        networks = [ipaddress.ip_network(network) for network in networks]
        summarizer = NetworkSummarizer(75, networks)
        summarizer.summarize()
        aggregated = summarizer.aggregated_networks
        self.assertEqual(aggregated, ['1.1.0.0/22'])
