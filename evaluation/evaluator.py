
import json
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
)

from guardrails.input_guard import check_input


DATASET_PATH = Path(__file__).resolve().parent.parent / "dataset" / "test_extended.jsonl"


def load_dataset(path=DATASET_PATH):
    samples = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            samples.append(json.loads(line))

    return samples


def evaluate(dataset):
    y_true = []
    y_pred = []

    category_results = {}

    for sample in dataset:

        prompt = sample["prompt"]

        # Run our guardrail
        result = check_input(prompt)

        expected_action = sample["expected_action"]
        actual_action = result["action"]

        # Convert:
        # allow = 0
        # block = 1

        expected_label = (
            1 if expected_action == "block" else 0
        )

        actual_label = (
            1 if actual_action == "block" else 0
        )

        y_true.append(expected_label)
        y_pred.append(actual_label)

        # Category-level evaluation
        category = sample["category"]

        if category not in category_results:
            category_results[category] = {
                "total": 0,
                "correct": 0,
                "false_negatives": 0,
                "false_positives": 0,
            }

        category_results[category]["total"] += 1

        if expected_label == actual_label:
            category_results[category]["correct"] += 1

        if expected_label == 1 and actual_label == 0:
            category_results[category]["false_negatives"] += 1

        if expected_label == 0 and actual_label == 1:
            category_results[category]["false_positives"] += 1

    # Overall metrics

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

    # Print results

    print("=" * 50)
    print("GUARDEVAL - GUARDRAIL EVALUATION")
    print("=" * 50)

    print(f"Total samples:          {len(dataset)}")
    print(f"Accuracy:               {accuracy:.2%}")
    print(f"Precision:              {precision:.2%}")
    print(f"Attack detection rate:  {recall:.2%}")
    print(f"False positive rate:    {false_positive_rate:.2%}")
    print(f"False negative rate:    {false_negative_rate:.2%}")

    print("\nConfusion Matrix")
    print("-" * 30)

    print(f"True Negatives:   {tn}")
    print(f"False Positives:  {fp}")
    print(f"False Negatives:  {fn}")
    print(f"True Positives:   {tp}")

    print("\nCategory Performance")
    print("-" * 50)

    for category, stats in category_results.items():

        category_accuracy = (
            stats["correct"] / stats["total"]
        )

        print(
            f"{category:22s} "
            f"{category_accuracy:.2%}"
        )

    print("=" * 50)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "false_positive_rate": false_positive_rate,
        "false_negative_rate": false_negative_rate,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "true_positives": tp,
        "category_results": category_results,
    }


if __name__ == "__main__":
    dataset = load_dataset()
    results = evaluate(dataset)
    with open("evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=lambda x: x.item() if hasattr(x, "item") else x)
    print("JSON report written to evaluation_report.json")
