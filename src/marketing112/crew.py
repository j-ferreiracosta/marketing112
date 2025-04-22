# marketing112/crew.py
from typing import List, Optional, Dict, Any
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

load_dotenv()	

# Uncomment the following line to use an example of a custom tool
# from marketing_posts.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field


# --- Pydantic Models ---

# Model to structure the extracted knowledge from the input text
class ProductInfo(BaseModel):
    name: Optional[str] = Field(description="Extracted product name.")
    description: Optional[str] = Field(description="Extracted full product description.")
    key_benefits_differentials: List[str] = Field(default=[], description="List of extracted key benefits or differentiators.")
    usp: Optional[str] = Field(description="Extracted Unique Value Proposition.")
    price_info: Optional[str] = Field(description="Extracted pricing information (e.g., '297€, com campanhas a 247€').")
    product_link_placeholder: Optional[str] = Field(description="Placeholder or note about the product link mentioned.")

class CampaignObjective(BaseModel):
    primary_goal: Optional[str] = Field(description="Extracted primary campaign goal.")
    specific_measurable_goal: Optional[str] = Field(description="Extracted specific, measurable goal (e.g., leads, sales targets).")
    funnel_stage_focus: List[str] = Field(default=[], description="Extracted funnel stages targeted (e.g., Top, Middle, Bottom).")
    calls_to_action: List[str] = Field(default=[], description="List of extracted Calls to Action (CTAs).")

class AudienceDemographics(BaseModel):
    age_range: Optional[str] = Field(description="Extracted target age range.")
    gender: Optional[str] = Field(description="Extracted target gender.")
    location: Optional[str] = Field(description="Extracted target location.")
    income_level: Optional[str] = Field(description="Extracted target income level.")
    education_level: Optional[str] = Field(description="Extracted target education level.")
    profession: Optional[str] = Field(description="Extracted target profession.")

class AudiencePsychographics(BaseModel):
    interests: List[str] = Field(default=[], description="List of extracted interests.")
    hobbies: List[str] = Field(default=[], description="List of extracted hobbies.")
    values: List[str] = Field(default=[], description="List of extracted values.")
    lifestyle: List[str] = Field(default=[], description="List of extracted lifestyle descriptions.")

class AudienceBehaviors(BaseModel):
    online_activity: List[str] = Field(default=[], description="Notes on online activity (platforms used).")
    purchase_history: List[str] = Field(default=[], description="Notes on relevant purchase history.")
    brand_loyalty: List[str] = Field(default=[], description="Notes on brand loyalty or influencers followed.")

class TargetAudience(BaseModel):
    demographics: Optional[AudienceDemographics] = None
    psychographics: Optional[AudiencePsychographics] = None
    behaviors: Optional[AudienceBehaviors] = None
    challenges: List[str] = Field(default=[], description="List of extracted audience challenges or pain points.")
    specific_segments: List[str] = Field(default=[], description="List of extracted specific audience segments.")

class CommunicationStyle(BaseModel):
    tone: List[str] = Field(default=[], description="List of words describing the desired tone.")
    keywords: List[str] = Field(default=[], description="List of specific keywords or terms to use.")
    brand_restrictions: List[str] = Field(default=[], description="List of brand style restrictions (colors, typography, voice notes).")
    preferred_examples: List[str] = Field(default=[], description="Notes on preferred communication examples.")

class CampaignDetails(BaseModel):
    budget: Optional[str] = Field(description="Extracted campaign budget information.")
    duration: Optional[str] = Field(description="Extracted campaign duration information (e.g., capture phase, sales phase).")
    past_references: List[str] = Field(default=[], description="Notes on past campaigns or successful references.")
    visual_guidelines: List[str] = Field(default=[], description="Notes on visual guidelines for creatives.")
    platform_preferences: List[str] = Field(default=[], description="List of preferred platforms for the campaign.")

class FullProjectContext(BaseModel):
    """Structured context extracted from the unstructured input text."""
    product_info: Optional[ProductInfo] = None
    campaign_objectives: Optional[CampaignObjective] = None
    target_audience: Optional[TargetAudience] = None
    communication_style: Optional[CommunicationStyle] = None
    campaign_details: Optional[CampaignDetails] = None
    source_language: str = Field(default="Portuguese", description="Language of the source document.")
    other_notes: List[str] = Field(default=[], description="Any other relevant notes extracted.")


# Models for Strategy and Content (Potentially containing Portuguese)
class OfferStack(BaseModel):
    """Details of the core offer."""
    main_product: str = Field(..., description="Description of the main info-product.")
    bonuses: List[str] = Field(description="List of bonuses included.")
    price_tiers: List[str] = Field(..., description="Pricing tiers or options.")
    guarantee: Optional[str] = Field(description="Description of the guarantee offered.")
    payment_options: List[str] = Field(description="Available payment options.")

class LaunchPhase(BaseModel):
    """Activities for a specific launch phase."""
    phase_name: str = Field(..., description="Name of the phase (e.g., Pre-launch, Launch Week, Post-launch).")
    activities: List[str] = Field(..., description="List of key activities planned for this phase.")

class LaunchStrategy(BaseModel):
    """Comprehensive Info-Product Launch Strategy."""
    launch_goals: List[str] = Field(..., description="Specific, measurable goals for the launch.")
    target_audience_summary: str = Field(..., description="Refined summary of the target audience profile for Portugal.")
    usp: str = Field(..., description="Unique Selling Proposition of the info-product (should be in Portuguese).")
    core_offer_stack: OfferStack
    phased_launch_plan: List[LaunchPhase]
    list_building_strategy: str = Field(..., description="Primary strategy for building the email list pre-launch.")
    key_messaging_pillars: List[str] = Field(..., description="Core themes or angles for communication (in Portuguese).")
    recommended_channels: List[str] = Field(..., description="Marketing channels to focus on (Email, Social, Meta Ads, etc.).")
    kpis: List[str] = Field(..., description="Key Performance Indicators to track launch success.")

class LaunchHook(BaseModel):
    """A single creative angle or hook for the launch campaign."""
    angle_name: str = Field(..., description="Short name or title for the angle (in Portuguese).")
    description: str = Field(..., description="Brief description of the core message and emotional appeal (in Portuguese).")

class LaunchHookList(BaseModel):
    """List of launch hooks."""
    hooks: List[LaunchHook]

class LeadMagnetBrief(BaseModel):
    """Concept brief for a lead magnet."""
    topic: str = Field(..., description="Specific topic of the lead magnet (in Portuguese).")
    format: str = Field(..., description="Format (e.g., PDF Checklist, Video Workshop Outline, Template).")
    value_proposition: str = Field(..., description="Key value or transformation offered (in Portuguese).")
    connection_to_product: str = Field(..., description="How it naturally leads to the main info-product (in Portuguese).")

class PageCopy(BaseModel):
    """Copy elements for a landing/opt-in page."""
    headline: str = Field(..., description="Main headline grabbing attention (in Portuguese).")
    sub_headline: Optional[str] = Field(description="Supporting sub-headline (in Portuguese).")
    body_bullet_points: List[str] = Field(..., description="Bullet points highlighting benefits or contents (in Portuguese).")
    call_to_action: str = Field(..., description="The text for the call-to-action button/link (in Portuguese).")

class Email(BaseModel):
    """Represents a single email in a sequence."""
    subject: str = Field(..., description="The email subject line (in Portuguese).")
    body: str = Field(..., description="The main body content of the email (in Portuguese).")

class EmailSequence(BaseModel):
    """A sequence of emails for a specific purpose (e.g., nurture, sales)."""
    sequence_name: str = Field(..., description="Name of the email sequence (e.g., Pre-Launch Nurture).")
    emails: List[Email]

class SocialPost(BaseModel):
    """Represents a single social media post."""
    text: str = Field(..., description="The main text content of the post (in Portuguese).")
    phase: str = Field(..., description="Launch phase this post belongs to (e.g., Pre-launch, Launch Week, Cart Close).")
    platform_note: Optional[str] = Field(description="Optional note about target platform or visual suggestion.")

class SocialMediaPlan(BaseModel):
    """A collection of social media posts for the launch."""
    posts: List[SocialPost]


@CrewBase
class MarketingInfoProductCrew():
    """MarketingInfoProductCrew crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Initialize tools potentially used by agents
        self.web_scraper = ScrapeWebsiteTool()
        self.search_tool = SerperDevTool()

    # --- Agent Definitions ---
    @agent
    def input_text_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['input_text_analyzer'],
            verbose=True,
            memory=False,
            # No tools needed for basic text analysis, relies on LLM capability
        )

    @agent
    def lead_market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_market_analyst'],
            tools=[self.search_tool, self.web_scraper], # Tools for external research
            verbose=True,
            memory=False, # Allow memory for multi-step research
        )

    @agent
    def chief_marketing_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_marketing_strategist'],
             # Tools might be useful for strategy validation/inspiration
            tools=[self.search_tool, self.web_scraper],
            verbose=True,
            memory=False,
        )

    @agent
    def creative_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_content_creator'],
            verbose=True,
            memory=False,
            # Consider setting a specific LLM if needed for better Portuguese generation
            # llm=YourLLMConfiguration()
        )

    @agent
    def email_marketing_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['email_marketing_specialist'],
            verbose=True,
            memory=False,
            # llm=YourLLMConfiguration() if needed
        )

    @agent
    def social_media_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_manager'],
            verbose=True,   
            memory=False,
            # llm=YourLLMConfiguration() if needed
        )

    @agent
    def chief_creative_director(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_creative_director'],
            verbose=True,
            memory=False,
        )

    @agent
    def final_report_synthesizer(self) -> Agent:
        return Agent(
            config=self.agents_config['final_report_synthesizer'],
            verbose=True,
            memory=False,
        )

    # --- Task Definitions ---

    # Input & Foundation Tasks
    @task
    def extract_and_structure_knowledge_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_and_structure_knowledge_task'],
            agent=self.input_text_analyzer(),
            output_pydantic=FullProjectContext
            # The input 'knowledge_base_text' will be interpolated from crew.kickoff()
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.lead_market_analyst(),
            context=[self.extract_and_structure_knowledge_task()], # Depends on structured context
            output_file='market_research_report_pt.md'
        )

    @task
    def project_competitors_task(self) -> Task:
        return Task(
            config=self.tasks_config['project_competitors_task'],
            agent=self.lead_market_analyst(),
             # Depends on structured context and initial research
            context=[self.extract_and_structure_knowledge_task(), self.research_task()],
            output_file='competitor_analysis_report_pt.md'
        )

    # Strategy Task
    @task
    def marketing_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['marketing_strategy_task'],
            agent=self.chief_marketing_strategist(),
             # Depends on structured context, research, competitors
            context=[self.extract_and_structure_knowledge_task(), self.research_task(), self.project_competitors_task()],
            output_pydantic=LaunchStrategy
        )

    # Content Creation Tasks
    @task
    def launch_angle_and_hook_task(self) -> Task:
        return Task(
            config=self.tasks_config['launch_angle_and_hook_task'],
            agent=self.creative_content_creator(),
            # Needs strategy and original context (for brand voice, keywords etc.)
            context=[self.marketing_strategy_task(), self.extract_and_structure_knowledge_task()],
            output_pydantic=LaunchHookList
        )

    @task
    def create_lead_magnet_brief_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_lead_magnet_brief_task'],
            agent=self.creative_content_creator(),
            context=[self.marketing_strategy_task(), self.extract_and_structure_knowledge_task()],
            output_pydantic=LeadMagnetBrief
        )

    @task
    def write_optin_page_copy_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_optin_page_copy_task'],
            agent=self.creative_content_creator(),
            context=[self.create_lead_magnet_brief_task(), self.marketing_strategy_task(), self.extract_and_structure_knowledge_task()],
            output_pydantic=PageCopy
        )

    @task
    def write_sales_page_copy_task(self) -> Task:
        # Outputting long-form text to file is generally more reliable
        return Task(
            config=self.tasks_config['write_sales_page_copy_task'],
            agent=self.creative_content_creator(),
            context=[self.marketing_strategy_task(), self.research_task(), self.launch_angle_and_hook_task(), self.extract_and_structure_knowledge_task()],
            output_file='sales_page_copy_draft_pt.md'
        )

    @task
    def write_email_sequence_task_PRELAUNCH(self) -> Task:
        return Task(
            config=self.tasks_config['write_email_sequence_task_PRELAUNCH'],
            agent=self.email_marketing_specialist(),
            context=[self.marketing_strategy_task(), self.create_lead_magnet_brief_task(), self.extract_and_structure_knowledge_task()],
            output_pydantic=EmailSequence
        )

    @task
    def write_email_sequence_task_SALES(self) -> Task:
        return Task(
            config=self.tasks_config['write_email_sequence_task_SALES'],
            agent=self.email_marketing_specialist(),
             # Needs sales page copy (from file) and strategy/context
            context=[self.marketing_strategy_task(), self.write_sales_page_copy_task(), self.extract_and_structure_knowledge_task()],
            output_pydantic=EmailSequence
        )

    @task
    def write_social_media_launch_posts_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_social_media_launch_posts_task'],
            agent=self.social_media_manager(),
            context=[self.marketing_strategy_task(), self.launch_angle_and_hook_task(), self.extract_and_structure_knowledge_task()],
            output_pydantic=SocialMediaPlan
        )

    # Review Task
    @task
    def review_launch_content_task(self) -> Task:
        # Review feedback is often textual commentary
        return Task(
            config=self.tasks_config['review_launch_content_task'],
            agent=self.chief_creative_director(),
            context=[ # Pass all relevant generated content and strategy context
                self.launch_angle_and_hook_task(),
                self.create_lead_magnet_brief_task(),
                self.write_optin_page_copy_task(),
                self.write_sales_page_copy_task(),
                self.write_email_sequence_task_PRELAUNCH(),
                self.write_email_sequence_task_SALES(),
                self.write_social_media_launch_posts_task(),
                self.marketing_strategy_task(), # Needs strategy for alignment check
                self.extract_and_structure_knowledge_task() # Needs original style guidelines
            ],
            output_file='creative_review_feedback.md'
        )

    # Final Output Task
    @task
    def compile_final_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['compile_final_report_task'],
            agent=self.final_report_synthesizer(),
            context=[ # Collect all major outputs
                self.extract_and_structure_knowledge_task(),
                self.research_task(),
                self.project_competitors_task(),
                self.marketing_strategy_task(),
                self.launch_angle_and_hook_task(),
                self.create_lead_magnet_brief_task(),
                self.write_optin_page_copy_task(),
                self.write_sales_page_copy_task(),
                self.write_email_sequence_task_PRELAUNCH(),
                self.write_email_sequence_task_SALES(),
                self.write_social_media_launch_posts_task(),
                self.review_launch_content_task() # Include the feedback
            ],
            output_file='final_info_product_launch_plan_pt.md'
        )

    # --- Crew Definition ---
    @crew
    def crew(self) -> Crew:
        """Creates the Marketing Info Product Launch crew"""
        return Crew(
            agents=self.agents,   # Automatically gathered by @agent decorators
            tasks=self.tasks,    # Automatically gathered by @task decorators
            process=Process.sequential, # Let context define the execution flow
            verbose=True,           # Log level (1 for basic, 2 for detailed)
            memory=False          # Enable memory for context sharing between agents/tasks
            # You might want to explore manager_llm for hierarchical process later
            # manager_llm=YourLLMConfiguration() # if using Process.hierarchical
        )