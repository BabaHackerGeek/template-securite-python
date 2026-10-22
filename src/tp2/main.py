import argparse

from tp2.utils.analyzer import process_samples
from tp2.utils.config import logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    logger.info("Samples : %s, rules : %s, out : %s", args.samples, args.rules, args.out)
    chemins = process_samples(args.samples, args.out)
    logger.info("%d rapport(s) écrit(s) dans %s", len(chemins), args.out)


if __name__ == "__main__":
    main()