# GuardEval
[![GuardEval Security CI](https://github.com/ishapageni/guardeval/actions/workflows/guardrail.yml/badge.svg)](https://github.com/ishapageni/guardeval/actions/workflows/guardrail.yml)

### Automated LLM-Agent Guardrail Evaluation Framework

GuardEval is a security evaluation framework for testing and measuring guardrails used in LLM-powered agents.

It evaluates user inputs, tool calls, and model outputs against security policies and provides quantitative metrics for guardrail performance.

---

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
                    |  Semantic / LLM   |
                    |       Guard       |
                    +-------------------+
                              |
                              v
                    +-------------------+
                    |   Hybrid Guard    |
                    +-------------------+
                              |
                              v
                    +-------------------+
                    |   Policy Layer   |
                    +-------------------+
                       /            \
                    Block           Agent
                                    |
                                    v
                           +----------------+
                           |   Tool Guard   |
                           +----------------+
                                    |
                                    v
                              Tool Execution
                                    |
                                    v
                           +----------------+
                           |  Output Guard  |
                           +----------------+
                                    |
                                    v
                              Final Response
