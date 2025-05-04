# src/marketing112/app3.py (Combined UI and Crew Execution)
import gradio as gr
import os
from dotenv import load_dotenv
import time
import random
import markdown
import re
import threading # Added for running crew in background
import queue # Added for communication with thread
from marketing112.crew import MarketingInfoProductCrew # Import from app.py

load_dotenv()

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up two levels to get the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
# Define the reports directory relative to the project root
REPORTS_DIR_ABS = os.path.join(PROJECT_ROOT, "reports")

# Ensure the reports directory exists
if not os.path.exists(REPORTS_DIR_ABS):
    os.makedirs(REPORTS_DIR_ABS)

# Define the expected report files in order of generation
EXPECTED_REPORTS = [
    "1structured_project_context_pt.md",
    "2market_research_report_pt.md",
    "3competitor_analysis_report_pt.md",
    "4marketing_strategy_report_pt.md",
    "5launch_angle_and_hook_report_pt.md",
    "6lead_magnet_brief_report_pt.md",
    "7optin_page_copy_draft_pt.md",
    "8sales_page_copy_draft_pt.md",
    "9email_sequence_prelaunch_draft_pt.md",
    "10email_sequence_sales_draft_pt.md",
    "11social_media_launch_posts_draft_pt.md",
    "12creative_review_feedback.md",
    "13final_info_product_launch_plan_pt.md"
]

# Map filenames to user-friendly task names
TASK_NAMES = {
    "1structured_project_context_pt.md": "Structuring Knowledge",
    "2market_research_report_pt.md": "Market Research",
    "3competitor_analysis_report_pt.md": "Competitor Analysis",
    "4marketing_strategy_report_pt.md": "Developing Strategy",
    "5launch_angle_and_hook_report_pt.md": "Creating Launch Hooks",
    "6lead_magnet_brief_report_pt.md": "Designing Lead Magnet",
    "7optin_page_copy_draft_pt.md": "Writing Opt-in Page Copy",
    "8sales_page_copy_draft_pt.md": "Writing Sales Page Copy",
    "9email_sequence_prelaunch_draft_pt.md": "Writing Pre-launch Emails",
    "10email_sequence_sales_draft_pt.md": "Writing Sales Emails",
    "11social_media_launch_posts_draft_pt.md": "Drafting Social Posts",
    "12creative_review_feedback.md": "Reviewing Content",
    "13final_info_product_launch_plan_pt.md": "Compiling Final Report"
}

FINAL_REPORT_FILENAME = EXPECTED_REPORTS[-1] # Use the last report as the final one
FINAL_REPORT_PATH_ABS = os.path.join(REPORTS_DIR_ABS, FINAL_REPORT_FILENAME)

# Convert markdown to HTML with proper styling (from app2.py)
def convert_markdown_to_html(md_text):
    # Process code blocks with syntax highlighting
    md_text = re.sub(r'```(\w+)\n(.*?)\n```', r'<pre><code class="language-\1">\2</code></pre>', md_text, flags=re.DOTALL)

    # Convert standard markdown to HTML
    html = markdown.markdown(
        md_text,
        extensions=['extra', 'smarty', 'tables', 'nl2br']
    )

    # Apply additional styling for better readability
    styled_html = f"""
    <div class="markdown-content">
        {html}
    </div>
    """
    return styled_html

# Define the absolute path to the CSS file (from app2.py)
CSS_FILE_PATH = os.path.join(SCRIPT_DIR, "style.css")

# Read CSS content from file (from app2.py)
try:
    with open(CSS_FILE_PATH, 'r', encoding='utf-8') as f:
        CUSTOM_CSS_FROM_FILE = f.read()
except FileNotFoundError:
    print(f"Warning: CSS file not found at {CSS_FILE_PATH}. Using default styles.")
    CUSTOM_CSS_FROM_FILE = "" # Provide empty string as fallback

# Emoji/icon themes (from app2.py)
SUCCESS_ICONS = ["✨", "✅", "🌿", "🍃", "🌱"]
PROCESS_ICONS = ["🖋️", "📝", "🔖", "📊", "📈"]
ERROR_ICONS = ["📌", "🔍", "📢", "✒️", "💭"]

def get_random_icon(icon_set):
    return random.choice(icon_set)

# --- Crew Execution Function with Threading and File Monitoring ---
def run_crew_in_thread(knowledge_base_text: str, result_queue: queue.Queue):
    """Target function for the thread to run the crew kickoff."""
    try:
        inputs = {'knowledge_base_text': knowledge_base_text}
        crew_instance = MarketingInfoProductCrew()
        result = crew_instance.crew().kickoff(inputs=inputs)
        result_queue.put(result)
    except Exception as e:
        result_queue.put(e) # Put the exception in the queue

def run_crew(knowledge_base_text: str, progress=gr.Progress(track_tqdm=True)):
    """
    Runs the MarketingInfoProductCrew in a thread, monitors report file creation,
    yields status updates formatted as HTML for the Gradio interface,
    and includes the final report content or download link.
    """
    if not knowledge_base_text:
        yield f"<div style='color: var(--secondary-color);'>{get_random_icon(ERROR_ICONS)} Please provide your product vision to begin crafting your strategy.</div>"
        return

    output_html = "" # Accumulate HTML output
    progress_percent = 0
    reports_found = 0
    total_reports = len(EXPECTED_REPORTS)
    result_queue = queue.Queue()

    # Initializing message
    progress_percent = 2 # Small initial progress
    icon = get_random_icon(PROCESS_ICONS)
    update = f"<div class='status-update'><span class='status-icon sparkle'>{icon}</span> <b>Initializing Crew...</b></div>"
    output_html += update
    yield f"""
    <div class='container'>
        <div class='progress-container'>
            <div class='progress-bar' style='width: {progress_percent}%'></div>
        </div>
        {output_html}
    </div>
    """
    time.sleep(0.5) # Short delay for visual feedback

    # Start the crew execution in a separate thread
    crew_thread = threading.Thread(target=run_crew_in_thread, args=(knowledge_base_text, result_queue))
    crew_thread.start()

    # Monitor thread and report files
    while crew_thread.is_alive():
        # Check for the next expected report file
        if reports_found < total_reports:
            next_report_filename = EXPECTED_REPORTS[reports_found]
            next_report_path = os.path.join(REPORTS_DIR_ABS, next_report_filename)

            if os.path.exists(next_report_path):
                reports_found += 1
                progress_percent = int((reports_found / total_reports) * 95) # Cap progress before final step
                task_name = TASK_NAMES.get(next_report_filename, f"Task {reports_found}")
                icon = get_random_icon(PROCESS_ICONS)
                update = f"<div class='status-update'><span class='status-icon'>{icon}</span> <b>Completed:</b> {task_name}</div>"
                output_html += f"<br/>{update}"
                yield f"""
                <div class='container'>
                    <div class='progress-container'>
                        <div class='progress-bar' style='width: {progress_percent}%'></div>
                    </div>
                    {output_html}
                </div>
                """
        time.sleep(1) # Check every second

    # Wait for the thread to finish (should be quick now)
    crew_thread.join()

    # Get the result or exception from the queue
    try:
        result = result_queue.get_nowait()
        if isinstance(result, Exception):
            raise result # Re-raise the exception caught in the thread
    except queue.Empty:
        result = None # Should not happen if thread finished, but handle defensively
        print("Warning: Crew thread finished but queue was empty.")
    except Exception as e:
        # Handle exceptions raised from the thread
        progress_percent = 100 # Show full bar even on error
        icon = get_random_icon(ERROR_ICONS)
        error_message = f"An error occurred during crew execution: {str(e)}"
        update = f"<div class='status-update' style='color: red;'><span class='status-icon'>{icon}</span> <b>Error:</b> {error_message}</div>"
        output_html += f"<br/>{update}"
        yield f"""
        <div class='container'>
            <div class='progress-container'>
                <div class='progress-bar' style='width: {progress_percent}%; background: red;'></div>
            </div>
            {output_html}
        </div>
        """
        return # Stop processing on error

    # Crew finished successfully, process final report
    progress_percent = 98 # Nearly done
    icon = get_random_icon(SUCCESS_ICONS)
    update = f"<div class='status-update'><span class='status-icon sparkle'>{icon}</span> <b>Crew execution finished.</b> Processing final report...</div>"
    output_html += f"<br/>{update}"
    yield f"""
    <div class='container'>
        <div class='progress-container'>
            <div class='progress-bar' style='width: {progress_percent}%'></div>
        </div>
        {output_html}
    </div>
    """
    time.sleep(0.5) # Simulate report processing

   # Final report generation/check
    progress_percent = 100

    if os.path.exists(FINAL_REPORT_PATH_ABS):
        with open(FINAL_REPORT_PATH_ABS, "r", encoding="utf-8") as f:
            report_content = f.read()

        # --- START: Add cleaning logic ---
        cleaned_report_content = report_content.strip()
        # Remove potential markdown code fences
        if cleaned_report_content.startswith("```markdown"):
            cleaned_report_content = cleaned_report_content[len("```markdown"):].lstrip()
        elif cleaned_report_content.startswith("```"):
             cleaned_report_content = cleaned_report_content[len("```"):].lstrip()

        if cleaned_report_content.endswith("```"):
             cleaned_report_content = cleaned_report_content[:-len("```")].rstrip()

        # Overwrite the file with cleaned content only if changes were made
        if cleaned_report_content != report_content:
            try:
                with open(FINAL_REPORT_PATH_ABS, "w", encoding="utf-8") as f:
                    f.write(cleaned_report_content)
                print(f"Cleaned markdown tags from and overwrote: {FINAL_REPORT_PATH_ABS}")
            except Exception as write_err:
                print(f"Warning: Could not overwrite cleaned report file {FINAL_REPORT_PATH_ABS}: {write_err}")
                # Continue with the cleaned content in memory anyway

        report_content = cleaned_report_content # Use cleaned content going forward
        # --- END: Add cleaning logic ---


        # Convert markdown report to HTML for display
        formatted_report = convert_markdown_to_html(report_content) # Use the cleaned content

        # Create download link
        file_url_path_abs = FINAL_REPORT_PATH_ABS.replace(os.path.sep, '/')
        download_link = f'<a href="/file={file_url_path_abs}" target="_blank" download="{FINAL_REPORT_FILENAME}" class="download-link">Download the Final Report ({FINAL_REPORT_FILENAME})</a>'

        icon = get_random_icon(SUCCESS_ICONS)
        update = f"""
        <div class='status-update'><span class='status-icon sparkle'>{icon}</span> <b>Strategy Crafted Successfully!</b></div>
        {download_link}
        <div class='report-content'>
            <h3 style="font-family: var(--heading-font); color: var(--secondary-color);">Final Launch Plan Preview:</h3>
            {formatted_report}
        </div>
        """
        output_html += f"<br/>{update}"
    else:
        # This case might happen if the final report task failed silently or the filename is wrong
        icon = get_random_icon(ERROR_ICONS)
        update = f"<div class='status-update' style='color: var(--accent-soft);'><span class='status-icon'>{icon}</span> <b>Warning:</b> Crew finished, but the final report file '{FINAL_REPORT_FILENAME}' was not found in '{REPORTS_DIR_ABS}'.<br/>Raw result from crew: {result}</div>"
        output_html += f"<br/>{update}"

    # Yield final state with report or warning
    yield f"""
    <div class='container'>
        <div class='progress-container'>
            <div class='progress-bar' style='width: {progress_percent}%; background: var(--primary-color);'></div>
        </div>
        {output_html}
    </div>
    """


# --- Gradio Interface (from app2.py, adapted for real crew) ---
with gr.Blocks(css=CUSTOM_CSS_FROM_FILE, theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_classes=["container"]):
        # Header
        with gr.Row(elem_classes=["header"]):
            gr.HTML("""
                <h1>✨ Marketing Launch Strategist ✨</h1>
                <p>Crafting your info-product launch, step by step.</p>
            """)

        # Input Section
        with gr.Column(elem_classes=["vision-input-container"]):
            with gr.Row(elem_classes=["vision-input-header"]):
                 gr.HTML("<span class='vision-input-label'>Describe Your Product Vision</span>")
            gr.HTML("""
                    <div>
                    <strong class='vision-input-label'>Include details like:</strong>
                    <ul>
                        <li>What is the core product/service?</li>
                        <li>Who is your ideal customer?</li>
                        <li>What problem does it solve or benefit does it provide?</li>
                        <li>What makes it unique?</li>
                        <li>What are your main goals for the launch?</li>
                    </ul>
                    </div>
                    """)
            gr.HTML("<p class='vision-input-description'>Share the core idea, target audience, and goals for your info-product.</p>")


            knowledge_base_input = gr.Textbox(
                label="", # Label handled by HTML above
                placeholder="e.g., 'A comprehensive online course teaching sustainable gardening techniques for urban dwellers, aiming to empower city residents to grow their own food.'",
                lines=6,
                elem_id="input-box"
            )

        # Buttons
        with gr.Row(elem_classes=["button-container"]):
            clear_btn = gr.Button("Clear Vision", elem_id="clear-btn", size="sm")
            submit_btn = gr.Button("🚀 Generate Launch Strategy", variant="primary", elem_id="submit-btn")

        # Output Section (Progress and Report)
        output_display = gr.HTML(label="Strategy Progress & Report") # Use HTML for rich output

        # Footer
        with gr.Row(elem_classes=["footer"]):
            gr.HTML("Powered by CrewAI & Gradio | Real Agent Collaboration")

    # --- Event Handlers (adapted for real crew) ---

    # Define button click behavior with progress updates
    def submit_action(knowledge_text):
        # Disable button immediately
        yield {submit_btn: gr.update(value="🏃‍♂️ Running Crew...", interactive=False),
               output_display: "<div class='container'><div class='status-update'><span class='status-icon'>⏳</span> Starting... Please wait.</div></div>"} # Initial feedback

        # Stream output from run_crew
        final_output_html = ""
        # Use the modified run_crew which now handles threading and progress
        for status_update_html in run_crew(knowledge_text):
            final_output_html = status_update_html # Keep track of the latest state
            yield {output_display: final_output_html} # Update the output display progressively

        # Re-enable button after the generator is exhausted
        yield {submit_btn: gr.update(value="🚀 Generate Launch Strategy", interactive=True)}


    submit_btn.click(
        fn=submit_action, # Use the wrapper function
        inputs=[knowledge_base_input],
        outputs=[output_display, submit_btn] # Update both output and button state
    )

    # Clear button action remains the same
    clear_btn.click(lambda: ("", "<div class='container'></div>"), inputs=None, outputs=[knowledge_base_input, output_display])


# Launch the Gradio app (using app.py's launch config)
if __name__ == "__main__":
    print(f"Reports will be saved in/read from: {REPORTS_DIR_ABS}")
    print(f"Expecting final report: {FINAL_REPORT_PATH_ABS}")
    if not os.path.exists(REPORTS_DIR_ABS):
         print(f"Warning: Reports directory '{REPORTS_DIR_ABS}' does not exist. It will be created if needed.")
    # Allow serving files from the absolute path of the 'reports' directory for downloads
    demo.launch(share=False, allowed_paths=[REPORTS_DIR_ABS]) # Set share=True for public link
