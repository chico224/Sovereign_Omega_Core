from pathlib import Path

from Sovereign-Omega AI.agents import Agent
from Sovereign-Omega AI.app.main import run_interaction_loop
from Sovereign-Omega AI.commands import COMMAND_CATEGORIES
from Sovereign-Omega AI.config import AIConfig, Config, ConfigBuilder
from Sovereign-Omega AI.memory.vector import get_memory
from Sovereign-Omega AI.models.command_registry import CommandRegistry
from Sovereign-Omega AI.prompts.prompt import DEFAULT_TRIGGERING_PROMPT
from Sovereign-Omega AI.workspace import Workspace

PROJECT_DIR = Path().resolve()


def run_task(task) -> None:
    agent = bootstrap_agent(task)
    run_interaction_loop(agent)


def bootstrap_agent(task):
    config = ConfigBuilder.build_config_from_env(workdir=PROJECT_DIR)
    config.continuous_mode = False
    config.temperature = 0
    config.plain_output = True
    command_registry = CommandRegistry.with_command_modules(COMMAND_CATEGORIES, config)
    config.memory_backend = "no_memory"
    config.workspace_path = Workspace.init_workspace_directory(config)
    config.file_logger_path = Workspace.build_file_logger_path(config.workspace_path)
    ai_config = AIConfig(
        ai_name="Sovereign-Omega AI",
        ai_role="a multi-purpose AI assistant.",
        ai_goals=[task.user_input],
    )
    ai_config.command_registry = command_registry
    return Agent(
        memory=get_memory(config),
        command_registry=command_registry,
        ai_config=ai_config,
        config=config,
        triggering_prompt=DEFAULT_TRIGGERING_PROMPT,
    )
