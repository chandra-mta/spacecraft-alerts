#!/usr/bin/env /proj/sot/ska3/flight/bin/python
"""
Spacecraft Alerting Script
"""

import spacecraft_alerts
import argparse
from configparser import ConfigParser, ExtendedInterpolation
_CONFIGS = ConfigParser(interpolation = ExtendedInterpolation(), default_section='primary')
_CONFIGS.read('config.ini')

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices = ['primary', 'secondary', 'buocc', 'test'], required = True, help = "Determine configuration of script run.")
    return parser.parse_args()

def load_config(mode):
    config = _CONFIGS[mode]
    return config

if __name__ == "__main__":
    #: Determine Config Section
    args = get_options()
    config = load_config(args.mode)