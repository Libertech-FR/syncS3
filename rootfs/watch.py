#!/usr/bin/python3
import os.path
import argparse
import pyinotify

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
       print(f"IN_CLOSE_WRITE event detected on: {event.pathname}")
    def process_IN_DELETE(self,event):
       print(f"IN_DELETE event detected on: {event.pathname}")
def main():
    global __SECTION__
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='configFile',default='/data')
    args = parser.parse_args()
    path = args.path
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE
    notifier = pyinotify.Notifier(wm, EventHandler())
    wm.add_watch(path, mask,rec=True)
    try:
        notifier.loop()
    except KeyboardInterrupt:
        print("Stopped.")
if __name__ == "__main__":
    main()
