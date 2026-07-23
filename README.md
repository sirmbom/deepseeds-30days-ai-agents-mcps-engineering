# DEEPSEED 30-Day AI Mastery Challenge

## AI Agents & MCPs Engineering Track

My proof of work for the Deepseeds(SEED - @iwstech3) 30 Days challenge focused on AI Agents & MCPs Engineering.

---

### Challenge Guidelines

> [!NOTE]
> **Build in Public:** Every day of work goes to GitHub. Not just the successes — the failures, the half-working scripts, the confused `learnings.md` entries.
>
> **Sunday Presentations:** Presenting forces clarity of understanding. Every Sunday presentation should have a live demo (not slides), an honest account of what didn't work, and at least one question for the community.
>
> **Contribute to what you consume:** Spend at least 30 minutes on an open-source project in your field.
>
> **Teach as you learn:** Write a short post in your `learnings.md` every day.

---

### 30-Day Progress Table

|  Day   | Topic     | Status     |                        Key Output / Links                         |
| :----: | :------------------------------------------------------------------------------------------------------ | :--------- | :---------------------------------------------------------------: |
| **01** | Started Reading ReAct paper | ✅ Done | [Learnings](week1/day01/learnings.md) • [Code](week1/day01/code/) |
| **02** | Devised and Wrote boilerplate tools and functions for agents | ✅ Done | [Learnings](week1/day02/learnings.md) • [Code](week1/day02/code/) |
| **03** | Explored the foundation of the OpenAI Agents SDK and built an agent-driven customer support terminal | ✅ Done | [Learnings](week1/day03/learnings.md) • [Code](week1/day03/code/) |
| **04** | A dive into nodes and graphs in Langgraph, built a research agent | ✅ Done | [Learnings](week1/day04/learnings.md) • [Code](week1/day04/code/) |
| **05** | Built an mcp server that exposes Windows PC user Filesystem to LLM/Agent | ✅ Done | [Learnings](week1/day05/learnings.md) • [Code](week1/day05/code/) |
| **06** | Built an episodic memory vector database for agents | ✅ Done | [Learnings](week1/day06/learnings.md) • [Code](week1/day06/code/) |
| **07** | Week One Gathering and Presentations | ✅ Done |[Learnings](week1/day07/learnings.md) • _No code today_ |
| **08** | Built a Content Creation and Research agent workflow using CrewAI | ✅ Done | [Learnings](week2/day08/learnings.md) • [Code](week2/day08/code/) |
| **09** | Built a _coder and critic_ agent system using [AG2](https://github.com/ag2ai/ag2.git). | ✅ Done | [Learnings](week2/day09/learnings.md) • [Code](week2/day09/code/) |
| **10** | Apply Checkpointing, Time Travel and Human-In-The-Loop interruption for Langraph Agents  | �~\~E Done | [Learnings](week2/day10/learnings.md) • [Code](week2/day10/code/) |
| **11** | Study Agent Planning Strategies and implement the Plan-and-Execute strategy for a complex research task | ✅ Done | [Learnings](week2/day11/learnings.md) • [Code](week2/day11/code/) |
| **12** | Build and Implement an MCP server to handle complex tasks | ✅ Done | [Learnings](week2/day12/learnings.md) • [Code](week2/day12/code/) |
| **13** | Study and Implement Safety measures and fallbacks, and Guardrails for agents. | ✅ Done | [Learnings](week2/day13/learnings.md) • [Code](week2/day13/code/) |
| **14** | Week Two Gathering and Presentations | ✅ Done | [Learnings](week2/day14/learnings.md) • _No code today ;)_ |
| **15** | Study and Build with the Google ADK and compare to other Agent Development Frameworks. | ✅ Done | [Learnings](week3/day15/learnings.md) • [Code](week3/day15/code/) |
| **16** | Study the Vercel AI SDK and use it to render components for agents. | ✅ Done | [Learnings](week3/day16/learnings.md) • [Code](week3/day16/code/) |
| **17** | Study task completion rate, tool call accuracy, number of steps to completion, and cost per task in regards to Agent Evaluation. | ⏳ Pending | [Learnings](week3/day17/learnings.md) • [Code](week3/day17/code/) |
| **18** | --- | ⏳ Pending | [Learnings](week3/day18/learnings.md) • [Code](week3/day18/code/) |
| **19** | --- | ⏳ Pending | [Learnings](week3/day19/learnings.md) • [Code](week3/day19/code/) |
| **20** | --- | ⏳ Pending | [Learnings](week3/day20/learnings.md) • [Code](week3/day20/code/) |
| **21** | --- | ⏳ Pending | [Learnings](week3/day21/learnings.md) • [Code](week3/day21/code/) |
| **22** | --- | ⏳ Pending | [Learnings](week4/day22/learnings.md) • [Code](week4/day22/code/) |
| **23** | --- | ⏳ Pending | [Learnings](week4/day23/learnings.md) • [Code](week4/day23/code/) |
| **24** | --- | ⏳ Pending | [Learnings](week4/day24/learnings.md) • [Code](week4/day24/code/) |
| **25** | --- | ⏳ Pending | [Learnings](week4/day25/learnings.md) • [Code](week4/day25/code/) |
| **26** | --- | ⏳ Pending | [Learnings](week4/day26/learnings.md) • [Code](week4/day26/code/) |
| **27** | --- | ⏳ Pending | [Learnings](week4/day27/learnings.md) • [Code](week4/day27/code/) |
| **28** | --- | ⏳ Pending | [Learnings](week4/day28/learnings.md) • [Code](week4/day28/code/) |
| **29** | --- | ⏳ Pending | [Learnings](week4/day29/learnings.md) • [Code](week4/day29/code/) |
| **30** | --- | ⏳ Pending | [Learnings](week4/day30/learnings.md) • [Code](week4/day30/code/) |

---

## Project Structure

The current workspace layout is:

```text
.
|-- README.md
|-- config.py
|-- requirements.txt
|-- resources.md
|-- presentation-slides/
|-- week1/
|   |-- README.md
|   |-- day01/
|   |   |-- learnings.md
|   |   `-- code/
|   |-- day02/
|   |   |-- learnings.md
|   |   `-- code/
|   |       |-- goodfile.txt
|   |       `-- toolkit.py
|   |-- day03/
|   |   |-- learnings.md
|   |   `-- code/
|   |       |-- agent+runner_skeleton.py
|   |       `-- main.py
|   |-- day04/
|   |   |-- learnings.md
|   |   `-- code/
|   |       `-- main.py
|   |-- day05/
|   |   |-- learnings.md
|   |   `-- code/
|   |       |-- helloworld.py
|   |       `-- main.py
|   |-- day06/
|   |   |-- learnings.md
|   |   `-- code/
|   |       |-- helloworld.py
|   |       `-- main.py
|   |-- day07/
|       |-- learnings.md
|       `-- code/
|-- week2/
|   |-- README.md
|   |-- day08/
|   |   |-- learnings.md
|   |   `-- code/
|   |       `-- helloworld.py
|   |-- day09/
|   |   |-- learnings.md
|   |   `-- code/
|   |       `-- helloworld.py
|   |-- day10/
|   |   |-- learnings.md
|   |   `-- code/
|   |       `-- helloworld.py
|   |-- day11/
|   |   |-- learnings.md
|   |   `-- code/
|   |       |-- helloworld.py
|   |       |-- helloworld2.py
|   |       `-- main.py
|   |-- day12/
|   |   |-- learnings.md
|   |   `-- code/
|   |       |-- database_mcp.py
|   |       |-- main.py
|   |       |-- sandbox_env.py
|   |       `-- web-search.py
|   |-- day13/
|   |   |-- learnings.md
|   |   `-- code/
|   |       `-- helloworld.py
|   |-- day14/
|       |-- learnings.md
|       `-- code/
|-- week3/
|   |-- README.md
|   |-- day15/
|   |   |-- learnings.md
|   |   `-- code/
|   |       |-- adk_help_agent/
|   |       |   |-- __init__.py
|   |       |   `-- agent.py
|   |       |-- helloworld-growth_rate_agent/
|   |       |   |-- __init__.py
|   |       |   `-- agent.py
|   |       |-- main-writer_agent/
|   |           |-- __init__.py
|   |           `-- agent.py
|   |-- day16/
|   |   |-- learnings.md
|   |   `-- code/
|   |       `-- helloworld.py
|   |-- day17/
|   |   |-- learnings.md
|   |   `-- code/
|   |-- day18/
|   |   |-- learnings.md
|   |   `-- code/
|   |-- day19/
|   |   |-- learnings.md
|   |   `-- code/
|   |-- day20/
|   |   |-- learnings.md
|   |   `-- code/
|   |-- day21/
|       |-- learnings.md
|       `-- code/
|-- week4/
|   |-- README.md
|   |-- capstone/
|   |-- day22/
|   |   |-- learnings.md
|   |   `-- code/
|   |-- day23/
|   |   |-- learnings.md
|   |   `-- code/
|   |-- day24/
|   |   |-- learnings.md
|   |   `-- code/
|   |-- day25/
|   |   |-- learnings.md
|   |   `-- code/
|   |-- day26/
|   |   |-- learnings.md
|   |   `-- code/
|   |-- day27/
|   |   |-- learnings.md
|   |   `-- code/
|   `-- day28/
|       |-- learnings.md
|       `-- code/
```
