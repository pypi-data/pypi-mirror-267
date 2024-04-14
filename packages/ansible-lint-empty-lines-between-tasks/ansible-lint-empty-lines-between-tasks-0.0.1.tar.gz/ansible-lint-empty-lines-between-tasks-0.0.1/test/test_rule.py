from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner

from rules.empty_line_between_tasks import EmptyLineBetweenTasksRule


def test_success_playbook() -> None:
    """Positive test for no-changed-when."""
    collection = RulesCollection(rulesdirs=["rules/"])
    collection.register(EmptyLineBetweenTasksRule())
    success = "test/fixtures/success.playbook.yaml"
    good_runner = Runner(success, rules=collection)
    assert [] == good_runner.run()


def test_failure_playbook() -> None:
    """Negative test for no-changed-when."""
    collection = RulesCollection()
    collection.register(EmptyLineBetweenTasksRule())
    failure = "test/fixtures/failure.playbook.yaml"
    bad_runner = Runner(failure, rules=collection)
    errs = bad_runner.run()
    assert len(errs) == 3


def test_success_tasks() -> None:
    """Positive test for no-changed-when."""
    collection = RulesCollection(rulesdirs=["rules/"])
    collection.register(EmptyLineBetweenTasksRule())
    success = "test/fixtures/success_include.playbook.yaml"
    good_runner = Runner(success, rules=collection)
    assert [] == good_runner.run()


def test_failure_tasks() -> None:
    """Negative test for no-changed-when."""
    collection = RulesCollection()
    collection.register(EmptyLineBetweenTasksRule())
    failure = "test/fixtures/failure_include.playbook.yaml"
    bad_runner = Runner(failure, rules=collection)
    errs = bad_runner.run()
    assert len(errs) == 3
