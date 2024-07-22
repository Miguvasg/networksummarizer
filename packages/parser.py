import argparse

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--percentage',
        type=float,
        default=50.0,
        help='porcentaje que debe cubrir los segmentos sumarizados con respecto a la supernet'
    )
    return parser.parse_args()
