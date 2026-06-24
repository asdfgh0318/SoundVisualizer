from server.core.config import Config, load_config


def test_research_trees_empty_by_default(tmp_path):
    cfg = load_config(tmp_path / "nope.toml")
    assert cfg.research_trees == []


def test_legacy_singular_research_tree_folds_into_list(tmp_path):
    """Old [research_tree] config still works after the multi-tree refactor."""
    p = tmp_path / "config.toml"
    p.write_text(
        """
[research_tree]
enabled = true
base_url = "http://localhost:8123"
public_url = "https://jama.local:8000"
""".lstrip()
    )
    cfg = load_config(p)
    assert len(cfg.research_trees) == 1
    rt = cfg.research_trees[0]
    assert rt.name == "default"
    assert rt.enabled is True
    assert rt.base_url == "http://localhost:8123"
    assert rt.public_url == "https://jama.local:8000"


def test_multi_tree_list_parses(tmp_path):
    p = tmp_path / "config.toml"
    p.write_text(
        """
[[research_trees]]
name = "duct"
enabled = true
base_url = "http://localhost:8123"

[[research_trees]]
name = "drone-paczek"
enabled = true
base_url = "http://localhost:8124"
""".lstrip()
    )
    cfg = load_config(p)
    assert [t.name for t in cfg.research_trees] == ["duct", "drone-paczek"]
    assert all(t.enabled for t in cfg.research_trees)
    assert cfg.research_trees[1].base_url == "http://localhost:8124"


def test_new_list_form_wins_over_legacy_if_both_present(tmp_path):
    """A config that accidentally contains both shapes prefers the new list
    (no silent merging that would surprise the user)."""
    p = tmp_path / "config.toml"
    p.write_text(
        """
[research_tree]
enabled = true
base_url = "http://localhost:9999"

[[research_trees]]
name = "duct"
enabled = true
base_url = "http://localhost:8123"
""".lstrip()
    )
    cfg = load_config(p)
    assert [t.name for t in cfg.research_trees] == ["duct"]
    assert cfg.research_trees[0].base_url == "http://localhost:8123"


def test_load_config_returns_defaults_when_missing(tmp_path):
    cfg = load_config(tmp_path / "nonexistent.toml")
    assert isinstance(cfg, Config)
    assert cfg.tyto.enabled is False
    assert cfg.tyto.tty == "/dev/ttyUSB0"
    assert cfg.tyto.calibration.hinge_distance == 0.07492


def test_load_config_overrides_from_file(tmp_path):
    p = tmp_path / "config.toml"
    p.write_text(
        """
[tyto]
enabled = true
tty = "/dev/ttyACM0"

[tyto.calibration]
hinge_distance = 0.1
cal_thrust = -1.0
""".lstrip()
    )
    cfg = load_config(p)
    assert cfg.tyto.enabled is True
    assert cfg.tyto.tty == "/dev/ttyACM0"
    assert cfg.tyto.calibration.hinge_distance == 0.1
    assert cfg.tyto.calibration.cal_thrust == -1.0
    # unspecified field falls through to default
    assert cfg.tyto.calibration.cal_poles == 14
