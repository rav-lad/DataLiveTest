import openai
import runpy
from typing import Tuple, Optional, Dict
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
from typing import List

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
        You are a helpful data analyst. A user uploaded a dataset.
        Here is a description of the dataset:
        Start of dataset description \n
        {metadata}
        End of dataset description \n
        The user asked: "{user_request}"

        Please write valid Python code to fulfill the user's request using pandas and matplotlib or seaborn.
        Do not include explanations. Only return the code.
        """

def get_python_code_from_gpt(metadata: str, user_request: str,messages: List[Dict[str, str]]
) -> Tuple[str, List[Dict[str, str]]]:
    # build the prompt  


    # handle first request case
    if not messages:
        # 1. Add system message
        messages.append({
            "role": "system",
            "content": (
                "You are a helpful Python coding assistant. Only return valid Python code "
                "using pandas, matplotlib, or seaborn. Do not explain your answers. "
                "Assume the DataFrame is already loaded as `df`."
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
            model= "gpt-4o-mini",
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
        print_message_history(messages)
        return clean_code,messages
    
    except Exception as e:
        print(f"Error calling OpenAI APi: {e}")
        return "#Error: Unable to generate code at this time",""
    
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