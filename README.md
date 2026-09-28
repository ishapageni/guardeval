# GuardEval

**GuardEval** is an automated evaluation framework for testing security guardrails used in LLM-powered agents.

The project evaluates a hybrid guard architecture that combines:

1. Deterministic rule-based input filtering
2. Semantic security classification
3. Centralized risk policy enforcement
4. Automated benchmark evaluation
5. Baseline comparison
6. Interactive Streamlit visualization
7. CI-oriented quality gates

The framework is designed to measure both security detection and false-positive behavior rather than relying only on individual examples.

---

## Key Features

- Prompt-injection detection
- Jailbreak detection
- Data-exfiltration detection
- Tool-abuse detection
- Malicious-code detection
- Deterministic rule guard
- Semantic-risk classifier
- Hybrid security guard
- Precision, recall, F1, accuracy, specificity
- False-positive and false-negative rates
- Confusion-matrix analysis
- Category-level evaluation
- Decision-method coverage
- Baseline comparison
- Controlled benchmark datasets
- Unseen holdout evaluation
- JSON evaluation reports
- Streamlit dashboard
- CI quality gate

---

# Architecture

```text
User Prompt
     │
     ▼
┌─────────────────────┐
│   Rule-Based Guard  │
│                     │
│ Injection patterns  │
│ Sensitive requests  │
│ Dangerous actions   │
└──────────┬──────────┘
           │
      Block? ──────── Yes ──────► Policy ──► BLOCK
           │
           │ No
           ▼
┌─────────────────────┐
│ Semantic Guard      │
│                     │
│ Mock classifier     │
│ or real LLM         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Risk Policy      │
│                     │
│ Final decision      │
└──────────┬──────────┘
           │
           ▼
       ALLOW / BLOCK
The semantic layer can operate in two modes:

* mock — deterministic local semantic-risk simulator
* real — OpenAI-backed semantic classifier

Security Benchmark

GuardEval uses controlled benchmark datasets containing benign requests and security attacks.

The primary development benchmark contains:

* 400 total samples
* 380 benign samples
* 20 attack samples
* 95% benign / 5% attack distribution
* 4 examples per attack category

Attack categories:

* Prompt injection
* Data exfiltration
* Tool abuse
* Jailbreak
* Malicious code

The 400-sample benchmark is a controlled evaluation dataset, not 400 independent real-world observations. Some benign prompts are reused across controlled variants to test consistency.

400-Sample Development Benchmark

The development benchmark was evaluated using:

```bash
GUARDEVAL_DATASET=dataset/test_realistic_95_5_400.jsonl \
GUARDEVAL_LLM_MODE=mock \
python -m evaluation.evaluator

## Results

| System | Accuracy | Attack Detection | Precision | F1 | FPR | FNR |
|---|---:|---:|---:|---:|---:|---:|
| No Guard | 95.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% |
| Rule Only | 96.75% | 35.00% | 100.00% | 51.85% | 0.00% | 65.00% |
| Hybrid Guard | 100.00% | 100.00% | 100.00% | 100.00% | 0.00% | 0.00% |

### Hybrid Confusion Matrix

| | Actual Benign | Actual Attack |
|---|---:|---:|
| **Predicted Benign** | 380 | 0 |
| **Predicted Attack** | 0 | 20 |

| Metric | Count |
|---|---:|
| True Negatives | 380 |
| False Positives | 0 |
| False Negatives | 0 |
| True Positives | 20 |

The hybrid guard detected all 20 attacks in this controlled development benchmark while producing no false positives.

> **Important:** This result should not be interpreted as general real-world security performance.

Unseen 200-Sample Holdout Benchmark

To test generalization, GuardEval includes a separate holdout dataset that was generated after the development classifier was finalized.

Dataset:
dataset/test_holdout_200.jsonl
Composition:

* 200 total samples
* 180 benign
* 20 attacks
* 4 attacks per category
* IDs 1001–1200

The attack wording differs from the development benchmark.

The classifier was not modified after observing these results. Therefore, this benchmark is treated as an unseen evaluation rather than another tuning dataset.

Run:
GUARDEVAL_DATASET=dataset/test_holdout_200.jsonl \
GUARDEVAL_LLM_MODE=mock \
python -m evaluation.evaluator

Holdout Results

Metric

Result

Accuracy

98.00%

Precision

100.00%

Attack Detection / Recall

80.00%

F1 Score

88.89%

False Positive Rate

0.00%

False Negative Rate

20.00%

Specificity

100.00%

Holdout confusion matrix

True Negatives:    180
False Positives:     0
False Negatives:     4
True Positives:     16

Attack-category performance

Category

Detection

Prompt Injection

50.00%

Data Exfiltration

75.00%

Tool Abuse

100.00%

Jailbreak

100.00%

Malicious Code

75.00%
The holdout demonstrates that the deterministic semantic simulator does not perfectly generalize to unseen attack phrasing.

In particular, prompt injection and data-exfiltration wording produced false negatives even though the development benchmark achieved 100% detection.

This difference is important because it demonstrates why benchmark performance on a controlled development dataset should not be treated as equivalent to real-world security performance.

⸻Baseline Comparison

GuardEval also evaluates simpler baselines.

No Guard

A system with no security guardrail allows every request.

On the 400-sample benchmark:

Accuracy:              95.00%
Attack Detection:       0.00%
F1 Score:               0.00%
False Positive Rate:    0.00%
False Negative Rate:  100.00%

TN = 380
FP =   0
FN =  20
TP =   0

The high accuracy is caused by the 95/5 class distribution and does not indicate useful attack detection.

Rule-Only Guard

The deterministic rule guard improves attack detection but misses attacks whose wording does not match its explicit patterns.
Accuracy:              96.75%
Attack Detection:      35.00%
Precision:            100.00%
F1 Score:              51.85%
False Positive Rate:    0.00%
False Negative Rate:   65.00%

Hybrid Guard

The hybrid architecture combines deterministic rules with semantic classification.

On the controlled 400-sample development benchmark:

Accuracy:             100.00%
Attack Detection:     100.00%
Precision:            100.00%
F1 Score:             100.00%
False Positive Rate:    0.00%
False Negative Rate:    0.00%

On the unseen 200-sample holdout:
Accuracy:              98.00%
Attack Detection:      80.00%
Precision:            100.00%
F1 Score:              88.89%
False Positive Rate:    0.00%
False Negative Rate:   20.00%

The difference between these two evaluations illustrates the importance of testing on data that was not used during classifier development.

Benchmark Configuration

Current benchmark configuration:
Dataset:
dataset/test_realistic_95_5_400.jsonl

Samples:
400

Benign:
380

Attacks:
20

LLM Mode:
mock

Configured Model:
gpt-5.6-luna

The current benchmark uses the deterministic mock semantic classifier.

The configured real model is gpt-5.6-luna, but the development and holdout benchmarks reported above did not call the OpenAI API.
Mock Semantic Classifier

The current semantic component is a deterministic local simulator.

It is not an actual LLM.

The mock classifier detects broader security concepts using deterministic patterns so that the complete evaluation pipeline can be tested without requiring API credits.

This makes it useful for:

* CI
* reproducible experiments
* local development
* regression testing
* benchmark generation
* architecture testing

However, mock-mode results should not be interpreted as measurements of actual LLM security performance.

Real LLM Mode

GuardEval also supports an OpenAI-backed semantic classifier.

Set:
export GUARDEVAL_LLM_MODE=real

and provide:
export OPENAI_API_KEY="your-api-key"

The configured model is:
export OPENAI_MODEL="gpt-5.6-luna"

Then run:
GUARDEVAL_DATASET=dataset/test_realistic_95_5_400.jsonl \
GUARDEVAL_LLM_MODE=real \
python -m evaluation.evaluator

The real-LLM benchmark has not been reported in this repository because the available OpenAI API account currently has insufficient quota.

No real-LLM performance numbers are fabricated or substituted with mock results.

Evaluation Metrics

GuardEval reports:

Accuracy

Overall fraction of correctly classified requests.

Precision

Fraction of blocked requests that were actually attacks.

Attack Detection Rate / Recall

Fraction of attacks correctly blocked.

F1 Score

Harmonic mean of precision and recall.

False Positive Rate

Fraction of benign requests incorrectly blocked.

False Negative Rate

Fraction of attacks incorrectly allowed.

Specificity

Fraction of benign requests correctly allowed.

CI Quality Gate

The dashboard uses the following quality thresholds:
Minimum attack detection rate: 95%
Maximum false positive rate:    5%

The quality gate passes when:
Recall >= 95%
AND
False Positive Rate <= 5%

The holdout benchmark currently achieves:
Attack Detection: 80%
False Positive Rate: 0%


Therefore, it would not satisfy the configured 95% detection threshold.

This is intentional: the holdout exposes a generalization limitation instead of being used to tune the classifier until the threshold passes.

⸻

Streamlit Dashboard

GuardEval includes an interactive Streamlit dashboard showing:

* Benchmark configuration
* Sample counts
* Accuracy
* Attack detection rate
* Precision
* False-positive rate
* Confusion matrix
* Category performance
* Decision-method coverage
* CI quality gate

Live Dashboard

https://ishapageni-guardeval-dashboardapp-mbstvj.streamlit.app/

Run Locally
streamlit run dashboard/app.py

The dashboard will be available at:
http://localhost:8501

Evaluation

Run the standard development benchmark:
GUARDEVAL_DATASET=dataset/test_realistic_95_5_400.jsonl \
GUARDEVAL_LLM_MODE=mock \
python -m evaluation.evaluator

Run the unseen holdout:
GUARDEVAL_DATASET=dataset/test_holdout_200.jsonl \
GUARDEVAL_LLM_MODE=mock \
python -m evaluation.evaluator

The evaluator writes:
evaluation_report.json

Project Structure

guardeval/
│
├── dashboard/
│   └── app.py
│
├── dataset/
│   ├── test_extended.jsonl
│   ├── test_legacy_regex_tuned.jsonl
│   ├── test_realistic_95_5.jsonl
│   ├── test_realistic_95_5_direct.jsonl
│   ├── test_realistic_95_5_adversarial.jsonl
│   ├── test_realistic_95_5_400.jsonl
│   └── test_holdout_200.jsonl
│
├── evaluation/
│   ├── evaluator.py
│   └── baselines.py
│
├── guardrails/
│   ├── input_guard.py
│   ├── policy.py
│   ├── hybrid_guard.py
│   ├── mock_llm_guard.py
│   └── llm_guard.py
│
├── generate_realistic_95_5.py
├── generate_adversarial_95_5.py
├── generate_realistic_95_5_400.py
├── generate_holdout_200.py
│
├── evaluation_report.json
├── requirements.txt
└── README.md

Limitations

The current evaluation has several important limitations.

Controlled dataset

The benchmark is constructed rather than sampled from production traffic.

Reused benign prompts

The 400-sample development benchmark contains controlled prompt variants, meaning the 380 benign samples should not be interpreted as 380 completely independent real-world observations.

Deterministic mock semantic classifier

The current benchmark uses a local pattern-based semantic simulator rather than an actual LLM.

Holdout generalization gap

The unseen 200-sample benchmark reduced attack detection from 100% on the development benchmark to 80%.

This indicates that the current semantic simulator is sensitive to attack phrasing.

Real LLM performance is unmeasured

The real OpenAI semantic classifier is implemented, but a representative benchmark has not been reported because the API account currently has insufficient quota.

No claim of production security

These experiments demonstrate the evaluation architecture and benchmark methodology. They do not establish that GuardEval provides complete protection against real-world attacks.

⸻

Conclusion

GuardEval demonstrates a reproducible framework for evaluating layered security controls for LLM-powered agents.

The controlled development benchmark shows that combining deterministic rules with semantic classification can substantially improve attack detection compared with a rule-only guard.

The unseen holdout provides a more conservative result: the current deterministic semantic simulator achieved 80% attack detection with 0% false positives on 200 previously unseen samples.

This difference highlights the importance of:

* held-out security datasets
* false-negative analysis
* category-level evaluation
* baseline comparison
* reproducible CI benchmarks
* separating mock evaluation from real-LLM evaluation

Future work includes evaluating the framework with a real LLM, expanding the holdout dataset, adding adversarially generated examples, and testing additional semantic guard models.
