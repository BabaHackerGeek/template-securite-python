import argparse

from src.tp3.utils.config import logger
from src.tp3.utils.network import breach_network
from src.tp3.utils.web import breach_web


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    logger.info(f"Lancement contre {args.target}")

    host, port, key, flag1 = breach_web(args.target)
    print(f"[+] FLAG1: {flag1}")

    flag_final = breach_network(host, port, key)
    print(f"[+] FLAG_FINAL: {flag_final}")


if __name__ == "__main__":
    main()
