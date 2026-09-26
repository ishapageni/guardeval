# 🛡️ GuardEval

[![GuardEval Security CI](https://github.com/ishapageni/guardeval/actions/workflows/guardrail.yml/badge.svg)](https://github.com/ishapageni/guardeval/actions/workflows/guardrail.yml)

## Automated LLM-Agent Guardrail Evaluation Framework

GuardEval is a security evaluation framework for testing and measuring guardrails used in LLM-powered agents.

It evaluates user inputs, tool calls, and model outputs against security policies and produces quantitative metrics for guardrail performance.

## Key Features

- 🛡️ Input guardrail for detecting unsafe prompts
- 💉 Prompt-injection detection
- 🔐 Data-exfiltration detection
- ⚠️ Tool-abuse detection
- 🚨 Jailbreak detection
- 🔎 Hybrid rule-based and semantic guard architecture
- 🔧 Tool-call authorization checks
- 📤 Output security validation
- 📊 Automated security evaluation
- 📈 Confusion matrix and category-level metrics
- 📄 JSON evaluation reports
- 🚦 CI quality gates
- ⚙️ GitHub Actions security regression testing
- 🖥️ Streamlit security dashboard
- 🧪 Automated pytest test suite

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


``` Security Benchmark

GuardEval was evaluated against a 100-sample benchmark containing:

* 20 benign prompts
* 20 prompt-injection examples
* 20 data-exfiltration examples
* 20 tool-abuse examples
* 20 jailbreak examples

Results
## Evaluation Results

| Metric | Result |
|---|---:|
| Accuracy | 100% |
| Precision | 100% |
| Attack Detection Rate | 100% |
| False Positive Rate | 0% |
| False Negative Rate | 0% |

### Category Performance

| Category | Accuracy |
|---|---:|
| Benign | 100% |
| Prompt Injection | 100% |
| Data Exfiltration | 100% |
| Tool Abuse | 100% |
| Jailbreak | 100% |

### Confusion Matrix

| | Predicted Safe | Predicted Attack |
|---|---:|---:|
| **Actual Safe** | 20 | 0 |
| **Actual Attack** | 0 | 80 |

These results are benchmark-specific and should not be interpreted as 100% detection of real-world attacks.

Technologies

* Python
* Streamlit
* Pandas
* Scikit-learn
* Pytest
* JSONL
* Git / GitHub
* GitHub Actions

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
│   └── check_thresholds.py
│
├── dataset/
│   ├── test.jsonl
│   └── test_extended.jsonl
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
├── requirements.txt
└── README.md

Evaluation Pipeline

The evaluation engine measures:

* Accuracy
* Precision
* Attack detection rate / recall
* False positive rate
* False negative rate
* Confusion matrix
* Category-level performance

Evaluation reports are exported as:evaluation_report.json

Continuous Integration

Every push to main and every pull request triggers the GuardEval security pipeline.

The CI workflow:

1. Installs dependencies
2. Runs automated regression tests
3. Executes the security benchmark
4. Calculates guardrail metrics
5. Checks quality thresholds

The current CI quality gate requires:Minimum attack detection: 95%
Maximum false positive rate: 5%

A build fails if these security thresholds are not satisfied.

Dashboard

GuardEval includes a Streamlit dashboard for visualizing:

* Evaluation metrics
* Confusion matrix
* Category performance
* Security benchmark results
Run locally with:streamlit run dashboard/app.py

Then open:http://localhost:8501

Testing

Run the automated test suite:pytest -q

The tests cover:

* Safe inputs
* Prompt injection
* Tool abuse
* Sensitive tool operations
* Sensitive outputs
* Safe outputs
* End-to-end agent behavior

Limitations

The current implementation primarily evaluates deterministic guardrail logic and benchmark data.

The semantic/LLM guard component includes a deterministic mock implementation for development and testing because external LLM API usage is not required for the core evaluation pipeline.

Future evaluations should include larger datasets, unseen adversarial prompts, and real LLM-based semantic classification.

Future Work

* Larger adversarial security datasets
* Real LLM-based semantic guard evaluation
* Automated adversarial test generation
* Dockerized deployment
* Expanded agent/tool simulations
* Historical benchmark tracking
* Dashboard trend visualization
* Additional policy enforcement mechanisms

Author

Built as an AI security engineering project focused on evaluating safety mechanisms for LLM-powered agents.
