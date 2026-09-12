# 🍽️ Restaurant Review Analyzer

> **A professional local-AI Streamlit application that analyzes restaurant reviews and converts unstructured customer feedback into clear, actionable insights.**

The **Restaurant Review Analyzer** uses locally running **Ollama models** to analyze a restaurant review and return:

- 😊 **Sentiment**
- ⭐ **Estimated Rating**
- 👍 **Top Positive Points**
- 👎 **Top Negative Points**

The application is designed with a clean Streamlit interface, model selection, review history, JSON export, and validation to reduce unsupported or hallucinated information.

---

## 📸 Application Preview

### Review Analysis

![Restaurant Review Analyzer](screenshots/Screenshot%202026-09-12%20121349.png)

### Analysis & History

![Analysis Result](screenshots/Screenshot%202026-09-12%20121400.png)

---

## ✨ Features

### 🤖 Local AI with Ollama

The application communicates with an Ollama server running locally on your machine.

This allows the project to use local LLMs instead of requiring a cloud-based AI API.

### 📊 Review Analysis

Each review is analyzed for:

| Output | Description |
|---|---|
| **Sentiment** | Positive, Neutral, Negative, or Mixed |
| **Rating** | Rating from 1 to 5 |
| **Positive Points** | Specific things the reviewer liked |
| **Negative Points** | Specific things the reviewer disliked |

### 🎯 Structured JSON Output

The LLM is instructed to return a predictable JSON structure:

```json
{
    "sentiment": "Positive",
    "rating": 4,
    "top_positive_points": [
        "Food was delicious",
        "Friendly staff"
    ],
    "top_negative_points": [
        "Service was slow"
    ]
}
```

The application then validates and cleans the returned data before displaying it.

### 🛡️ Hallucination-Aware Prompting

The analysis prompt explicitly instructs the model to:

- Analyze only the supplied review.
- Avoid inventing restaurant information.
- Avoid adding unsupported facts.
- Extract positive points from the review.
- Extract negative points from the review.
- Return only JSON.
- Keep the rating within the 1–5 range.

This makes the application more reliable for review-analysis use cases, although no LLM-based system can guarantee perfect accuracy.

### 🧠 Multiple Ollama Models

The sidebar automatically checks the local Ollama server and displays installed models.

Suggested models include:

```text
llama3.2
llama3.1
mistral
gemma3
phi4
qwen2.5:3b
```

If Ollama is running and models are installed, the application allows the user to select an installed model.

### 📜 Review History

Every successfully analyzed review is stored in Streamlit session state.

The history contains:

- Review ID
- Timestamp
- Selected model
- Original review
- Analysis result

### 📥 JSON Export

Analyzed reviews can be exported as:

```text
restaurant_reviews_analysis.json
```

This makes the application useful not only for experimentation but also for collecting structured review-analysis results.

### 🎨 Professional Streamlit UI

The interface includes:

- Wide application layout
- Sidebar settings
- Review input area
- Analysis cards
- Sentiment indicators
- Rating display
- Positive/negative insight cards
- Expandable review history
- JSON download functionality
- Responsive Streamlit components

---

# 🏗️ Project Architecture

```text
                    User
                      │
                      ▼
             ┌─────────────────┐
             │ Streamlit UI    │
             │ Review Input    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Prompt Builder  │
             │ & Instructions  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Ollama Local    │
             │ LLM Server      │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ JSON Response   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Validation &    │
             │ Data Cleaning   │
             └────────┬────────┘
                      │
             ┌────────┴─────────┐
             ▼                  ▼
      ┌──────────────┐   ┌──────────────┐
      │ UI Results   │   │ Review       │
      │              │   │ History      │
      └──────────────┘   └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ JSON Export  │
                         └──────────────┘
```

---

# 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Application development |
| **Streamlit** | Web UI |
| **Ollama** | Local LLM runtime |
| **Requests** | Communication with Ollama API |
| **JSON** | Structured model output and export |

---

# 📁 Project Structure

```text
Restaurant-Review-Analyzer/
│
├── analyzer.py
├── requirements.txt
│
├── screenshots/
│   ├── Screenshot 2026-09-12 121349.png
│   └── Screenshot 2026-09-12 121400.png
│
└── prompt engineering/
    └── README.md
```

### File Description

| File / Folder | Description |
|---|---|
| `analyzer.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies |
| `screenshots/` | Application screenshots |
| `prompt engineering/` | Prompt-engineering documentation used alongside the project |

---

# ⚙️ How It Works

## 1. Enter a Restaurant Review

The user pastes a restaurant review into the Streamlit text area.

Example:

```text
The food was amazing and the staff were very friendly.
The pasta was delicious, but the service was a little slow
and the restaurant was quite crowded.
```

## 2. Select an Ollama Model

The application checks:

```text
http://localhost:11434/api/tags
```

and retrieves the locally available Ollama models.

## 3. Build the Analysis Prompt

The review is inserted into a carefully designed prompt containing:

- Role
- Task
- Rules
- Expected JSON schema
- Allowed sentiment values

## 4. Send the Request to Ollama

The application sends a request to:

```text
POST http://localhost:11434/api/generate
```

with:

```json
{
    "model": "selected-model",
    "prompt": "analysis prompt",
    "stream": false,
    "format": "json"
}
```

## 5. Validate the Response

The application checks:

- Whether Ollama returned successfully
- Whether the response contains content
- Whether the response is valid JSON
- Whether sentiment is valid
- Whether the rating is between 1 and 5
- Whether positive points are lists
- Whether negative points are lists

## 6. Display the Results

The final result is presented using separate UI sections for:

```text
Sentiment
Rating
Key Insights
Positive Points
Negative Points
Original Review
```

## 7. Store the Analysis

The result is added to Streamlit session state so it can appear in the review-history section.

## 8. Export the Results

The complete review history can be downloaded as JSON.

---

# 🛠️ Installation

## Prerequisites

Make sure the following are installed:

- Python 3.9+
- Ollama
- A compatible Ollama model
- Git (optional)

---

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Restaurant-Review-Analyzer
```

If you already downloaded the project, simply open a terminal inside the project directory.

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The project requires:

```text
streamlit>=1.36.0
requests>=2.32.0
```

---

# 🦙 Ollama Setup

## 1. Install Ollama

Install Ollama for your operating system and make sure the Ollama service is running.

## 2. Verify Ollama

Run:

```bash
ollama --version
```

Then:

```bash
ollama list
```

## 3. Download a Model

For example:

```bash
ollama pull llama3.2
```

You can also use another compatible model:

```bash
ollama pull mistral
```

or:

```bash
ollama pull gemma3
```

## 4. Verify the Model

```bash
ollama list
```

You should see the installed model in the list.

---

# ▶️ Run the Application

From the project directory:

```bash
streamlit run analyzer.py
```

Streamlit will provide a local URL, usually similar to:

```text
http://localhost:8501
```

Open the URL in your browser.

---

# 🖥️ Using the Application

### Step 1 — Start Ollama

Make sure Ollama is running.

### Step 2 — Start Streamlit

```bash
streamlit run analyzer.py
```

### Step 3 — Choose a Model

Select one of the models detected by Ollama.

### Step 4 — Enter a Review

Paste a restaurant review into the input area.

### Step 5 — Analyze

Click:

```text
🔍 Analyze Review
```

### Step 6 — Explore the Results

The application displays:

```text
😊 Sentiment
⭐ Rating
💡 Key Insights
👍 Positive Points
👎 Negative Points
💬 Original Review
```

### Step 7 — Export

If multiple reviews have been analyzed, download them using:

```text
⬇️ Download JSON
```

---

# 🧪 Example

### Input

```text
The restaurant had amazing food and the staff were very friendly.
The pasta was delicious. However, the service was slow and the
restaurant was very crowded.
```

### Possible Output

```text
Sentiment: Mixed

Rating: 4/5

Positive Points:
- Food was amazing
- Staff were very friendly
- Pasta was delicious

Negative Points:
- Service was slow
- Restaurant was crowded
```

The exact result may vary depending on the selected model.

---

# 🧠 Prompt Engineering

One of the important parts of this project is the prompt used to guide the LLM.

The application uses instructions similar to:

```text
You are a restaurant review analysis assistant.

Analyze ONLY the restaurant review provided below.

IMPORTANT RULES:
1. Do not invent information.
2. Do not add facts that are not present in the review.
3. Do not assume restaurant details that the reviewer did not mention.
4. Rating must be between 1 and 5.
5. Positive points must come directly from things the reviewer liked.
6. Negative points must come directly from things the reviewer disliked.
7. Return ONLY valid JSON.
8. Do not use Markdown.
9. Do not add explanations outside the JSON.
```

This demonstrates several prompt-engineering concepts:

- Role prompting
- Instruction prompting
- Constraint-based prompting
- Structured output prompting
- Contextual prompting
- Hallucination reduction through explicit grounding rules

---

# 🛡️ Error Handling

The application handles several common failure cases.

### Ollama Not Running

```text
❌ Ollama is not available.
```

### No Model Available

```text
❌ No Ollama model is available.
```

### Empty Review

```text
⚠️ Please enter a restaurant review first.
```

### Very Short Review

```text
⚠️ Please enter a more detailed review.
```

### Connection Error

```text
Could not connect to Ollama.
```

### Timeout

```text
The request timed out.
```

### Invalid JSON

```text
The model returned invalid JSON.
```

This helps make the application more robust during real usage.

---

# 🔐 Privacy

This project is designed around **local AI processing**.

The application sends review data to the local Ollama server:

```text
localhost:11434
```

It does not require a cloud LLM API key for the core analysis workflow.

However, privacy also depends on the environment in which the application and Ollama are running.

---

# ⚠️ Limitations

Although the application includes prompt constraints and response validation, it is important to understand that LLM output is probabilistic.

Potential limitations include:

- Sentiment classification can occasionally be incorrect.
- Inferred ratings may differ from a human's rating.
- Different models can produce different results.
- Model performance depends on the selected Ollama model.
- Review history is stored in Streamlit session state and is not a permanent database.
- The application currently analyzes one review at a time.
- There is no authentication or multi-user database layer.
- Very long reviews may increase processing time depending on the model.

---

# 🚀 Future Improvements

Possible improvements include:

- [ ] Batch review analysis
- [ ] CSV upload
- [ ] Persistent database storage
- [ ] Review analytics dashboard
- [ ] Sentiment distribution charts
- [ ] Average rating analytics
- [ ] Restaurant comparison
- [ ] Aspect-based sentiment analysis
- [ ] Keyword extraction
- [ ] Review summarization
- [ ] Download results as CSV
- [ ] PDF report generation
- [ ] Authentication
- [ ] Multi-user support
- [ ] Docker deployment
- [ ] Cloud deployment
- [ ] Model performance comparison
- [ ] Evaluation dataset for measuring model accuracy

---

# 📊 Potential Business Use Cases

This project can be extended for:

### Restaurant Owners

Identify common customer complaints and strengths.

### Restaurant Managers

Track issues related to:

- Food
- Service
- Ambience
- Pricing
- Staff
- Waiting time

### Food Delivery Platforms

Analyze large numbers of customer reviews automatically.

### Customer Experience Teams

Convert unstructured feedback into structured insights.

### Business Intelligence

Combine review sentiment with ratings and other business metrics.

---

# 🎓 Learning Outcomes

By building this project, you can practice:

- Python
- Streamlit
- REST APIs
- Ollama
- Local LLMs
- Prompt engineering
- Structured JSON generation
- Response validation
- Error handling
- Session state
- Data export
- AI application UI design
- Hallucination-aware prompting

---

# 💼 Portfolio Value

This project demonstrates more than simply calling an LLM.

It shows experience with:

```text
Python
   ↓
Streamlit
   ↓
Prompt Engineering
   ↓
Local LLM
   ↓
Ollama API
   ↓
Structured JSON
   ↓
Response Validation
   ↓
Interactive UI
   ↓
Data Export
```

That makes it a useful beginner-to-intermediate portfolio project for demonstrating **LLM application development**.

---

# 📚 Related Concepts

If you want to extend this project, the following topics are worth learning:

1. Prompt Engineering
2. Large Language Models
3. Ollama
4. RAG
5. Embeddings
6. Vector Databases
7. Structured Outputs
8. Function Calling / Tool Use
9. AI Agents
10. LLM Evaluation
11. Guardrails
12. Streamlit Deployment

---

# 🤝 Contributing

Contributions are welcome.

A simple workflow:

```bash
git checkout -b feature/new-feature
```

Make your changes, test them, and then commit:

```bash
git add .
git commit -m "Add new feature"
```

Push the branch:

```bash
git push origin feature/new-feature
```

Then open a Pull Request.

---

# 📄 License

No license has been specified for this project yet.

If you plan to publish the repository publicly, consider adding an appropriate open-source license such as MIT, Apache-2.0, or another license that matches your intended usage.

---

# ⭐ Acknowledgements

Built with:

- [Streamlit](https://streamlit.io/)
- [Ollama](https://ollama.com/)
- Python

---

# 👨‍💻 Project Summary

**Restaurant Review Analyzer** is a local AI-powered review analysis application built with **Streamlit and Ollama**.

It transforms raw restaurant reviews into structured insights while focusing on clear prompting, JSON output, response validation, local processing, and an easy-to-use interface.

> **Turn customer feedback into structured insights — privately, locally, and interactively.** 🍽️🤖

---

## ⭐ If You Like This Project

If this project helped you learn about local LLM applications, prompt engineering, or Streamlit:

- ⭐ Star the repository
- 🍴 Fork the project
- 🐛 Report issues
- 💡 Suggest improvements
- 🤝 Contribute new features
