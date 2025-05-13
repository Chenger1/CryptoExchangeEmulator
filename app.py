def run_cli():
    import sys
    import traceback
    from pathlib import Path

    from loguru import logger

    current_path = Path(__file__).parent.parent.resolve()
    sys.path.append(str(current_path))

    try:
        from src import start_app
        start_app()
    except ImportError as e:
        traceback.print_exc()
        logger.error(f'Unable to load libraries: {e}.')
        sys.exit(1)


if __name__ == "__main__":
    run_cli()
