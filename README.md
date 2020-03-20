# Code to download episodes from sdarot
Hello!

To use the code plaese first install selenium, tqdm and pandas running:

pip install selenium

pip install tqdm

pip install pandas.

Also, you need to download from here https://github.com/mozilla/geckodriver/releases the geckodriver for your system, unzip it and put it in a folder which is in your PATH.

After that the program should be ready to use.

Edit the excel for the episodes that you want to download.
In the excel there is an example for a valid download requesrt.
The series number is the number you see in the url of a series page in sdarot.
The series name is only for the name that will be given to the files you download so you can write there whatever you want. (for example GOT instead of Game of Thrones).
The seasons and episodes accepts the value in pattern x-y and will download from episode/season x to y include.
If you want to download several seasons with differnt number of episodes just write the highest episode number as y, the program will just continue if it can't find a specific episode.

As default the program saves the downloaded videos in the current folder. If you want to change that you can use the flag -v and write the path where you would like the videos to be saved.
You can also move the excel file from the folder of the scrpit, but then you'll need to use the flag -e and specify the location of the excel.
