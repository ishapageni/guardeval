# 🛡️ GuardEval

[![GuardEval Security CI](https://github.com/ishapageni/guardeval/actions/workflows/guardrail.yml/badge.svg)](https://github.com/ishapageni/guardeval/actions/workflows/guardrail.yml)

## Automated LLM-Agent Guardrail Evaluation Framework

GuardEval is a security evaluation framework for testing and measuring guardrails used in LLM-powered agents.

It evaluates user inputs, tool calls, and model outputs against security policies and produces quantitative metrics for guardrail performance.

## Key Features

- Input guardrail for detecting unsafe prompts
- Prompt-injection detection
- Data-exfiltration detection
- Tool-abuse detection
- Jailbreak detection
- Malicious-code detection
- Hybrid rule-based and semantic guard architecture
- Tool-call authorization checks
- Output security validation
- Automated security evaluation
- Confusion matrix and category-level metrics
- JSON evaluation reports
- CI quality gates
- GitHub Actions security regression testing
- Streamlit security dashboard
- Automated pytest test suite

## Architecture

```text
                         User Prompt
                              |
                              v
                    +-------------------+
                    |   Input Guard     |
                    +-------------------+
                              |
                              v
                    +-------------------+
                    | Semantic / LLM    |
                    |      Guard        |
                    +-------------------+
                              |
                              v
                    +-------------------+
                    |   Hybrid Guard    |
                    +-------------------+
                              |
                              v
                    +-------------------+
                    |   Policy Layer    |
                    +-------------------+
                       /             \
                    Block             |
                                      v
                              +---------------+
                              |   Tool Guard  |
                              +---------------+
                                      |
                                      v
                                Tool Execution
                                      |
                                      v
                              +---------------+
                              | Output Guard  |
                              +---------------+
                                      |
                                      v
                               Final Response


Security Benchmark

GuardEval includes a controlled 400-sample security benchmark containing:

* 380 benign prompts
* 20 attack prompts
* 95% benign / 5% attack distribution
* 4 examples each of:
    * Prompt injection
    * Data exfiltration
    * Tool abuse
    * Jailbreak
    * Malicious code

The benchmark uses controlled prompt variants to evaluate the guard architecture across multiple security categories.

The benchmark dataset is generated reproducibly using:
generate_realistic_95_5_400.py

The benign portion includes controlled prompt cycles, so the 400 samples should not be interpreted as 400 completely independent real-world observations.

Baseline Comparison

The benchmark compares three configurations:

1. No Guard — no security filtering
2. Rule Only — deterministic input rules
3. Hybrid — rule guard + semantic guard + policy layer

Method

Accuracy

Attack Detection

F1

False Positive Rate

False Negative Rate

No Guard

95.00%

0.00%

0.00%

0.00%

100.00%

Rule Only

96.75%

35.00%

51.85%

0.00%

65.00%

Hybrid

100.00%

100.00%

100.00%

0.00%

0.00%

Hybrid Confusion Matrix
Actual

Predicted Safe

Predicted Attack

Actual Safe

380

0

Actual Attack

0

20

Category Performance

Category

Samples

Accuracy

General Knowledge

50

100%

Programming

50

100%

Math / Science

50

100%

Writing

50

100%

Productivity

50

100%

Data Analysis

50

100%

System Administration

50

100%

Security Education

30

100%

Prompt Injection

4

100%

Data Exfiltration

4

100%

Tool Abuse

4

100%

Jailbreak

4

100%

Malicious Code

4

100%

These results are specific to the controlled benchmark and should not be interpreted as 100% detection of real-world attacks.

Benchmark Configuration

The current benchmark was executed with:

Dataset:      test_realistic_95_5_400.jsonl
Samples:      400
Benign:       380
Attacks:       20
LLM Mode:     mock

The semantic component used for this benchmark is a deterministic mock semantic-risk simulator. It is not an actual LLM.

The configured real model is:
gpt-5.6-luna

but the reported 400-sample benchmark did not call the OpenAI API.

A real-LLM benchmark has therefore not been reported. This avoids presenting simulated results as measurements of actual LLM performance.

Evaluation Pipeline

The evaluation engine measures:

* Accuracy
* Precision
* Attack detection rate / recall
* F1 score
* False positive rate
* False negative rate
* Specificity
* Confusion matrix
* Category-level performance
* Decision-method coverage

Evaluation reports are exported as:
evaluation_report.json

Run the 400-sample evaluation with:
 bash :GUARDEVAL_DATASET=dataset/test_realistic_95_5_400.jsonl \
GUARDEVAL_LLM_MODE=mock \
python -m evaluation.evaluator

Continuous Integration

Every push to main and every pull request triggers the GuardEval security pipeline.

The CI workflow:

1. Installs dependencies
2. Runs automated regression tests
3. Executes the security benchmark
4. Calculates guardrail metrics
5. Checks quality thresholds

The current CI quality gate requires:
Minimum attack detection: 95%
Maximum false positive rate: 5%

A build fails if these security thresholds are not satisfied.

Dashboard

GuardEval includes a Streamlit dashboard for visualizing:

* Evaluation metrics
* Benchmark configuration
* Confusion matrix
* Category performance
* Decision-method coverage
* CI quality gate
* Security benchmark results

Live Dashboard

⁠Open the GuardEval Security Dashboard

Run Locally
streamlit run dashboard/app.py

Then open:
http://localhost:8501

The dashboard explicitly identifies whether the evaluation uses the mock semantic classifier or the real semantic classifier.

Testing

Run the automated test suite:
pytest -q

The tests cover:

* Safe inputs
* Prompt injection
* Tool abuse
* Sensitive tool operations
* Sensitive outputs
* Safe outputs
* End-to-end agent behavior

Limitations

The current implementation primarily evaluates deterministic guardrail logic and controlled benchmark data.

The semantic/LLM guard component includes a deterministic mock implementation for development, testing, and benchmark execution without API credits.

The current 400-sample benchmark is controlled rather than a statistically representative collection of real-world traffic. The benign examples include repeated controlled prompt variants.

The reported 100% hybrid result therefore describes performance on this benchmark only.

Real LLM-based semantic classification has not been quantitatively benchmarked because external API quota was unavailable during the current evaluation.

Future Work

* Larger independent adversarial security datasets
* Unseen adversarial prompts
* Real LLM-based semantic guard evaluation
* Automated adversarial test generation
* Dockerized deployment
* Expanded agent/tool simulations
* Historical benchmark tracking
* Dashboard trend visualization
* Additional policy enforcement mechanisms
* Cross-model semantic guard comparison

Technologies

* Python
* Streamlit
* Pandas
* Scikit-learn
* Pytest
* JSONL
* Git / GitHub
* GitHub Actions
* OpenAI API integration

Project Structure

guardeval/
├── guardrails/
│   ├── input_guard.py
│   ├── llm_guard.py
│   ├── mock_llm_guard.py
│   ├── hybrid_guard.py
│   ├── tool_guard.py
│   ├── output_guard.py
│   ├── policy.py
│   └── agent_pipeline.py
│
├── evaluation/
│   ├── evaluator.py
│   ├── baselines.py
│   └── check_thresholds.py
│
├── dataset/
│   ├── test.jsonl
│   ├── test_extended.jsonl
│   ├── test_legacy_regex_tuned.jsonl
│   ├── test_realistic_95_5.jsonl
│   ├── test_realistic_95_5_direct.jsonl
│   ├── test_realistic_95_5_adversarial.jsonl
│   └── test_realistic_95_5_400.jsonl
│
├── dashboard/
│   ├── app.py
│   └── __init__.py
│
├── tests/
│   └── test_guardrail.py
│
├── .github/
│   └── workflows/
│       └── guardrail.yml
│
├── generate_realistic_95_5.py
├── generate_adversarial_95_5.py
├── generate_realistic_95_5_400.py
├── evaluation_report.json
├── requirements.txt
└── README.md

Author

Built as an AI security engineering project focused on evaluating safety mechanisms for LLM-powered agents.
