# Marketing Info Product Launch Crew (marketing112)

This project utilizes the CrewAI framework to automate the generation of a comprehensive marketing launch plan for an information product, primarily targeting a Portuguese-speaking audience. It takes unstructured text input describing the product, goals, and audience, and uses a team of AI agents powered by Google Gemini to produce strategic documents and marketing content.

## Features

*   **Unstructured Input Processing:** Reads raw text describing the project from `src/marketing112/inputs.txt`.
*   **Knowledge Extraction:** Structures the input text into a usable format (`FullProjectContext`).
*   **Market & Competitor Analysis:** Conducts research using web search tools.
*   **Strategy Development:** Defines a launch strategy (`LaunchStrategy`), including goals, audience summary, USP, offer stack, phasing, messaging, channels, and KPIs.
*   **Content Creation:** Generates various marketing assets in Portuguese:
    *   Launch Hooks/Angles (`LaunchHookList`)
    *   Lead Magnet Brief (`LeadMagnetBrief`)
    *   Opt-in Page Copy (`PageCopy`)
    *   Sales Page Copy (Draft saved to `.md`)
    *   Email Sequences (Pre-launch & Sales) (`EmailSequence`)
    *   Social Media Post Plan (`SocialMediaPlan`)
*   **Content Review:** Simulates a review process, providing feedback.
*   **Final Report Compilation:** Consolidates all generated materials into a final launch plan document.
*   **Powered by Gemini:** Explicitly configured to use Google's Gemini model via `langchain-google-genai`.

## Project Structure

```
marketing112/
├── .env                  # Environment variables (API keys) - **DO NOT COMMIT**
├── .gitignore            # Specifies intentionally untracked files by Git
├── config/               # CrewAI agent and task configurations
│   ├── agents.yaml
│   └── tasks.yaml
├── knowledge/            # Potentially deprecated input directory
├── src/
│   └── marketing112/
│       ├── __init__.py
│       ├── main.py         # Main entry point (run, train)
│       ├── crew.py         # Crew definition, agents, tasks, LLM setup
│       ├── utils/
│       │   ├── __init__.py
│       │   └── util.py     # Utility classes (e.g., TextFileReader)
│       ├── inputs.txt      # <<< INPUT FILE for unstructured text description
│       ├── crewV1.py       # Older crew version (not used)
│       └── mainV1.py       # Older main version (not used)
├── tests/                # Placeholder for tests
├── pyproject.toml        # Project metadata and dependencies (for uv/pip)
├── uv.lock               # Lock file for uv dependencies
└── README.md             # This file

# --- Generated Output Files (in project root) ---
# market_research_report_pt.md
# competitor_analysis_report_pt.md
# sales_page_copy_draft_pt.md
# creative_review_feedback.md
# final_info_product_launch_plan_pt.md
# (Plus potentially JSON outputs if tasks are configured differently)
```

## Setup

1.  **Prerequisites:**
    *   Python 3.9+
    *   `uv` (recommended for managing dependencies): `pip install uv` or follow official installation instructions.
    *   Git

2.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd marketing112
    ```

3.  **Install Dependencies:**
    Using `uv`:
    ```bash
    uv sync
    ```
    Alternatively, if you prefer pip and have a `requirements.txt` generated from `pyproject.toml`:
    ```bash
    pip install -r requirements.txt
    ```
    Or install directly from `pyproject.toml` (might require build tools):
    ```bash
    pip install .
    ```

4.  **Configure Environment Variables:**
    *   Create a `.env` file in the project root directory.
    *   Add the following required variables:
        ```dotenv
        GEMINI_API_KEY="your_google_gemini_api_key"
        SERPER_API_KEY="your_serperdev_api_key"
        ```
    *   Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   Obtain a Serper API key from [Serper.dev](https://serper.dev/) for the search tool.

## Usage

1.  **Prepare Input:**
    *   Edit the `src/marketing112/inputs.txt` file.
    *   Paste the unstructured text describing your information product, target audience, marketing goals, existing assets, brand voice, etc. Write this description in Portuguese, as the agents are primarily configured for it.

2.  **Run the Crew:**
    The standard way to run a CrewAI project:
    ```bash
    crewai run src.marketing112
    ```
    Alternatively, you can run the main script directly:
    ```bash
    python src/marketing112/main.py
    ```

3.  **Check Outputs:**
    *   Monitor the console for agent activity and logs (`verbose=True` is set).
    *   Check the project root directory for the generated Markdown files (listed in the Project Structure section).

4.  **Training (Experimental):**
    *   The `train()` function in `main.py` exists but uses outdated structured inputs.
    *   To run it (for demonstration purposes only): `python src/marketing112/main.py train <number_of_iterations>`
    *   **Note:** This training function needs significant adaptation to work effectively with the current unstructured `knowledge_base_text` input format.

## Configuration

*   **LLM:** Google Gemini (`gemini-pro`) is explicitly configured in `src/marketing112/crew.py`.
*   **Agents & Tasks:** The specific roles, goals, tools, and instructions for each AI agent and task are defined in `config/agents.yaml` and `config/tasks.yaml`. You can modify these files to customize the crew's behavior.
*   **Tools:** The crew utilizes `SerperDevTool` for web searches and `ScrapeWebsiteTool` for accessing website content. Ensure API keys are set correctly.
