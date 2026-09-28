import json
import os
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from guardrails.input_guard import check_input
from guardrails.hybrid_guard import hybrid_check


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = Path(
    os.getenv(
        "GUARDEVAL_DATASET",
        PROJECT_ROOT
        / "dataset"
        / "test_realistic_95_5_adversarial.jsonl",
    )
)


def load_dataset(path):
    with open(path, "r", encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


def calculate_metrics(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0,
    )
    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0,
    )
    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()

    fpr = fp / (fp + tn) if (fp + tn) else 0
    fnr = fn / (fn + tp) if (fn + tp) else 0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "fpr": fpr,
        "fnr": fnr,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
    }


def evaluate_no_guard(dataset):
    """
    Baseline 1:
    No security guard.

    Every request is allowed.
    """

    y_true = []
    y_pred = []

    for sample in dataset:
        expected = (
            1 if sample["expected_action"] != "allow" else 0
        )

        y_true.append(expected)
        y_pred.append(0)

    return calculate_metrics(y_true, y_pred)


def evaluate_rule_only(dataset):
    """
    Baseline 2:
    Deterministic rule guard only.
    """

    y_true = []
    y_pred = []

    for sample in dataset:
        result = check_input(sample["prompt"])

        expected = (
            1 if sample["expected_action"] != "allow" else 0
        )

        actual = (
            1 if result["action"] != "allow" else 0
        )

        y_true.append(expected)
        y_pred.append(actual)

    return calculate_metrics(y_true, y_pred)


def evaluate_hybrid(dataset):
    """
    System under evaluation:
    deterministic rules + semantic guard.
    """

    y_true = []
    y_pred = []

    for sample in dataset:
        result = hybrid_check(sample["prompt"])

        expected = (
            1 if sample["expected_action"] != "allow" else 0
        )

        actual = (
            1 if result["action"] != "allow" else 0
        )

        y_true.append(expected)
        y_pred.append(actual)

    return calculate_metrics(y_true, y_pred)


def print_result(name, result):
    print()
    print(name)
    print("-" * 60)

    print(f"Accuracy:              {result['accuracy']:.2%}")
    print(f"Precision:             {result['precision']:.2%}")
    print(f"Attack detection:      {result['recall']:.2%}")
    print(f"F1:                    {result['f1']:.2%}")
    print(f"False positive rate:   {result['fpr']:.2%}")
    print(f"False negative rate:   {result['fnr']:.2%}")

    print()
    print(
        f"TN={result['tn']}  "
        f"FP={result['fp']}  "
        f"FN={result['fn']}  "
        f"TP={result['tp']}"
    )


def main():
    dataset = load_dataset(DATASET_PATH)

    print("=" * 60)
    print("GUARDEVAL - BASELINE COMPARISON")
    print("=" * 60)
    print(f"Dataset: {DATASET_PATH}")
    print(f"Samples: {len(dataset)}")
    print("LLM mode:", os.getenv("GUARDEVAL_LLM_MODE", "mock"))

    results = {
        "No Guard": evaluate_no_guard(dataset),
        "Rule Only": evaluate_rule_only(dataset),
        "Hybrid": evaluate_hybrid(dataset),
    }

    for name, result in results.items():
        print_result(name, result)

    print()
    print("=" * 60)
    print("COMPARISON")
    print("=" * 60)

    print(
        f"{'Method':<15}"
        f"{'Accuracy':>12}"
        f"{'Recall':>12}"
        f"{'F1':>12}"
        f"{'FNR':>12}"
    )

    print("-" * 60)

    for name, result in results.items():
        print(
            f"{name:<15}"
            f"{result['accuracy']:>11.2%}"
            f"{result['recall']:>11.2%}"
            f"{result['f1']:>11.2%}"
            f"{result['fnr']:>11.2%}"
        )


if __name__ == "__main__":
    main()
