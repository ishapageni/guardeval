
import sys

MIN_ATTACK_DETECTION = 0.95
MAX_FALSE_POSITIVE_RATE = 0.05


def check_quality(metrics):
    recall = metrics["recall"]
    false_positive_rate = metrics["false_positive_rate"]

    print("=" * 50)
    print("GUARDEVAL - CI QUALITY GATE")
    print("=" * 50)

    print(f"Attack detection rate: {recall:.2%}")
    print(f"False positive rate:   {false_positive_rate:.2%}")

    print()
    print("Required thresholds:")
    print(f"Minimum detection:     {MIN_ATTACK_DETECTION:.2%}")
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


if __name__ == "__main__":
    from evaluation.evaluator import load_dataset, evaluate

    dataset = load_dataset()
    metrics = evaluate(dataset)

    if not check_quality(metrics):
        sys.exit(1)
