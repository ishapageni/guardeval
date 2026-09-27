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

from guardrails.hybrid_guard import hybrid_check


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = Path(
    os.getenv(
        "GUARDEVAL_DATASET",
        PROJECT_ROOT / "dataset" / "test_extended.jsonl",
    )
)


def load_dataset(path=DATASET_PATH):
    samples = []

    with open(path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                samples.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {path} at line {line_number}: {exc}"
                ) from exc

    return samples


def evaluate(dataset):
    y_true = []
    y_pred = []

    category_results = {}
    method_counts = {}

    for sample in dataset:
        prompt = sample["prompt"]

        # Evaluate the complete hybrid guard.
        result = hybrid_check(prompt)

        expected_action = sample["expected_action"]
        actual_action = result["action"]

        expected_label = (
            1 if expected_action != "allow" else 0
        )

        actual_label = (
            1 if actual_action != "allow" else 0
        )

        y_true.append(expected_label)
        y_pred.append(actual_label)

        # Track which layer produced the decision.
        method = result.get("method", "unknown")

        method_counts[method] = (
            method_counts.get(method, 0) + 1
        )

        # ---------------------------------------------
        # Category-level evaluation
        # ---------------------------------------------

        category = sample["category"]

        if category not in category_results:
            category_results[category] = {
                "total": 0,
                "correct": 0,
                "false_negatives": 0,
                "false_positives": 0,
            }

        stats = category_results[category]

        stats["total"] += 1

        if expected_label == actual_label:
            stats["correct"] += 1

        if expected_label == 1 and actual_label == 0:
            stats["false_negatives"] += 1

        if expected_label == 0 and actual_label == 1:
            stats["false_positives"] += 1

    # ---------------------------------------------
    # Overall metrics
    # ---------------------------------------------

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

    false_positive_rate = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0
    )

    false_negative_rate = (
        fn / (fn + tp)
        if (fn + tp) > 0
        else 0
    )

    specificity = (
        tn / (tn + fp)
        if (tn + fp) > 0
        else 0
    )

    # ---------------------------------------------
    # Print results
    # ---------------------------------------------

    print("=" * 60)
    print("GUARDEVAL - HYBRID GUARD EVALUATION")
    print("=" * 60)

    print(f"Dataset:                 {DATASET_PATH}")
    print(f"Total samples:           {len(dataset)}")
    print(
        f"LLM mode:                "
        f"{os.getenv('GUARDEVAL_LLM_MODE', 'mock')}"
    )
    print(
        f"LLM model:               "
        f"{os.getenv('OPENAI_MODEL', 'gpt-5.6-luna')}"
    )

    print()
    print(f"Accuracy:                {accuracy:.2%}")
    print(f"Precision:               {precision:.2%}")
    print(f"Attack detection rate:   {recall:.2%}")
    print(f"F1 score:                {f1:.2%}")
    print(f"False positive rate:     {false_positive_rate:.2%}")
    print(f"False negative rate:     {false_negative_rate:.2%}")
    print(f"Specificity:             {specificity:.2%}")

    print()
    print("Decision Method Coverage")
    print("-" * 40)

    for method, count in sorted(method_counts.items()):
        percentage = count / len(dataset)

        print(
            f"{method:20s}"
            f"{count:4d} "
            f"({percentage:.2%})"
        )

    print()
    print("Confusion Matrix")
    print("-" * 40)

    print(f"True Negatives:    {tn}")
    print(f"False Positives:   {fp}")
    print(f"False Negatives:   {fn}")
    print(f"True Positives:    {tp}")

    print()
    print("Category Performance")
    print("-" * 60)

    for category, stats in category_results.items():
        category_accuracy = (
            stats["correct"] / stats["total"]
            if stats["total"]
            else 0
        )

        print(
            f"{category:25s}"
            f"{category_accuracy:.2%}"
        )

    print("=" * 60)

    return {
        "dataset": str(DATASET_PATH),
        "total_samples": len(dataset),

        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,

        "false_positive_rate": false_positive_rate,
        "false_negative_rate": false_negative_rate,
        "specificity": specificity,

        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "true_positives": tp,

        "category_results": category_results,
        "method_counts": method_counts,

        "configuration": {
            "llm_mode": os.getenv(
                "GUARDEVAL_LLM_MODE",
                "mock",
            ),
            "model": os.getenv(
                "OPENAI_MODEL",
                "gpt-5.6-luna",
            ),
        },
    }


if __name__ == "__main__":
    dataset = load_dataset()

    results = evaluate(dataset)

    report_path = PROJECT_ROOT / "evaluation_report.json"

    with open(
        report_path,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            results,
            f,
            indent=2,
            default=lambda x: (
                x.item()
                if hasattr(x, "item")
                else x
            ),
        )

    print(
        f"\nJSON report written to {report_path}"
    )
