#!/usr/bin/env python3
import argparse
import logging
import os
import time

from systemd_watchdog_thread import wdt_logger, __version__, run_watchdog

print(f"Version {__version__}")

def main():
    logging.basicConfig()
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--loglevel', default='WARN', help="Python logging level")
    parser.add_argument('--usec',type=int,help="Set micro-seconds" )
    parser.add_argument('--sleep',type=int,default=5,help="Time of main run in seconds")

    args = parser.parse_args()
    if args.usec:
        os.environ['WATCHDOG_USEC'] = str(args.usec)

    wdt_logger.setLevel(getattr(logging,args.loglevel))
    run_watchdog()
    time.sleep(args.sleep)

if __name__ == "__main__":
    main()
