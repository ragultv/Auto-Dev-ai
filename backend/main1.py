from workflow.lang_graph_pipeline import app

initial_state = {"user_prompt": "Train a random forest on Titanic dataset"}
final_state = app.invoke(initial_state)

print(final_state)
