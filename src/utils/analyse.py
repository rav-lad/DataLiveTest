import cv2
import base64
import os
import requests
import matplotlib.pyplot as plt

def image_to_video(image_path: str, output_path: str = "chart.mp4", fps: float = 1.0, repeat: int = 5) -> str:
    """
    Converts a static image into a video with repeated frames.

    Parameters:
        image_path (str): Path to the input image
        output_path (str): Path to the output video (default: 'generated_video.mp4')
        fps (float): Frames per second for the video (default: 1.0)
        repeat (int): How many times to repeat the image as frames (default: 5)

    Returns:
        str: Path to the generated .mp4 video
    """
    # Lire l’image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image from path: {image_path}")

    height, width, _ = img.shape

    # Préparer le writer vidéo
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Répéter la frame plusieurs fois
    for _ in range(repeat):
        out.write(img)
    out.release()

    return output_path

def analyze_video_chart(output_path: str) -> str:
    """
    Sends a base64-encoded video (.mp4) representing a chart to the Hugging Face VideoLLaMA endpoint.
    The prompt is fixed: 'You are a senior data analyst...'.

    Parameters:
        output_path (str): Path to the .mp4 video file to analyze

    Returns:
        str: The generated textual analysis from the model
    """
    # Fixed Hugging Face credentials and endpoint
    ENDPOINT_URL = "https://cyiijbw03epwqjty.us-east-1.aws.endpoints.huggingface.cloud"
    HF_TOKEN = "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"
    PROMPT = """
**Role**: You are a seasoned Lead Data Analyst with 10+ years of experience.

**Task**: Perform a detailed, structured analysis of the provided chart and deliver executive-ready insights with technical recommendations.

### Analysis Framework

1. **Technical Assessment**:
   - Chart Type: Identify the visualization type and its appropriateness
   - Data Structure:
     * Distribution (skewness, kurtosis, multimodality)
     * Outliers (quantify impact)
     * Data quality (missing values, artifacts)

2. **Statistical Insights**:
   - Transformations Needed: Recommend adjustments (log/Box-Cox, standardization)
   - Key Relationships: Highlight correlations/trends with metrics (RÂ², CI)
   - Hypotheses: Generate 2-3 testable hypotheses

3. **Business Implications**:
   - Actionable Takeaways: Link to business decisions
   - Benchmarking: Compare against industry standards
   - Risks/Opportunities: Flag limitations or opportunities

4. **Next Steps**:
   - Data Adjustments: Specific fixes (imputation, filtering)
   - Advanced Analysis: Suggest models (ARIMA, SHAP)
   - Visualization Improvements: Propose alternatives

**Deliverable**: Concise bullet points for executives + technical appendix
**Tone**: Professional, data-driven, no unexplained jargon
"""

    # Read and encode the video
    with open(output_path, "rb") as f:
        video_bytes = f.read()
    video_b64 = base64.b64encode(video_bytes).decode("utf-8")

    # Prepare payload
    payload = {
        "inputs": {
            "video": video_b64,
            "prompt": PROMPT
        }
    }

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    # Send request
    response = requests.post(ENDPOINT_URL, headers=headers, json=payload)
    print(f"Status code: {response.status_code}")

    try:
        return response.json().get("response", "No response field found.")
    except Exception:
        return response.text

def analyse_plot(fig): 
    # Save to file
    PATH = "src/temp/dummy_plot.png"  # or e.g. "/tmp/myplot.png"
    OUTPATH = "src/temp/test.mp4"
    fig.savefig(PATH, format="png", dpi=100, bbox_inches='tight')


    print(f"Plot saved to: {PATH}")

    _ = image_to_video(PATH,OUTPATH)
    analysis = analyze_video_chart(OUTPATH)
    print(f"{analysis}")
    return analysis

if __name__ == "__main__":
    # Create a dummy plot
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot([1, 2, 3, 4], [10, 5, 8, 12], marker='o')
    ax.set_title("Dummy Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")

    # Save to file
    PATH = "dummy_plot.png"  # or e.g. "/tmp/myplot.png"
    OUTPATH = "test.mp4"
    fig.savefig(PATH, format="png", dpi=100, bbox_inches='tight')


    print(f"Plot saved to: {PATH}")

    _ = image_to_video(PATH,OUTPATH)
    analysis = analyze_video_chart(OUTPATH)
    print(f"{analysis}")