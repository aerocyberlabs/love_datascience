from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import evaluate_default_rule, load_credit_rows, train_default_rule


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Train and evaluate a simple credit default rule."
    )
    parser.add_argument("training_csv", type=Path, help="Path to credit training data")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    rows = load_credit_rows(args.training_csv)
    rule = train_default_rule(rows)
    metrics = evaluate_default_rule(rule, rows)
    print(
        f"Best feature={rule['feature']}, threshold={rule['threshold']}, "
        f"accuracy={metrics['accuracy']:.3f}, "
        f"precision={metrics['precision']:.3f}, "
        f"recall={metrics['recall']:.3f}"
    )


if __name__ == "__main__":
    main()
