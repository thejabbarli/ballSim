#!/usr/bin/env python3
"""BallSim - Entry point."""

import argparse
import sys
from pathlib import Path

from src.factories import SimulationFactory


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BallSim - Physics-based ball bouncing simulation renderer"
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default="config/simulation.yaml",
        help="Path to configuration file (default: config/simulation.yaml)"
    )
    
    args = parser.parse_args()
    
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        return 1
    
    try:
        simulation = SimulationFactory.create_from_config(config_path)
        simulation.run()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
