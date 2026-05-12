from server.core.config import Config, load_config


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
