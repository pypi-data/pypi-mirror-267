"""
Go through a series of prompts to construct a custom configuration.
"""

from enum import Enum
from pathlib import Path
from typing import Set

from rich.text import Text

from ... import ui
from ...config import HYPER_CONFIG_FILE_NAME, PYPROJECT_FILE_NAME, ConfigFile
from ...version import Version
from .file_validation import DefinitionValidator
from .files import FilesConfigEditor
from .git import GitConfigEditor


class TopMenu(Enum):
    General = "general"
    Files = "files"
    Git = "git"
    Done = "done"


class InteractiveConfigEditor:
    def __init__(
        self,
        initial_config: ConfigFile,
        pyproject: bool,
        project_root: Path,
    ) -> None:
        if initial_config.current_version is None:
            raise ValueError(
                "The current version of the initial config must not be None."
            )
        self._current_version: Version = initial_config.current_version
        self._config: ConfigFile = initial_config.model_copy(deep=True)
        self._pyproject = pyproject
        self._project_root = project_root
        self._was_configured: Set[TopMenu] = set()
        self._config_funcs = {
            TopMenu.General: self._configure_general,
            TopMenu.Files: self._configure_files,
            TopMenu.Git: self._configure_git,
        }

    def configure(self) -> tuple[ConfigFile, bool]:
        """
        Use interactive prompts to allow the user to edit the configuration.

        :return: First, Configuration with the user's edits.
            Second, `True` if the configuration should be written to pyproject.toml.
            Otherwise (`False`), the configuration should be written to hyper-bump-it.toml.
        """
        while (selection := _prompt_top_level_menu()) is not TopMenu.Done:
            ui.blank_line()
            self._was_configured.add(selection)
            self._config_funcs[selection]()

        return self._config, self._pyproject

    def _configure_general(self) -> None:
        show_confirm_prompt = _prompt_show_confirm(self._config.show_confirm_prompt)
        ui.blank_line()
        self._pyproject = _prompt_pyproject(self._pyproject)
        ui.blank_line()
        self._config = self._config.model_copy(
            update={"show_confirm_prompt": show_confirm_prompt}
        )

    def _configure_files(self) -> None:
        editor = FilesConfigEditor(
            self._config.files,
            DefinitionValidator(self._current_version, self._project_root),
        )
        file_config, has_keystone = editor.configure()
        current_version = None if has_keystone else self._current_version
        self._config = self._config.model_copy(
            update={"files": file_config, "current_version": current_version}
        )

    def _configure_git(self) -> None:
        editor = GitConfigEditor(self._config.git)
        self._config = self._config.model_copy(update={"git": editor.configure()})


def _prompt_top_level_menu() -> TopMenu:
    return ui.choice_enum(
        "What part of configuration would you like to edit?",
        option_descriptions={
            TopMenu.General: "Top level settings that don't fit in a specific category",
            TopMenu.Files: "File matching settings",
            TopMenu.Git: "Git integration settings",
            TopMenu.Done: "Stop editing and write out the configuration",
        },
        default=TopMenu.Done,
    )


def _prompt_show_confirm(show_confirm_prompt: bool) -> bool:
    # It is easier to phrase the question as disabling the prompt. So the default is negated,
    # then the response is flipped back to the meaning used within the program.
    return not ui.confirm(
        Text()
        .append("hyper-bump-it", style="app")
        .append(
            " shows a confirmation prompt before performing the actions.\n"
            "Do you want to silence this prompt and execute the actions automatically?"
        ),
        default=not show_confirm_prompt,
    )


def _prompt_pyproject(pyproject: bool) -> bool:
    return ui.confirm(
        Text()
        .append("hyper-bump-it", style="app")
        .append(" can store the configuration in ")
        .append(PYPROJECT_FILE_NAME, style="file.path")
        .append(" instead of ")
        .append(HYPER_CONFIG_FILE_NAME, style="file.path")
        .append(".\nDo you want to use ")
        .append(PYPROJECT_FILE_NAME, style="file.path")
        .append("?"),
        default=pyproject,
    )
