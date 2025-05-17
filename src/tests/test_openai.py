import openai
import runpy
from typing import Tuple, Optional, List
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd

FILENAME = "test_generated_code.py"

client= openai.OpenAI(api_key= "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") 



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

def get_starting_prompt(metadata: str, user_request: str) -> str:
    """
    Returns the initial prompt for the GPT model based on dataset metadata and user request.
    """
    return f"""
        You are a helpful data analyst. A user uploaded a dataset.
        Here is a description of the dataset:
        {metadata}

        The user asked: "{user_request}"

        Please write valid Python code to fulfill the user's request using pandas and matplotlib or seaborn.
        Do not include explanations. Only return the code.
        """



def get_python_code_from_gpt(metadata: str, user_request: str, context: List[str]) -> str:
    # build the prompt  

    messages = [
        {"role": "system", "content": "You are a helpful Python coding assistant. Only return executable code using pandas, matplotlib, or seaborn. Assume the DataFrame is called df."}
    ]

    if not context:
        starting_prompt= get_starting_prompt(metadata, user_request)
        messages.append({"role": "user", "content": starting_prompt})
    else:
        for msg in context:
            messages.append({"role": "user", "content": msg})
        messages.append({"role": "user", "content": user_request})
    
    # call the api 
    try: 
        response = client.chat.completions.create(
            model= "gpt-4o-mini",
            messages =messages,
            temperature=0.2
        )

        # fetch code from gpt answer
        raw_response = response.choices[0].message.content
        clean_code = sanitize_code(raw_response)
        write_code_to_file(clean_code)

        return clean_code
    
    except Exception as e:
        print(f"Error calling OpenAI APi: {e}")
        return "#Error: Unable to generate code at this time"
    
def run_code_with_df(df: pd.DataFrame, metadata: str, user_request: str, filename: str =FILENAME) -> Tuple[str, Optional[Figure]]:
    """
    Executes the GPT-generated script (stored in a file), injecting the user's DataFrame `df`.
    Returns:
        - The generated code as a string
        - The resulting matplotlib Figure object (or None if nothing was plotted)
    """

    # Step 1: Read the Python code from file (for display/logging)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        print(f"[⚠️] Error reading code from {filename}: {e}")
        return "# Error: could not read generated code", None

    # Step 2: Prepare clean matplotlib state before running new code
    plt.close("all")

    # Step 3: Run the script with `df` injected
    try:
        runpy.run_path(filename, init_globals={"df": df})
    except Exception as e:
        print(f"[⚠️] Error running {filename}: {e}")
        return code, None

    # Step 4: Return the last figure (if one was created)
    figs = [plt.figure(i) for i in plt.get_fignums()]
    fig = figs[-1] if figs else None
    return code, fig   
    
if __name__ == "__main__":
    
    # Step 1: Load and normalize dataset
    try:
        df = pd.read_csv("train.csv")
        df.columns = df.columns.str.lower()  # normalize to lowercase
    except Exception as e:
        print(f"Error loading train.csv: {e}")
        exit(1)

    # Step 2: Generate metadata from real DataFrame
    sample = df.head(3).to_csv(index=False)
    col_info = ", ".join([f"{col} ({df[col].dtype})" for col in df.columns])
    metadata = f"""
Columns: {col_info}
Rows: {len(df)}
Sample:
{sample}
All column names are lowercase.
    """

    # Step 3: Create full starting prompt (acts as first user context message)
    user_request = "Plot the age distribution"
    starting_prompt = get_starting_prompt(metadata, user_request)

    # Step 4: Build context with prior instructions (color and title preferences)
    context = [
        starting_prompt,  # Full context: metadata + initial task
        "Please use red color for all plots.",
        "Use 'Passenger Age Group Distribution' as the title of all future plots."
    ]

    # Step 5: New follow-up request (should reuse styling from context)
    user_request = "Now group passengers by age ranges and plot the number of passengers per group."

    # Step 6: Generate code from GPT
    generated_code = get_python_code_from_gpt(metadata, user_request, context)
    print("Generated Code:\n")
    print(generated_code)

    # Step 7: Run the generated code with the real DataFrame
    code, fig = run_code_with_df(df, metadata, user_request)
    if fig:
        print("[✔] Plot generated successfully.")
        fig.show()
    else:
        print("[✘] No plot was generated.")
