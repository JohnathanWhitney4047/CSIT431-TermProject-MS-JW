import os # JW: allows us to interact with the operating system
from time import time, strftime, localtime # JW: allows us to use various time related operations #MS: added strftime and localtime
import random # JW: allows us to use a random number generator for the .DAT file names
import pyinotify # JW: allows us to monitor a directory for changes
from pathlib import Path # JW: allows us to create the path if it isn't created already

#JW: sets the folders used in the project as variables
WATCHED_FOLDER = Path("/home/vboxuser/project/watched")
CHANGELOG_FOLDER = Path("/home/vboxuser/project/hidden_journal")
DAT_FILE_USED = None 

#MS: ensuring the directories for the folders exist
WATCHED_FOLDER.mkdir(parents=True, exist_ok=True)
CHANGELOG_FOLDER.mkdir(parents=True, exist_ok=True)


#MS: replaces the dots in the original file with underscores for .DAT files
def Sanitize_File_Name(fileName):
  return fileName.replace('.', '_')

#JW: Check to see if the file being passed is a swap file. Used for making sure the .swp file of created files aren't logged 
def Text_File_Check(fileName):
  return fileName.endswith(".txt")

#MS: creates the .DAT files in the hidden journal
def Create_Journal_File(event, prefix="j1"):
  global DAT_FILE_USED
  #JW: If the file is not a .txt file it is skipped
  if not Text_File_Check(event.pathname):
    return

  print(f"Creating journal file for: {event.pathname}")
  randomNumber = random.randint(10000, 99999) #MS: creates a random 5 digit number
  originalName = os.path.basename(event.pathname) #MS: extracts the file name
  sanitizedName = Sanitize_File_Name(originalName)
  DATFileName = f"{prefix}_{sanitizedName}_{randomNumber}.DAT" #MS: formats the file into a .DAT file
  DATFilePath = CHANGELOG_FOLDER / DATFileName

  DAT_FILE_USED = DATFilePath

  try:
    with open(DATFilePath, 'w') as file:
      file.write(f"Journal for {originalName}\n")
    print(f"Created journal file: {DATFilePath}")
  except Exception as e:
    print(f"Error creating journal file: {DATFilePath}: {e}")

def Log_File_Content(event):
  global DAT_FILE_USED

  if not Text_File_Check(event.pathname):
    return

  try:
    with open(event.pathname, 'r') as file:
      current_content = file.read()
    print(f"Read current content from {event.pathname}: {current_content[:100]}...")
  except Exception as e:
    print(f"Error readinf file {event.pathname}: {e}")
    return

  if not DAT_FILE_USED:
    print("No .DAT file selected, skipping log writing.")
    return

  timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
  try:
    with open(DAT_FILE_USED, 'a') as dat_file:
      dat_file.write(f"\nTimestamp: {timestamp}\n")
      dat_file.write(current_content)
      dat_file.write("\n--- End of log ---\n")
  except Exception as e:
    print(f"Error writing to journal file{DAT_FILE_USED}: {e}")

# JW: defines the class to help with the creation, deletion, and modifications of files
class EventHandler(pyinotify.ProcessEvent):
  def process_IN_CREATE(self, event):
    if not Text_File_Check(event.pathname):
      return

    print(f"File created: {event.pathname}")
    Create_Journal_File(event)

  def process_IN_DELETE(self, event):
    if not Text_File_Check(event.pathname):
      return

    print(f"File deleted: {event.pathname}")

  def process_IN_CLOSE_WRITE(self, event):
    if not Text_File_Check(event.pathname):
      return

    print(f"File modified: {event.pathname}")
    Log_File_Content(event)

print(f"Setting up watch manager...")
Watch_Manager = pyinotify.WatchManager() #JW: sets up the watch manager for the file system
Event_Handler = EventHandler() # JW: sets up the event handler for the file system
Notifier = pyinotify.Notifier(Watch_Manager, Event_Handler) #JW: sets up notifier with the watch manager & event

Watch_Manager.add_watch(str(WATCHED_FOLDER), pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE) #MS: watches for the creation, deletion, and modification of files in the watched folder

#MS: starts the notifier
print(f"Monitoring changes in: {WATCHED_FOLDER}")
Notifier.loop()
