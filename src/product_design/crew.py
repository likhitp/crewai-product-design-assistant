import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ProductDesign():
	"""ProductDesign crew for IKEA innovation team pitch"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self):
		"""Initialize the ProductDesign crew with necessary tools"""
		self.search_tool = SerperDevTool()

	def _get_base_prompt(self, role):
		return f"""You are a {role}.
		
		When using tools, ALWAYS use this format:
		Thought: I need to [explain your thought process]
		Action: [tool name]
		Action Input: [input for the tool]
		
		When giving your final answer, ALWAYS use this format:
		Thought: I have enough information to provide a complete answer
		Final Answer: [your detailed response]
		
		Remember to:
		1. Always follow the exact format above
		2. Use tools when you need more information
		3. Give a Final Answer only when you have all needed information
		4. Format your Final Answer in markdown
		"""

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools

	@agent
	def market_analyst(self) -> Agent:
		base_prompt = self._get_base_prompt("Global Market Intelligence Analyst")
		return Agent(
			config=self.agents_config['market_analyst'],
			tools=[self.search_tool],
			verbose=True,
			llm_config={
				"temperature": 0.7,
				"request_timeout": 120,
				"max_retries": 3,
				"system_prompt": base_prompt
			}
		)

	@agent
	def tech_specialist(self) -> Agent:
		base_prompt = self._get_base_prompt("Technology and Materials Innovation Specialist")
		return Agent(
			config=self.agents_config['tech_specialist'],
			tools=[self.search_tool],
			verbose=True,
			llm_config={
				"temperature": 0.7,
				"request_timeout": 120,
				"max_retries": 3,
				"system_prompt": base_prompt
			}
		)

	@agent
	def feasibility_assessor(self) -> Agent:
		base_prompt = self._get_base_prompt("Product Feasibility Expert")
		return Agent(
			config=self.agents_config['feasibility_assessor'],
			tools=[self.search_tool],
			verbose=True,
			llm_config={
				"temperature": 0.7,
				"request_timeout": 120,
				"max_retries": 3,
				"system_prompt": base_prompt
			}
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task

	@task
	def market_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['market_analysis_task'],
			output_file='market_analysis.md'
		)

	@task
	def technical_assessment_task(self) -> Task:
		return Task(
			config=self.tasks_config['technical_assessment_task'],
			output_file='technical_assessment.md'
		)

	@task
	def feasibility_evaluation_task(self) -> Task:
		return Task(
			config=self.tasks_config['feasibility_evaluation_task'],
			output_file='feasibility_evaluation.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ProductDesign crew for IKEA innovation assessment"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			planning=True,  # Enable planning for better task coordination
			max_round=3  # Limit maximum rounds to prevent infinite loops
		)
