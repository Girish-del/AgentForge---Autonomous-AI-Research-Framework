My project is like a smart robot scientist factory.

You tell it:

“Hey, make my AI better at this job.”

And then your app does this, step by step, like a little team of helpers:

Helper 1 (Planner): “What is the goal? What should we do first?”
Helper 2 (Data): “Let’s collect examples and practice material.”
Helper 3 (Model Picker): “Which brain should we use for this kind of problem?”
Helper 4 (Trainer): “Let’s train the brain.”
Helper 5 (Tester): “How good is it now? Did it improve?”
Helper 6 (Detective): “Where did it fail?”
Helper 7 (Fixer): “Okay, let’s fix that and try again.”
Then it repeats this loop until:

it gets good enough, or
it runs out of budget/time/tries.
Super simple picture
Your app is basically:

Frontend (React UI)
This is the screen you click.
You type a goal and press run.

Backend (FastAPI server)
This is the manager that receives your request and starts the AI workflow.

Agent loop (the brain team)
This is the repeating improvement cycle: collect → train → test → fix → repeat.

MCP tools (toolbox)
These are small tool files each helper uses (fetch data, evaluate metrics, swap model, etc.).

Observability + report (storybook)
It saves traces/logs and gives you a final summary report of what happened.

What your code does now
Runs an autonomous research loop.
Chooses model types based on task kind.
Simulates data collection / training / evaluation workflow.
Finds failure patterns and proposes improvements.
Tracks each iteration with traces and checkpoints.
Returns a final response with:
best score
why it stopped
report
history of each step
So in kid words:
It’s a machine that tries, learns, fixes itself, and tries again.

One-liner
Your app is an AI coach for AI models: it trains them, checks mistakes, and keeps helping them improve automatically.