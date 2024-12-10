import os # JW: allows us to interact with the operating system
from time import time, strftime, localtime # JW: allows us to use various time related operations #MS: added strftime and localtime
import random # JW: allows us to use a random number generator for the .DAT file names
import string # JW: allows us to use strings
import pyinotify # JW: allows us to monitor a directory for changes
from pathlib import Path # JW: allows us to create the path if it isn't created already
import difflib 

#JW: sets the folders used in the project as variables
WATCHED_FOLDER = Path("/home/vboxuser/project/watched")
CHANGELOG_FOLDER = Path("/home/vboxuser/project/hidden_journal")

#MS: ensuring the directories for the folders exist
WATCHED_FOLDER.mkdir(parents=True, exist_ok=True)
CHANGELOG_FOLDER.mkdir(parents=True, exist_ok=True)

#MS: replaces the dots in the original file with underscores for .DAT files
def Sanitize_File_Name(fileName):
  return fileName.replace('.', '_')

#JW: check to see if the file being passed is a swap file. Used for making sure the .swp file of created files aren't logged 
def Text_File_Check(filename):
  return filename.endswith(".txt")

#MS: maps the original file path to its .DAT file
file_mapping = {}

#MS: generates the path for the .DAT file
def Get_DAT_File_Path(event):
  origianlName = os.path.basename(event.pathname)
  sanitizedName = Sanitize_File_Name(originalName)
  if event.pathname not in file_mapping:
    randomNumber = random.randint(10000, 99999) #MS: creates a random 5 digit number
    DAT_fileName = f"j1_{sanitizedName}_{randomNumber}.DAT" #MS: formats the file into a .DAT file
    file_mapping[event.pathname] = CHANGELOG_FOLDER / DAT_fileName
  return file_mapping[event.pathname]

#MS: returns the content of the file as a list of lines
def Get_File_Content(filePath):
  try:
    with open(filePath, 'r') as file:
      return file.readlines()
  except Exception:
    return []

#MS: writes down the changes to the .DAT file
def Write_Change(DAT_filePath, timestamp, changeType, content):
  with open(DAT_filePath, 'a') as DAT_file:
    DAT_file.write(f"{timestamp} | {changeType}: {content}\n")

#MS: creates a new .DAT file to log changes to the text file
def Initialize_DAT_File(event):
  DAT_filePath = Get_DAT_File_Path(event)
  #MS: writes details about the .DAT file
  timestamp = strftime(timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
  try:
    with open(DAT_filePath, 'w') as DAT_file:
      DAT_file.write(f"Event Type: IN_CREATE\n")
      DAT_file.write(f"Timestamp: {timestamp}\n")
      dat_file.write(f"Original Path: {event.pathname}\n")
      dat_file.write("Changes:\n")
    print(f"Initialized .DAT file: {dat_file_path}")
  expect Exception as e:
    print(f"Error initializing .DAT file {DAT_filePath}: {e}")

#JW: defines the class to help with the creation, deletion, and modifications of files
class EventHandler(pyinotify.ProcessEvent):
  def process_IN_CREATE(self, event):
    #JW: If the file is not a .txt file, nothing happens
    if not Text_File_Check(event.pathname):
      return

    print(f"File created: {event.pathname}")
    Create_Journal_File(event)

  def process_IN_DELETE(self, event):
    if not Text_File_Check(event.pathname):
      return

    print(f"File deleted: {event.pathname}")
    #MS: added more lines of code to handle the deletion of a file
    DAT_filePath = Get_DAT_File_Path(event)
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
    Write_Change(DAT_filePath, timestamp, "DELETED", "File was deleted.")

  def process_IN_CLOSE_WRITE(self, event):
    if not Text_File_Check(event.pathname):
      return

    print(f"File modified: {event.pathname}")
    currentContent = Get_File_Content(event.pathname) #MS: reads the current file contents
    backupPath = f"{event.pathname}.bak"
    if not backupPath.exists():
      print(f"No backup found for: {event.pathname}. Skipping diff calculation.")
      return
    oldContent = Get_File_Content(backupPath) #MS: reads the old file contents
    diff = "".join(difflib.unified_diff(old_content, new_content, lineterm="")) #MS: compares the old and new version of the file to find changes
    
    #MS: if a difference exists, log it into the .DAT file
    if diff:
      timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
      DAT_filePath = Get_DAT_File_Path(event)
      with open(DAT_File_Path, 'a') as DAT_File:
        DAT_File.write(f"Timestamp: {timestamp}\n")
        DAT_File.write(f"Changes: \n")
        DAT_File.write(diff)
        DAT_File.write(DAT_file.write"\n")
      print(f"Logged chagnes to: {DAT_filePath}")
    else:
      print(f"No changes detected in: {event.pathname}")

    #MS: updates backup content for new changes
    try:
      with open(backupPath, 'w') as f:
        f.writelines(currentContent)
    except Exception as e:
      print(f"Error updating backup for {event.pathname}: {e}")

print(f"Setting up watch manager...")
try:
  Watch_Manager = pyinotify.WatchManager() #JW: sets up the watch manager for the file system
  Event_Handler = EventHandler() # JW: sets up the event handler for the file system
  Notifier = pyinotify.Notifier(Watch_Manager, Event_Handler) #JW: sets up notifier with the watch manager & event

  Watch_Manager.add_watch(str(WATCHED_FOLDER), pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE) #MS: watches for the creation, deletion, and modification of files in the watched folder

  #MS: starts the notifier
  print(f"Monitoring changes in: {WATCHED_FOLDER}")
  Notifier.loop()
except Exception as e:
  print(f"Error setting up watch manager: {e}")