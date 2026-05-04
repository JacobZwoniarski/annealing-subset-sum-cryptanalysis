"""Small CLI used to verify that the package imports correctly."""

from annealing_crypto import __version__


def main() -> None:
    print(f"annealing_crypto {__version__}")


if __name__ == "__main__":
    main()
