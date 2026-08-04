### This is Day 17.

> Task of the Day: Study task completion rate, tool call accuracy, number of steps to completion, and cost per task in regards to Agent Evaluation.

When it comes to agent or LLM operations, the response and how it got to the response are both key. Agent evaluation studies the path to the response because an agent not only needs to be coorect but also be efficient at doing it. Thus, we have 4 metrics for evaluating this efficiency which are **Task Completion Rate**, **Tool Call Accuracy**, **Number of Steps Taken** and **Cost Per Task**,

* **Task Completion Rate(TCR)**: This is the percentage of the tasks that have terminated without an unhandled exceptions or hallucinations and completed their original request. It is derived using automated assertions or LLM-as-a-judge. It is calculated as:
  `TCR = (Completed Tasks/All Tasks) x 100%`

* **Tool Call Accuracy(TCA)**: This finds out if the agent called the correct tools for the task and passed the valid arguments to those tools. It is evaluated using the provided benchmarks as source for ground truth.

* **Number of Steps Taken(NST)**: The comparison of the optimal steps it would have took to complete a task to the actual steps taken by the agent.

* **Cost Per Task(CPT)**: This takes into account the input prompt tokens, output completion tokens and the model's pricing to evaluate the cost of responses and task executions. Other metrics like Tool call accuracy and Number of steps taken also influence this metric. This is done to know if the agent will be cost efficient at scale.

I used Langchain and gemini models along with creating 20 benchmarks in a dictionary for today's task.

---

#### Drawbacks

- I couln't implement the code.
- Some of the formulas are tough to remeber.
- I used Langchain instead of recommended AgentEvals.

---

This was Day 17. Unto the next. Godspeed!