from workflow.pipeline import run_autodev_once

if __name__ == "__main__":
    prompt = "Build a random forest classifier on the Iris dataset, give some visulization ."
    result = run_autodev_once(prompt, max_retries=10, launch_ui=True)
    print(result)
