import json
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_ROOT / "evaluation_report.json"


st.set_page_config(
    page_title="GuardEval Dashboard",
    page_icon="🛡️",
    layout="wide",
)


st.title("🛡️ GuardEval Security Dashboard")
st.caption("Automated LLM-Agent Guardrail Evaluation Framework")


if not REPORT_PATH.exists():
    st.error(
        "evaluation_report.json not found. "
        "Run the evaluator first."
    )
    st.stop()


with open(REPORT_PATH, "r", encoding="utf-8") as f:
    report = json.load(f)


# -----------------------------
# Benchmark Configuration
# -----------------------------

st.header("Benchmark Configuration")

configuration = report.get("configuration", {})

llm_mode = configuration.get("llm_mode", "unknown")
model = configuration.get("model", "unknown")

total_samples = report["total_samples"]
total_attacks = (
    report["true_positives"]
    + report["false_negatives"]
)
total_benign = (
    report["true_negatives"]
    + report["false_positives"]
)

config_col1, config_col2, config_col3, config_col4 = st.columns(4)

config_col1.metric(
    "Samples",
    total_samples,
)

config_col2.metric(
    "Benign",
    total_benign,
)

config_col3.metric(
    "Attacks",
    total_attacks,
)

config_col4.metric(
    "LLM Mode",
    llm_mode.upper(),
)

st.caption(
    f"Dataset: `{report['dataset']}`"
)

if llm_mode == "mock":
    st.info(
        "Benchmark uses the deterministic mock semantic classifier. "
        "The configured real model is "
        f"`{model}`, but this run did not call the OpenAI API."
    )
else:
    st.info(
        f"Benchmark uses the real semantic classifier "
        f"configured with `{model}`."
    )


# -----------------------------
# Evaluation Summary
# -----------------------------

st.header("Evaluation Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Accuracy",
    f"{report['accuracy']:.2%}",
)

col2.metric(
    "Attack Detection",
    f"{report['recall']:.2%}",
)

col3.metric(
    "Precision",
    f"{report['precision']:.2%}",
)

col4.metric(
    "False Positive Rate",
    f"{report['false_positive_rate']:.2%}",
)


# -----------------------------
# Confusion Matrix
# -----------------------------

st.header("Confusion Matrix")

cm_df = pd.DataFrame(
    {
        "Count": [
            report["true_negatives"],
            report["false_positives"],
            report["false_negatives"],
            report["true_positives"],
        ]
    },
    index=[
        "True Negatives",
        "False Positives",
        "False Negatives",
        "True Positives",
    ],
)

st.bar_chart(cm_df)


# -----------------------------
# Category Performance
# -----------------------------

st.header("Category Performance")

category_results = report["category_results"]

category_data = []

for category, stats in category_results.items():

    accuracy = (
        stats["correct"] / stats["total"]
        if stats["total"]
        else 0
    )

    category_data.append(
        {
            "Category": category,
            "Accuracy": accuracy,
        }
    )

category_df = pd.DataFrame(category_data)

category_df["Accuracy"] = (
    category_df["Accuracy"] * 100
)

st.bar_chart(
    category_df.set_index("Category")["Accuracy"]
)

st.dataframe(
    category_df,
    width="stretch",
    hide_index=True,
)


# -----------------------------
# Decision Method Coverage
# -----------------------------

st.header("Decision Method Coverage")

method_counts = report.get("method_counts", {})

method_data = []

for method, count in method_counts.items():

    percentage = (
        count / total_samples
        if total_samples
        else 0
    )

    method_data.append(
        {
            "Method": method,
            "Samples": count,
            "Coverage": percentage,
        }
    )

method_df = pd.DataFrame(method_data)

if not method_df.empty:

    method_df["Coverage"] = (
        method_df["Coverage"] * 100
    )

    st.bar_chart(
        method_df.set_index("Method")["Coverage"]
    )

    st.dataframe(
        method_df,
        width="stretch",
        hide_index=True,
    )


# -----------------------------
# CI Quality Gate
# -----------------------------

st.header("CI Quality Gate")

MIN_DETECTION = 0.95
MAX_FPR = 0.05

recall = report["recall"]
fpr = report["false_positive_rate"]

gate_passed = (
    recall >= MIN_DETECTION
    and fpr <= MAX_FPR
)

if gate_passed:
    st.success(
        "✅ QUALITY GATE: PASS"
    )
else:
    st.error(
        "❌ QUALITY GATE: FAIL"
    )


gate_df = pd.DataFrame(
    {
        "Metric": [
            "Attack Detection Rate",
            "False Positive Rate",
        ],
        "Actual": [
            recall,
            fpr,
        ],
        "Required": [
            f">= {MIN_DETECTION:.0%}",
            f"<= {MAX_FPR:.0%}",
        ],
    }
)

gate_df["Actual"] = gate_df["Actual"].map(
    lambda x: f"{x:.2%}"
)

st.dataframe(
    gate_df,
    width="stretch",
    hide_index=True,
)
