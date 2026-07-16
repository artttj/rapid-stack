from status_line import format_line, gather


def fake_run(responses):
    def run(args, cwd):
        return responses[args[0] if args[0] != "git" else " ".join(args[:3])]
    return run


def test_format_clean_pushed_with_pr():
    state = {"branch": "master", "dirty": False, "ahead": 0, "behind": 0,
             "upstream": True, "pr": "https://github.com/a/b/pull/1"}
    assert format_line(state) == "git: master — pushed — https://github.com/a/b/pull/1"


def test_format_dirty_ahead_no_pr():
    state = {"branch": "feat/x", "dirty": True, "ahead": 2, "behind": 0,
             "upstream": True, "pr": ""}
    assert format_line(state) == "git: feat/x* — 2 ahead — no PR"


def test_format_no_upstream():
    state = {"branch": "feat/x", "dirty": False, "ahead": 0, "behind": 0,
             "upstream": False, "pr": ""}
    assert format_line(state) == "git: feat/x — no upstream — no PR"


def test_format_not_a_repo():
    assert format_line(None) == "git: not a repository"


def test_gather_parses_counts_and_pr():
    responses = {
        "git rev-parse --abbrev-ref": (0, "feat/x"),
        "git status --porcelain": (0, "M file"),
        "git rev-list --left-right": (0, "1\t2"),
        "gh": (0, "https://github.com/a/b/pull/7"),
    }
    state = gather("/tmp", run=fake_run(responses))
    assert state == {"branch": "feat/x", "dirty": True, "ahead": 2,
                     "behind": 1, "upstream": True,
                     "pr": "https://github.com/a/b/pull/7"}


def test_gather_not_a_repo():
    responses = {"git rev-parse --abbrev-ref": (1, "")}
    state = gather("/tmp", run=fake_run(responses))
    assert state is None
