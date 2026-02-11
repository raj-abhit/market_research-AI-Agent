from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool , ScrapeWebsiteTool , SeleniumScrapingTool
from dotenv import load_dotenv
import os

load_dotenv(override=True)


def resolve_model() -> str:
    """Resolve model name and normalize deprecated Gemini aliases."""
    model = os.getenv("MODEL", "gpt-4o-mini").strip()
    deprecated_gemini = {
        "gemini-1.5-flash",
        "gemini/gemini-1.5-flash",
        "models/gemini-1.5-flash",
    }
    if model in deprecated_gemini:
        return "gemini/gemini-2.0-flash-001"
    return model


def resolve_max_tokens() -> int:
    """Bound output token count to control spend and provider limits."""
    return int(os.getenv("MAX_TOKENS", "300"))


def resolve_max_iter() -> int:
    """Limit reasoning loops to reduce repeated LLM calls."""
    return int(os.getenv("MAX_ITER", "2"))


def resolve_max_rpm() -> int:
    """Throttle request rate to avoid provider rate limits."""
    return int(os.getenv("MAX_RPM", "2"))

#create tools
web_search_tool = SerperDevTool()
web_scraping_tool = ScrapeWebsiteTool()
Selenium_scraping_tool = SeleniumScrapingTool()

toolkit = [web_search_tool, Selenium_scraping_tool, web_scraping_tool]




#define  the crew class
@CrewBase
class MarketResearchCrew():
    """MarketResearchCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    #provide the path for confguration file
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    # agent builder function
    @agent
    def market_research_specialist(self) -> Agent:
       return Agent(
           config = self.agents_config["market_research_specialist"],
           llm = LLM(
               model=resolve_model(),
               temperature=0.7,
               max_tokens=resolve_max_tokens()
           ),
           max_iter=resolve_max_iter(),
           verbose=True
    )
       
    @agent
    def competitive_intelligence_analyst(self) -> Agent:
       return Agent(
           config = self.agents_config["competitive_intelligence_analyst"],
           llm = LLM(
               model=resolve_model(),
               temperature=0.7,
               max_tokens=resolve_max_tokens()
           ),
           max_iter=resolve_max_iter(),
           verbose=True
    )
           
    @agent
    def customer_insights_researcher(self) -> Agent:
       return Agent(
           config = self.agents_config["customer_insights_researcher"],
           llm = LLM(
               model=resolve_model(),
               temperature=0.7,
               max_tokens=resolve_max_tokens()
           ),
           max_iter=resolve_max_iter(),
           verbose=True
    )
       
    @agent
    def product_strategy_advisor(self) -> Agent:
       return Agent(
           config = self.agents_config["product_strategy_advisor"],
           llm = LLM(
               model=resolve_model(),
               temperature=0.7,
               max_tokens=resolve_max_tokens()
           ),
           max_iter=resolve_max_iter(),
           verbose=True
    )
       
    @agent
    def business_analyst(self) -> Agent:
       return Agent(
           config = self.agents_config["business_analyst"],
           llm = LLM(
               model=resolve_model(),
               temperature=0.7,
               max_tokens=resolve_max_tokens()
           ),
           max_iter=resolve_max_iter(),
           verbose=True
    )
       
       #tasks builder function
    
    @task
    def market_research_task(self) -> Task:
        return Task(
            config = self.tasks_config["market_research_task"]
        )
        
    @task
    def competitive_intelligence_task(self) -> Task:
        return Task(
            config = self.tasks_config["competitive_intelligence_task"],
            context = [self.market_research_task()]
        )
        
    @task
    def customer_insights_task(self) -> Task:
        return Task(
            config = self.tasks_config["customer_insights_task"],
            context = [self.market_research_task(),
                       self.competitive_intelligence_task()]
        )
        
    @task
    def product_strategy_task(self) -> Task:
        return Task(
            config = self.tasks_config["product_strategy_task"],
            context = [self.market_research_task(),
                       self.competitive_intelligence_task(),
                       self.customer_insights_task()]
        )
        
    @task
    def business_analysis_task(self) -> Task:
        return Task(
            config = self.tasks_config["business_analyst_task"],
            # Keep final synthesis context focused to avoid oversized prompts/rate limits.
            context = [self.product_strategy_task()],
            output_file = "reports/report.md"
        )
        
        #define the crew function
        
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            max_rpm=resolve_max_rpm()
        )
