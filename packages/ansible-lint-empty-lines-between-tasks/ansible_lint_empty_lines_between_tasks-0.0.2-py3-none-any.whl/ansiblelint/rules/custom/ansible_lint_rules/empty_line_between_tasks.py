"""ansible-lint rule to detect missing empty lines between tasks."""

from __future__ import annotations

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from ansiblelint.errors import MatchError
from ansiblelint.file_utils import Lintable
from ansiblelint.rules import AnsibleLintRule, TransformMixin
from ansiblelint.utils import Task
from ruamel.yaml.comments import CommentedMap, CommentedSeq


def _parse_position(pos: str) -> list[str | int]:
    parts = pos.replace("[", ".").replace("]", ".").split(".")
    res: list[str | int] = []
    for p in [x for x in parts if x != ""]:
        try:
            res.append(int(p))
        except ValueError:
            res.append(p)
    return res


def _find_last_element_and_key(
    data: CommentedMap | CommentedSeq | str,
    key: str | int,
) -> tuple[CommentedMap | CommentedSeq | str, str | int]:
    if isinstance(data, CommentedSeq):
        elem = data
        item, key = _find_last_element_and_key(data[-1], len(data))
        if not isinstance(item, CommentedSeq | CommentedMap):
            return elem, key
        else:
            return item, key
    if isinstance(data, CommentedMap):
        last_key = list(data.keys())[-1]
        elem = data
        item, key = _find_last_element_and_key(data[last_key], last_key)
        if not isinstance(item, CommentedSeq | CommentedMap):
            return elem, key
        else:
            return item, key
    return data, key


class EmptyLineBetweenTasksRule(AnsibleLintRule, TransformMixin):
    """Tasks should be separated by an empty line."""

    id = "empty-line-between-tasks"
    description = "Ensure there is an empty line between consecutive tasks."
    tags = ["formatting"]
    severity = "VERY_LOW"

    def transform(
        self: Self,
        match: MatchError,
        lintable: Lintable,
        data: CommentedMap | CommentedSeq | str,
    ) -> None:
        if match.yaml_path == []:
            return
        elem = self.seek(match.yaml_path[:-1], data)
        elem.yaml_set_comment_before_after_key(
            match.yaml_path[-1],
            before="\n\n",
        )
        match.fixed = True

    def matchtask(
        self: Self,
        task: Task,
        file: Lintable | None = None,
    ) -> bool | str | MatchError | list[MatchError]:
        if not file:
            return []
        if (
            "tasks[0]" not in task.position
            and file.content.splitlines()[task["__line__"] - 2] != ""
        ) and task.position != ".[0]":
            match_ = MatchError(
                message="Missing empty line before Task",
                lintable=file,
                filename=file.filename,
                tag="",
                lineno=task["__line__"] - 1,
                details="",
                column=None,
                rule=self,
                ignored=False,
                fixed=False,
                transform_meta=None,
            )
            if match_.yaml_path == []:
                match_.yaml_path = _parse_position(task.position)
            return match_
        return False
