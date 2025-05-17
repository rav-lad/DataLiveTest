import openai
import runpy
from typing import Tuple, Optional, List, Dict
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from src.openai_caller import get_python_code_from_gpt,run_code_with_df
import pandas as pd

    
if __name__ == "__main__":

    # Step 1: Load and normalize dataset
    try:
        df = pd.read_csv("src/tests/train2tap.csv")
        df.columns = df.columns.str.lower()
    except Exception as e:
        print(f"Error loading train2tap.csv: {e}")
        exit(1)

    # Step 2: Generate metadata
    sample = df.head(3).to_csv(index=False)
    col_info = ", ".join([f"{col} ({df[col].dtype})" for col in df.columns])
    metadata = f"""
Columns: {col_info}
Rows: {len(df)}
Sample:
{sample}
All column names are lowercase.
    """.strip()

    # Step 3: Initialize empty message history (first conversation)
    messages: List[Dict[str, str]] = []

    # Step 4: First user request
    user_request = "Now group passengers by age ranges and plot the number of passengers per group."

    # Step 5: Call GPT to get the code
    generated_code, messages = get_python_code_from_gpt(metadata, user_request, messages)
    print("\nGenerated Code:\n")
    print(generated_code)

    # Step 6: Run the generated code using the actual DataFrame
    code, fig = run_code_with_df(df, metadata, user_request)

    # Step 7: Display the plot or error
    if fig:
        print("[✔] Plot generated successfully.")
        fig.show()
    else:
        print("[✘] No plot was generated.")

    # Optional: Print messages for debug
    print("\nMessage history:\n")
    for i, msg in enumerate(messages):
        print(f"{i+1}. [{msg['role'].upper()}] {msg['content'][:300]}...\n")  # Truncated for readability