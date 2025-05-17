import openai
import runpy
from typing import Tuple, Optional, Dict
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
from typing import List
import seaborn as sns


client= openai.OpenAI(api_key= "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") 

FILENAME = "src/generated_script.py"

context = ""
def sanitize_code(gpt_response: str) -> str:
    """ 
    Clean GPT output to extract raw python code
    Remove markdown, fences and comment around the code
    """
    cleaned = gpt_response.strip()

    #remove markdown
    if cleaned.startswith("```"):
        parts = cleaned.split("```")
        if len(parts) >= 2:
            cleaned = parts[1] 
            #removes 'python' if it exists
            if cleaned.startswith("python"):
                cleaned = cleaned[len("python"):].strip()

    return cleaned

def write_code_to_file(code: str, filename: str = FILENAME) -> None:
    """
    overwrites the given file with sanitized python code.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"[✔] Code successfully written to {filename}")
    except Exception as e:
        print(f"[✘] Failed to write code to file: {e}")

def create_prompt(metadata: str, user_request: str) -> str:
    """
    Returns the initial prompt for the GPT model based on dataset metadata and user request.
    """
    return f"""
        You are a professional data analyst. A user uploaded a dataset.

        Here is a description of the dataset:
        Start of dataset description:
        {metadata}
        End of dataset description.

        Your task is to analyze and visualize the data according to the user request:

        "{user_request}"

        You may preprocess or transform the data if needed before plotting (e.g., grouping, aggregating, cleaning, adding new columns).

        Make sure to:
        - Use only pandas, matplotlib, or seaborn
        - Format the chart professionally (set title, axis labels, color, size, etc.)
        - Do **not** include any explanations or `plt.show()`
        - Only return the Python code
        """

def get_python_code_from_gpt(metadata: str, user_request: str,messages: List[Dict[str, str]]
) -> Tuple[str, List[Dict[str, str]]]:
    # build the prompt  
    
    system_script = """
    You are a professional Python data analyst chatbot embedded in a web interface.

    You respond with clean, valid, executable Python code using only the following libraries:
    - pandas (as `pd`)
    - matplotlib.pyplot (as `plt`)
    - seaborn (as `sns`)

    IMPORTANT:
    - The dataset is already loaded into a DataFrame named `df`
    - The libraries `pd`, `plt`, and `sns` are already imported
    - Do NOT include import statements
    - Do NOT use `df = pd.read_csv(...)`
    - Do ALWAYS include `fig` at the end
    - When plotting a correlation heatmap, use df.corr(numeric_only=True) to avoid errors from non-numeric columns. Always plot with fig, ax = plt.subplots(), draw with ax=, and return fig as the last line.
    - Preprocess the DataFrame if needed (e.g., filtering, grouping, creating new columns)
    - Visualize the data according to the user request
    - Create professional, well-labeled plots (title, axis labels, color, font sizes)
    - Use consistent styling (e.g., figsize=(10, 6), clean color palettes, rotated ticks)


    Only return valid Python code. Do not include explanations or comments.

    Example template:

    ```python
    # Data preprocessing
    df['new_col'] = ...

    # correlation for numerical feature only
    correlation_matrix = df.corr(numeric_only=True)
    
    # Aggregation
    grouped = df.groupby(...).agg(...)

    # Plotting
    fig,ax = plt.figure(figsize=(10, 6))
    sns.heatmap(x=..., y=..., data=...,ax=axe)
    plt.title("Your Title", fontsize=16)
    plt.xlabel("X Axis", fontsize=14)
    plt.ylabel("Y Axis", fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig
    ```
    """

    # handle first request case
    if not messages:
        # 1. Add system message
        messages.append({
            "role": "system",
            "content": (
                system_script
            )
        })

        #create first user message with metadata
        first_prompt = create_prompt(metadata, user_request)
        messages.append({"role": "user", "content": first_prompt})

    else:
        user_message = (f"The user asked: \"{user_request}\"\n"
            "Please write valid Python code to fulfill the user's request using pandas and matplotlib or seaborn. "
            "Do not include explanations. Only return the code that should work when runned i.e don't forget the import each time")
    
        messages.append({"role": "user", "content": user_message})

    
    # call the api 
    try: 
        response = client.chat.completions.create(
            model= "gpt-4o",
            messages = messages,
            temperature=0.2
        )

        # fetch code from gpt answer
        raw_response = response.choices[0].message.content
        clean_code = sanitize_code(raw_response)

        # append the assistant's response to the messages
        messages.append({"role": "assistant", "content": clean_code})
        
        # write the code to a file
        write_code_to_file(clean_code)
        ##print_message_history(messages)
        return clean_code,messages
    
    except Exception as e:
        print(f"Error calling OpenAI APi: {e}")
        return "#Error: Unable to generate code at this time",""
    
def run_code_with_df(df: pd.DataFrame, metadata: str, user_request: str, filename: str = FILENAME) -> Tuple[str, Optional[Figure]]:
    """
    Executes the GPT-generated script (stored in a file), injecting the user's DataFrame `df`
    and necessary libraries. Returns:
        - The generated code as a string
        - The resulting matplotlib Figure object (or None if nothing was plotted)
    """
    # Step 1: Read code
    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        print(f"[⚠️] Error reading code from {filename}: {e}")
        return "# Error: could not read generated code", None

    # Step 2: Clean up previous plots
    plt.close("all")

    # Step 3: Inject df + modules
    try:
        runpy.run_path(filename, init_globals={
            "df": df,
            "pd": pd,
            "plt": plt,
            "sns": sns
        })
    except Exception as e:
        print(f"[⚠️] Error running {filename}: {e}")
        return code, None

    # Step 4: Return most recent figure
    figs = [plt.figure(i) for i in plt.get_fignums()]
    fig = figs[-1] if figs else None
    return code, fig

def print_message_history(messages: List[Dict[str, str]]) -> None:
    """
    Nicely prints the list of chat messages with role and truncated content.
    """
    print("\n:scroll: Message History:")
    print("=" * 60)
    for i, msg in enumerate(messages):
        role = msg["role"].upper()
        content_preview = msg["content"].strip()

        # Truncate long messages for readability
        if len(content_preview) > 500:
            content_preview = content_preview[:500] + " ... [truncated]"

        print(f"\n[{i+1}] Role: {role}")
        print("-" * 60)
        print(content_preview)
    print("=" * 60 + "\n")