#! /bin/sh
### BEGIN INIT INFO
# Provides:          capisuite
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Capisuite daemon
### END INIT INFO
#
# Script to start/stop capisuite daemon during boot/shutdown or from
# cardmgr via script from a /etc/pcmcia/<script>
#
#		Written by Miquel van Smoorenburg <miquels@cistron.nl>.
#		Modified for Debian GNU/Linux
#		by Ian Murdock <imurdock@gnu.ai.mit.edu>.
#		Modified for capisuite package
#		by Achim Bohnet <ach@mpe.mpg.de>
#
# Version:	@(#)skeleton  1.8  03-Mar-1998  miquels@cistron.nl
#
# This file was automatically customized by dh-make on Mon, 10 Mar 2003 21:37:06 +0100

PATH=/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/sbin/capisuite
NAME=capisuite
DESC="capisuite daemon"

test -f $DAEMON || exit 0

run_capisuite_daemon=n

if [ -f /etc/default/capisuite ]; then
  . /etc/default/capisuite
fi
if [ "y" != "$run_capisuite_daemon" ]; then
  echo " 
/etc/init.d/capisuite: To use the fax and/or voice box services of capisuite
                       configure files in '/etc/capisuite/'. Then set
		       'run_capisuite_daemon' to 'y' in /etc/default/capisuite.
"
  exit 0
fi

set -e

case "$1" in
  start)
	echo -n "Starting $DESC: "
	start-stop-daemon --start --quiet --background --make-pidfile --pidfile /var/run/$NAME.pid \
		--exec $DAEMON
	echo "$NAME."
	;;
  stop)
	echo -n "Stopping $DESC: "
	start-stop-daemon --oknodo --stop --quiet --pidfile /var/run/$NAME.pid \
		--exec $DAEMON
	rm -f /var/run/$NAME.pid
	echo "$NAME."
	;;
  restart|force-reload)
	echo -n "Restarting $DESC: "
	start-stop-daemon --oknodo --stop --quiet --pidfile /var/run/$NAME.pid \
		--exec $DAEMON
	sleep 1
	start-stop-daemon --start --quiet --background --make-pidfile --pidfile /var/run/$NAME.pid \
		--exec $DAEMON
	echo "$NAME."
	;;
  *)
	N=/etc/init.d/$NAME
	echo "Usage: $N {start|stop|restart|force-reload}" >&2
	exit 1
	;;
esac

exit 0
