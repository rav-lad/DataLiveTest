import openai
import runpy
from typing import Tuple, Optional, List, Dict
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from src.openai_caller import get_python_code_from_gpt,run_code_with_df
import pandas as pd

    
if __name__ == "__main__":
    df = pd.read_csv("src/tests/train2tap.csv")
    df.columns = df.columns.str.lower()

    # Generate metadata
    sample = df.head(3).to_csv(index=False)
    col_info = ", ".join([f"{col} ({df[col].dtype})" for col in df.columns])
    metadata = f"""
Columns: {col_info}
Rows: {len(df)}
Sample:
{sample}
All column names are lowercase.
""".strip()

    # Initialize messages
    messages: List[Dict[str, str]] = []

    # First user request
    user_request = "Group passengers by age range and plot the number per group."

    # Call GPT
    generated_code, messages = get_python_code_from_gpt(metadata, user_request, messages)
    print("\nGenerated Code:\n", generated_code)

    # Execute code
    code, fig = run_code_with_df(df, metadata, user_request)
    if fig:
        print("[✔] Plot generated successfully.")
        fig.show()
    else:
        print("[✘] No plot was generated.")

    # Print history
    print("\nMessage History:")
    for i, msg in enumerate(messages):
        print(f"{i+1}. [{msg['role'].upper()}]\n{msg['content'][:500]}...\n")