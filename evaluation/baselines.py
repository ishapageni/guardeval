import json
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

DATASET_PATH = (
    PROJECT_ROOT
    / "dataset"
    / "test_extended.jsonl"
)


def load_dataset():
    samples = []

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line:
                samples.append(json.loads(line))

    return samples


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

    fpr = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_positive_rate": fpr,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "true_positives": tp,
    }


def no_guard(prompt):
    # Baseline: every request is allowed.
    return "allow"


def regex_guard(prompt):
    result = check_input(prompt)
    return result["action"]


def hybrid_guard(prompt):
    result = hybrid_check(prompt)
    return result["action"]


def evaluate_system(name, classifier, dataset):
    y_true = []
    y_pred = []

    for sample in dataset:
        expected = sample["expected_action"]

        expected_label = (
            1
            if expected != "allow"
            else 0
        )

        actual = classifier(sample["prompt"])

        actual_label = (
            1
            if actual != "allow"
            else 0
        )

        y_true.append(expected_label)
        y_pred.append(actual_label)

    metrics = calculate_metrics(
        y_true,
        y_pred,
    )

    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    print(
        f"Accuracy:              "
        f"{metrics['accuracy']:.2%}"
    )

    print(
        f"Precision:             "
        f"{metrics['precision']:.2%}"
    )

    print(
        f"Attack detection:      "
        f"{metrics['recall']:.2%}"
    )

    print(
        f"F1 score:              "
        f"{metrics['f1']:.2%}"
    )

    print(
        f"False positive rate:   "
        f"{metrics['false_positive_rate']:.2%}"
    )

    print()
    print("Confusion Matrix")
    print(
        f"TN={metrics['true_negatives']} "
        f"FP={metrics['false_positives']} "
        f"FN={metrics['false_negatives']} "
        f"TP={metrics['true_positives']}"
    )

    return metrics


if __name__ == "__main__":
    dataset = load_dataset()

    print("=" * 60)
    print("GUARDEVAL - BASELINE COMPARISON")
    print("=" * 60)
    print(f"Dataset: {DATASET_PATH}")
    print(f"Samples: {len(dataset)}")

    no_guard_metrics = evaluate_system(
        "1. NO GUARD",
        no_guard,
        dataset,
    )

    regex_metrics = evaluate_system(
        "2. REGEX-ONLY GUARD",
        regex_guard,
        dataset,
    )

    hybrid_metrics = evaluate_system(
        "3. HYBRID GUARD (MOCK SEMANTIC)",
        hybrid_guard,
        dataset,
    )

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(
        f"{'System':35s}"
        f"{'Accuracy':>12s}"
        f"{'Detection':>12s}"
        f"{'FPR':>10s}"
        f"{'F1':>10s}"
    )

    print("-" * 80)

    for name, metrics in [
        ("No guard", no_guard_metrics),
        ("Regex-only", regex_metrics),
        ("Hybrid mock", hybrid_metrics),
    ]:
        print(
            f"{name:35s}"
            f"{metrics['accuracy']:>11.2%}"
            f"{metrics['recall']:>11.2%}"
            f"{metrics['false_positive_rate']:>9.2%}"
            f"{metrics['f1']:>9.2%}"
        )
