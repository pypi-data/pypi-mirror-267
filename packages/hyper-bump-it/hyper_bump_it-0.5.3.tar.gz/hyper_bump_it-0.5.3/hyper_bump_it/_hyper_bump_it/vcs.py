"""
Operation on git repositories.
"""

from dataclasses import dataclass
from pathlib import Path

from git import InvalidGitRepositoryError, Repo

from .config import Git, GitAction, GitActions
from .error import (
    AlreadyExistsError,
    DetachedRepositoryError,
    DirtyRepositoryError,
    DisallowedInitialBranchError,
    EmptyRepositoryError,
    MissingRemoteError,
    NoRepositoryError,
)
from .format_pattern import TextFormatter


@dataclass
class GitOperationsInfo:
    remote: str
    commit_message: str
    branch_name: str
    tag_name: str
    tag_message: str
    allowed_initial_branches: frozenset[str]
    actions: GitActions

    @classmethod
    def from_config(cls, config: Git, formatter: TextFormatter) -> "GitOperationsInfo":
        """
        Convert the configuration into the necessary operation information.

        :param config: Configuration of how git operations should operate.
        :param formatter: Object that converts format patterns into text.
        :return: Git operation information.
        :raises FormatError: Format pattern was invalid or attempted to use an invalid key.
        """
        return cls(
            remote=config.remote,
            commit_message=formatter.format(config.commit_format_pattern),
            branch_name=formatter.format(config.branch_format_pattern),
            tag_name=formatter.format(config.tag_name_format_pattern),
            tag_message=formatter.format(config.tag_message_format_pattern),
            allowed_initial_branches=config.allowed_initial_branches,
            actions=config.actions,
        )


def get_vetted_repo(project_root: Path, operation_info: GitOperationsInfo) -> Repo:
    """
    Retrieve the git repository, ensuring it is in the expected state.

    :param project_root: Root of the project repository.
    :param operation_info: Git operation information.
    :return: Repository that is valid for the planned operations.
    :raises GitError: Repository was not compatible with the configured git operations.
    """
    try:
        repo = Repo(project_root)
    except InvalidGitRepositoryError:
        raise NoRepositoryError(project_root)

    if len(repo.heads) == 0:
        raise EmptyRepositoryError(project_root)

    if repo.is_dirty():
        raise DirtyRepositoryError(project_root)

    if repo.head.is_detached:
        raise DetachedRepositoryError(project_root)

    _validate_repo_for_operations(repo, operation_info, project_root)

    return repo


def _validate_repo_for_operations(
    repo: Repo, operation_info: GitOperationsInfo, project_root: Path
) -> None:
    if operation_info.allowed_initial_branches and all(
        allowed_branch != repo.active_branch.name
        for allowed_branch in operation_info.allowed_initial_branches
    ):
        raise DisallowedInitialBranchError(
            operation_info.allowed_initial_branches,
            repo.active_branch.name,
            project_root,
        )

    if operation_info.actions.any_push and operation_info.remote not in repo.remotes:
        raise MissingRemoteError(operation_info.remote, project_root)

    if (
        operation_info.actions.branch.should_create
        and operation_info.branch_name in repo.heads
    ):
        raise AlreadyExistsError("branch", operation_info.branch_name, project_root)

    if (
        operation_info.actions.tag.should_create
        and operation_info.tag_name in repo.tags
    ):
        raise AlreadyExistsError("tag", operation_info.tag_name, project_root)


def create_branch(repo: Repo, branch_name: str) -> None:
    repo.create_head(branch_name)


def switch_to(repo: Repo, branch_name: str) -> None:
    repo.heads[branch_name].checkout()


def commit_changes(repo: Repo, commit_message: str) -> None:
    index = repo.index
    for diff in index.diff(None):
        if diff.deleted_file:
            index.remove(diff.a_path)
        else:
            index.add(diff.a_path)

    index.write_tree()
    repo.git.commit(message=commit_message)


def create_tag(repo: Repo, tag_name: str, tag_message: str) -> None:
    repo.create_tag(tag_name, message=tag_message)


def push_changes(repo: Repo, operation_info: GitOperationsInfo) -> None:
    to_push = [
        (
            operation_info.branch_name
            if operation_info.actions.branch == GitAction.CreateAndPush
            else repo.active_branch.name
        )
    ]
    if operation_info.actions.tag == GitAction.CreateAndPush:
        to_push.append(operation_info.tag_name)

    remote = repo.remotes[operation_info.remote]
    remote.push(to_push, atomic=True)
