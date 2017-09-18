#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from subprocess import Popen, PIPE, STDOUT
import os
import signal
import json

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


APPINDICATOR_ID = 'myappindicator'
p = None
def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_NETWORK, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_jupyter = gtk.MenuItem('Start server')
    item_jupyter.connect('activate', jupyterx)
    menu.append(item_jupyter)
    item_kill_jupyter = gtk.MenuItem('Stop server')
    item_kill_jupyter.connect('activate', kill_jupyter)
    menu.append(item_kill_jupyter)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def jupyterx(self):
	global p
	p = Popen(['/home/sid/anaconda2/bin/jupyter','notebook'], stdout=PIPE,stdin=PIPE,stderr=STDOUT)
	notify.Notification.new("<b>Server Started</b>", 'https://localhost:8888/', None).show()
	# return p.kill()

def kill_jupyter(self):
	global p
	if p is not None:
		p.kill()
		p.communicate(input=b'y\n')
	notify.Notification.new("<b>Server Stopped</b>", 'Stopped jupyter and killed it!', None).show()
# def fetch_joke():
#     request = Request('http://api.icndb.com/jokes/random?limitTo=[nerdy]')
#     response = urlopen(request)
#     joke = json.loads(response.read())['value']['joke']
#     return joke

# def joke(_):
#     notify.Notification.new("<b>Joke</b>", fetch_joke(), None).show()

def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
main()
