import argparse

from tp2.utils.config import logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    logger.info("Samples : %s, rules : %s, out : %s", args.samples, args.rules, args.out)


if __name__ == "__main__":
    main()