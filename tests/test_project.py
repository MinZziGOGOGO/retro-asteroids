"""Basic project sanity tests."""


def test_import() -> None:
    """Verify the package imports cleanly."""
    import retro_asteroids  # noqa: F401


def test_main_exists() -> None:
    """Verify main entry point is callable."""
    from retro_asteroids.main import main

    assert callable(main)
