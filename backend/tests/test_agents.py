import pytest
from app.agents.planner_agent import PlannerAgent
from app.agents.research_agent import ResearchAgent
from app.agents.coder_agent import CoderAgent

@pytest.mark.asyncio
async def test_planner_agent():
    agent = PlannerAgent()
    result = await agent.execute("Create a simple web application")
    assert result["status"] == "success"
    assert "plan" in result

@pytest.mark.asyncio
async def test_research_agent():
    agent = ResearchAgent()
    result = await agent.execute("Research machine learning algorithms")
    assert result["status"] == "success"
    assert "research_results" in result

@pytest.mark.asyncio
async def test_coder_agent():
    agent = CoderAgent()
    result = await agent.execute("Generate a Python script for data analysis")
    assert result["status"] == "success"
    assert "code" in result 