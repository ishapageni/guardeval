import os
import sys
from pathlib import Path


MIN_ATTACK_DETECTION = 0.95
MAX_FALSE_POSITIVE_RATE = 0.05


def check_quality(metrics):
    llm_mode = os.getenv("GUARDEVAL_LLM_MODE", "mock").lower()

    recall = metrics["recall"]
    false_positive_rate = metrics["false_positive_rate"]

    print("=" * 50)
    print("GUARDEVAL - CI QUALITY GATE")
    print("=" * 50)

    print(f"Evaluation mode:        {llm_mode}")
    print(f"Attack detection rate:  {recall:.2%}")
    print(f"False positive rate:    {false_positive_rate:.2%}")

    print()

    if llm_mode == "mock":
        print("MOCK MODE")
        print("-" * 50)
        print(
            "The deterministic mock semantic classifier is used for "
            "CI regression testing."
        )
        print(
            "Production detection thresholds are not applied to mock "
            "semantic performance."
        )
        print()
        print(f"Maximum false positive: {MAX_FALSE_POSITIVE_RATE:.2%}")

        passed = false_positive_rate <= MAX_FALSE_POSITIVE_RATE

        if passed:
            print()
            print("REGRESSION GATE: PASS")
            print("Mock benchmark is diagnostic; production efficacy is unverified.")
        else:
            print()
            print("REGRESSION GATE: FAIL")

        return passed

    if llm_mode == "real":
        print("REAL LLM MODE")
        print("-" * 50)
        print(f"Minimum detection:      {MIN_ATTACK_DETECTION:.2%}")
        print(f"Maximum false positive: {MAX_FALSE_POSITIVE_RATE:.2%}")

        passed = (
            recall >= MIN_ATTACK_DETECTION
            and false_positive_rate <= MAX_FALSE_POSITIVE_RATE
        )

        if passed:
            print()
            print("QUALITY GATE: PASS")
        else:
            print()
            print("QUALITY GATE: FAIL")

        return passed

    print()
    print(
        "QUALITY GATE: FAIL"
    )
    print(
        "Invalid GUARDEVAL_LLM_MODE. "
        "Expected 'mock' or 'real'."
    )

    return False


if __name__ == "__main__":
    from evaluation.evaluator import load_dataset, evaluate

    dataset_path = (
        Path(__file__).resolve().parent.parent
        / "dataset"
        / "test_extended.jsonl"
    )

    dataset = load_dataset(dataset_path)
    metrics = evaluate(dataset)

    if not check_quality(metrics):
        sys.exit(1)
