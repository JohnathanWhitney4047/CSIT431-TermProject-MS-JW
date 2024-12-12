The setup may be a bit complicated. I apologize in advance.

The file system has hardcoded file paths so you may need to change them to fit your system in both the recreate.py and file_system.py files. In addition to these files, you want to create three folders, each titled: "hidden_journal", "restored_files", and "watched".

You are also going to want to make sure you have the following libraries installed:
os
sys
datetime
time
random
pyinotify
pathlib 

Make sure the three folders and two files are in the same directory, or you could go into the files and change them as needed. 

And make sure you run the file system using:
python3 file_system.py &
BEFORE you create any files in the watched folder. If you create the file in the watch folder before running the program in the background it will not be able to be logged. That also goes for if you kill the process and then run it again. You won't be able to make more logs but you can still recover since it is a different program.

Speaking of the recovery program, you can run it by typing:

python3 recreate.py (.DAT journal) "(time stamp)"

So an actual example would be:
python3 recreate.py j1_file_txt_12345.DAT "2024-12-12 7:00:00"
You have to go into the .DAT file itself in order to recover the date and time of a log. 

Then the log is sent to the "restored_files" folder.

