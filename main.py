from packages import parser, front, networking


def main() -> None:
    """Función principal, lee los argumentos ingresados por el usuario, solicita
    las redes a sumarizar e inicia la sumarización.
    """
    args = parser.get_args()
    networks = front.get_networks()
    agent = networking.NetworkSummarizer(args.percentage, networks)
    agent.summarize()
    print(agent.aggregated_networks)
    print(agent.aggregated_networks_human_readable)


if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        print(error)
