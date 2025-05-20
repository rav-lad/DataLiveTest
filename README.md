
<h1 align="center">
  <br>
  <img src="![image](https://github.com/user-attachments/assets/dedb44b1-8cba-418b-97a8-0b63f6c0e187)" width="200">
  <br>
</h1>

<h4 align="center">Your local AI assistant for interactive, multimodal data exploration</h4>

<p align="center">
  🏆 <strong>1st Place — GenAI APIs Track</strong><br>
  <em>LauzHack Mini-Hackathon 2025</em><br>
  Organized by <a href="https://www.epfl.ch/labs/">@EPFL AI Team</a> and <a href="https://www.lauzhack.com/">@LauzHack</a>
</p>

<p align="center">
  <a href="https://streamlit.io">
    <img src="https://img.shields.io/badge/Frontend-Streamlit-ff4b4b?logo=streamlit&logoColor=white">
  </a>
  <a href="https://openai.com/api/">
    <img src="https://img.shields.io/badge/API-OpenAI GPT--4o-blue?logo=openai">
  </a>
  <a href="https://huggingface.co" target="_blank">
    <img src="https://img.shields.io/badge/API-HuggingFace-yellow.svg?logo=huggingface&logoColor=white" alt="Hugging Face">
  </a>
  <a href="https://www.python.org">
    <img src="https://img.shields.io/badge/Python-3.10-blue.svg?logo=python&logoColor=white">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#features">Why It's Different from ChatGPT</a> •
  <a href="#features">Features</a> •
  <a href="#features">Tech Stack</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#future-work">Future Work</a> •
  <a href="#team">Team</a>
</p>

> 🎥 **Demo**: *Coming soon — the demo video will be added here once it's ready!*

---
---

# DataLive.ai 🧠📊

**🏆 1st Place Winner – LauzHack Mini Hackathon (GenAI Track)**
Organized by **LauzHack** and the **EPFL AI Team**

## Overview

**DataLive.ai** is a next-generation AI assistant for data exploration and visualization. It combines automated preprocessing, intelligent code generation, and multimodal reasoning — all through a sleek and interactive Streamlit app.

Upload a `.csv` file, clean your data, ask natural language questions, generate plots, and even receive AI-driven insights from those plots. All computation is performed **locally**, keeping your data private while maximizing speed.

This project was built in under 24 hours during the **LauzHack Mini Hackathon 2025**, where it won **1st place** in the **Generative AI Track**.

---

## Why It's Different from ChatGPT

Unlike general-purpose tools like ChatGPT or Code Interpreter:

* **Your data is never uploaded to the LLM**
  → We extract only essential metadata (e.g., column names, types, number of missing values) and send **that** to the model. This:

  * Preserves **data privacy**
  * Avoids **token overload** on large datasets
  * Ensures compatibility with **sensitive or proprietary files**

* **All code is executed locally**
  → No need to copy/paste code; the app renders output instantly in the interface.

* **Lightning-fast interactions** thanks to **Streamlit**
  → Near-instant feedback loop between code generation, execution, and visualization.

---

## Features

###  Automatic Data Profiling

* Data shape, summary statistics
* Missing values report
* Column data types and inferred structure

###  Smart Data Cleaning

Choose from:

* **Drop** rows with missing values
* **Fill** with column-wise **mean**
* **KNN Imputation**

###  Conversational Code Generation

* Powered by **OpenAI GPT-4o**

* Ask natural questions like:

  > "Show a pairplot of numerical features"
  > "Plot the class distribution as a bar chart"

* Returns **executable Python code**, auto-rendered as:

  * Seaborn heatmaps
  * Histograms
  * Boxplots
  * And more...

###  Multimodal Plot Analysis

* After generating a plot, ask:

  > "What can you conclude from this?"

* The image is sent to **Video-LLaMA2B** via a custom Hugging Face inference handler

* Returns **textual interpretation** of trends, outliers, and insights

###  Export & Traceability

* Save all generated code
* Export plots for reuse or reporting

---

## Tech Stack

* **Frontend**: Streamlit
* **Backend**: Python (OpenAI API + Hugging Face Inference Endpoint)
* **LLMs**:

  * GPT-4o (OpenAI) – Prompt-to-code generation
  * Video-LLaMA2B (DAMO-NLP-SG) – Plot interpretation
* **Libraries**: pandas, NumPy, Scikit-learn, Seaborn, Matplotlib
* **Execution**: Local sandboxed Python runtime (safe, fast, private)

---

## How It Works

1. Upload your `.csv` dataset
2. Receive an automatic summary of key stats
3. Select a data cleaning strategy
4. Ask a question or request a visualization
5. Get back both:

   * The **generated code**
   * The **rendered output**
6. (Optional) Ask for AI-based interpretation of the plot

---

## Getting Started

### Requirements

```bash
pip install -r requirements.txt
```

### Launch Locally

```bash
streamlit run app.py
```

### Environment Setup

You'll need:

* `OPENAI_API_KEY`
* `HUGGINGFACE_TOKEN` (for the Video-LLaMA endpoint)

---

## Future Work

Here are some exciting features planned for the next iteration:

* **SQL Data Integration**
  → Connect to relational databases (PostgreSQL, MySQL) and run natural language queries directly on live data.

* **NoSQL Support** *(MongoDB, Firebase, etc.)*
  → Enable compatibility with document-based datasets.

* **Advanced Insight Generation**
  → Incorporate models to automatically detect:

  * **Trends**
  * **Seasonality**
  * **Anomalies**
  * **Correlations and causal patterns**

* **Explainable AI Layer**
  → Provide rationale behind detected trends or statistical recommendations.

---

## Team

Built by Ylan Vifian , Youcef Amar and Arno Vifian .

---

