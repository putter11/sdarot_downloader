# Code to download episodes from sdarot
Hello!

To use the code please first install selenium, tqdm, pandas and requests running:

pip install selenium

pip install tqdm

pip install pandas

pip install requests

Also, you need to download from here https://github.com/mozilla/geckodriver/releases the geckodriver for your system, unzip it and put it in a folder which is in your PATH.

After that the program should be ready to use.

The program reads which episodes to downaload from the excel.
The excel in the reposoitory contains an example for a valid download requesrt.
The series number is the number you see in the url of a series page in sdarot.
The series name is only used in order to give a meaningfull name to the created files, you can put whatever you want there.
The format for the seasons the episodes is x-y and will download from episode/season x to y.
If you want to download several seasons with differnt number of episodes just write the highest episode number as y, the program will just continue if it can't find a specific episode.

As default the program saves the downloaded videos in the current folder. If you want to change that you can use the flag -v and write the path where you would like the videos to be saved.
You can also move the excel file from the folder of the scrpit, but then you'll need to use the flag -e and specify the location of the excel.
