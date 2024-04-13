# systemd-watchdog-thread
Runs [systemd](https://en.wikipedia.org/wiki/Systemdwatchdog) notifies in thread.

When *run()* is called it sends the READY message to systemd and then
sends WATCHDOG messages at one-half the interval set by the WATCHDOG_USEC
environment variable.

It runs as a daemon [thread](https://docs.python.org/3/library/threading.html#thread-objects),
so it will exit when the main program exits.

## usage

    from systemd_watchdog_thread import WatchdogThread

    wdt = WatchdogThread()
    t = wdt.run()

or

    from systemd_watchdog_thread import run_watchdog 

    run_watchdog()

## testing
*finish()* may be called to stop sending READY messages. This is provided to test
the systemd watchdog functionality.