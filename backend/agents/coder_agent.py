from core.llm_client import get_llm
from langchain.prompts import ChatPromptTemplate

# Generates ONE self-contained python script with integrated Gradio UI:
# - loads dataset (Hugging Face)
# - splits train/val
# - trains model (sklearn/torch depending on task)
# - prints detailed evaluation metrics
# - saves model artifacts to project directory
# - launches Gradio interface for model interaction
_coder = ChatPromptTemplate.from_messages([
    ("system",
     "You are the Coder Agent. Generate a single, runnable Python script that:\n"
     "1) Loads the dataset using HuggingFace Datasets (from the given hf_id and target name).\n"
     "2) Preprocesses features (numeric/categorical), splits train/val.\n"
     "3) Trains a solid baseline model.sklearn is your core ( strictly no for torch ,transformers, tensorflow and keras).\n"
     "4) Prints detailed evaluation metrics (accuracy/F1/precision/recall for classification; MAE/R2/RMSE for regression).\n"
     "5) Saves trained model artifacts to {project_dir}/artifacts/.\n"
     "6) Creates a comprehensive evaluation report with visualizations (confusion matrix, needed graphs , feature importance, etc).\n"
     "7) Launches a Gradio interface for interactive model testing at the end.\n"
     "8) Use minimal dependencies (sklearn, gradio, pandas, numpy, matplotlib, seaborn).\n"
     "9) Add argparse for reproducibility (seed, max_iter, etc). Use try/except and clear logging.\n"
     "10) Print clear section headers and detailed results throughout execution.\n"
     "11) The Gradio interface should:\n"
     "    - Use the new unified component system (gr.Textbox, gr.Dataframe, gr.Label, etc.) instead of deprecated gradio.inputs/outputs.\n"
     "    - Show prediction results and model confidence.\n"
     "    - Launch with demo.launch(share=False, server_name='127.0.0.1', server_port=7860, prevent_thread_lock=True) to avoid blocking.\n"
     "    - Use demo.launch() in a try-except block and add a 3-second delay before terminating.\n"
     "    - Print the Gradio URL when launched.\n"
     "12) Save the dataset to {project_dir}/dataset/ folder for reference.\n"
     "13) IMPORTANT: Print 'EXECUTION_COMPLETE' at the very end after all processing is done.\n"
     "14) IMPORTANT: Print all metrics in the format 'METRIC_NAME: value' for easy parsing."),
    ("human",
     "Plan JSON:\n{plan_json}\n\n"
     "Dataset JSON:\n{dataset_json}\n\n"
     "Project Directory: {project_dir}\n\n"
     "Generate ONLY code in a single Python file; no explanations. "
     "Filename comment at top: # FILE: ml_pipeline.py")
])


def generate_training_code(plan_json: dict, dataset_json: dict, project_dir: str) -> str:
    llm = get_llm()
    response = (_coder | llm).invoke({
        "plan_json": plan_json, 
        "dataset_json": dataset_json,
        "project_dir": project_dir
    }).content
    print(f"Raw coder response starts with: {response[:50]}")
    
    # Clean up markdown formatting more aggressively
    import re
    
    # Remove all markdown code blocks
    code = re.sub(r'```python\s*', '', response)
    code = re.sub(r'```\s*', '', code)
    
    cleaned_code = code.strip()
    print(f"Cleaned code starts with: {cleaned_code[:50]}")
    return cleaned_code
