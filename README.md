# Marketing Info Product Launch Crew (marketing112)

This project utilizes the CrewAI framework to automate the generation of a comprehensive marketing launch plan for an information product, primarily targeting a Portuguese-speaking audience. It takes unstructured text input describing the product, goals, and audience, and uses a team of AI agents powered by Google Gemini to produce strategic documents and marketing content.

## Features

*   **Unstructured Input Processing:** Reads raw text from `src/marketing112/inputs.txt` to kickstart the crew's workflow.
*   **Knowledge Extraction:**
    *   **Agent:** `input_text_analyzer`
    *   **Task:** `extract_and_structure_knowledge_task`
    *   **Role:** Extracts key information from unstructured text and structures it into the `FullProjectContext` model.
*   **Market & Competitor Analysis:**
    *   **Agent:** `lead_market_analyst`
    *   **Task:** `project_competitors_task`
    *   **Role:** Identifies and analyzes competitors, focusing on Instagram presence and broader market context.
*   **Strategy Development:**
    *   **Agent:** `chief_marketing_strategist`
    *   **Task:** `marketing_strategy_task`
    *   **Role:** Develops a comprehensive launch strategy, including phases, messaging, and KPIs.
*   **Content Creation:**
    *   **Agent:** `creative_content_creator`
    *   **Tasks:**
        *   `launch_angle_and_hook_task` - Develops creative angles for the launch.
        *   `create_lead_magnet_brief_task` - Defines the concept for a lead magnet.
        *   `write_optin_page_copy_task` - Crafts compelling opt-in page copy.
        *   `write_sales_page_copy_task` - Drafts long-form sales page copy.
    *   **Role:** Produces engaging content and copy in Portuguese for various marketing assets.
*   **Email Marketing:**
    *   **Agent:** `email_marketing_specialist`
    *   **Tasks:**
        *   `write_email_sequence_task_PRELAUNCH` - Creates pre-launch email sequences.
        *   `write_email_sequence_task_SALES` - Develops sales phase email sequences.
    *   **Role:** Designs and writes email sequences to nurture leads and drive sales.
*   **Social Media Management:**
    *   **Agent:** `social_media_manager`
    *   **Task:** `write_social_media_launch_posts_task`
    *   **Role:** Plans and drafts social media posts to build community and drive engagement.
*   **Content Review:**
    *   **Agent:** `chief_creative_director`
    *   **Task:** `review_launch_content_task`
    *   **Role:** Ensures all content aligns with brand voice and strategic goals.
*   **Final Report Compilation:**
    *   **Agent:** `final_report_synthesizer`
    *   **Task:** `compile_final_report_task`
    *   **Role:** Synthesizes all outputs into a comprehensive launch plan document.
*   **Powered by Gemini:** Utilizes Google's Gemini model for advanced language processing and task execution.

## Project Structure

```
marketing112/
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
├── requirements.txt      # Project dependencies
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

1. Clone the repository:
   ```bash
   git clone https://github.com/j-ferreiracosta/marketing112.git
   cd marketing112
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure Environment Variables:
   ```bash
   cp .env.example .env
   ```
   * Add the following required variables:
     ```dotenv
     GEMINI_API_KEY="your_google_gemini_api_key"
     SERPER_API_KEY="your_serperdev_api_key"
     ```
   * Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
   * Obtain a Serper API key from [Serper.dev](https://serper.dev/) for the search tool.

5. Run the agent:
   ```bash
   crewai run
   ```

## Usage

1.  **Prepare Input:**
    *   Edit the `src/marketing112/inputs.txt` file.
    *   Paste the unstructured text describing your information product, target audience, marketing goals, existing assets, brand voice, etc. Write this description in Portuguese, as the agents are primarily configured for it.

2.  **Run the Crew:**
    The standard way to run a CrewAI project:
    ```bash
    crewai run 
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
