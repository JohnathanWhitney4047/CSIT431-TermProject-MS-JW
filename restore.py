import os #JW: Allows us to interact with Operating System
import sys #JW: allows us to mess with various parts of Python
import datetime #JW: allows us to use time
#JW: Initialize variables for the directories
DAT_FOLDER = "/home/vboxuser/project/hidden_journal"
RESTORED_FOLDER = "/home/vboxuser/project/restored_files"

#JW: Function that does the recreation
def Recreate_File(journal_file, timestamp):

  print(f"Starting recreation...")
  
  journal_path = os.path.join(DAT_FOLDER, journal_file) #JW: Creates the path for the journal file

#JW: Checks to see if the journal file exists
  if not os.path.exists(journal_path):
    print(f"Journal file not found: {journal_path}")
    return

#JW: Opens journal file so it can be read
  with open(journal_path, 'r') as file:
    lines = file.readlines()
#JW: looks for the line with a matching timestamp
  target_timestamp = f"Timestamp: {timestamp}"
  file_lines = []
  found_timestamp = False

#JW: After finding the matching timestamp start logging the file, and after the end of log message is reached, stop.
  for line in lines:
    print(f"Processing line: {line.strip()}")
    if line.startswith("Timestamp:"):
      print(f"Found timestamp: {line.strip()}")
      if target_timestamp in line:
        print(f"Matched target timestamp: {target_timestamp}")
        found_timestamp = True
        continue


      if found_timestamp:
        print("Reached next timestamp; stopping.")
        break


    if found_timestamp:
      if "--- End of log ---" in line:
        continue

      file_lines.append(line.strip())


  if not found_timestamp:
    print(f"No matching timestamp found in {journal_file}")
    return

#JW: Creates the name and path for the restored version of the file.
  restored_file_name = journal_file.replace(".DAT", ".txt")
  restored_path = os.path.join(RESTORED_FOLDER, restored_file_name)


#JW: Makes sure that the restored files directory actually exists
  os.makedirs(RESTORED_FOLDER, exist_ok=True)

#JW: Writes the logged contents from the timestamp to the new file
  with open(restored_path, 'w') as restored_file:
    restored_file.write("\n".join(file_lines))
  print(f"Restored file saved to: {restored_path}")

#JW: Check to make sure there is a proper amount of arguments
if __name__ == "__main__":
  if len(sys.argv) != 3:
    print("Usage: python3 restore.py <journal_file> <timestamp>")
    sys.exit(1)

#JW: Gets the journal file and timestamp needed
  journal_file = sys.argv[1]
  timestamp = sys.argv[2]


  Recreate_File(journal_file, timestamp)

