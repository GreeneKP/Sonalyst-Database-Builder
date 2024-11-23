Steps to Database Building:

(for the duration of this readme, note that the apostrophe symbol is used to denote what you should type, but should not itself be included in any typed entry.)

1. Right click in the Sonalyst Database Builder Folder to open command line there. Alternatively you can navigate there using a combination of pwd (to check out where you are), dir (to see your available directories to move into), and cd (to move accordingly).

2. After having opened the command prompt (assuming you're using unix or a unix-parallel syntax,) type 'conda activate' (this step assumes you have downloaded the anaconda libraries; this is critical for the different dependencies if you haven't already done it).

3. Type 'python dbuild.py'; the first prompt asking for your desired SCC should appear. As a test, you can either skip it or select 28885, just to check in on a satellite we know is in GEO.

4. The next prompt asks you to type an option indicating how many additional satellites you want to build the database for; this is valuable insomuch that tools which should show the positioning of a number of satellites all at once wouldn't be starved. Bear in mind, however, on my 64g RAM computer, I'm averaging 3 minutes to completion per satellite, so option 5, for example, takes about 2.5 hours... your mileage may vary. BE SURE TO ONLY TYPE A SINGLE DIGIT CORRESPONDING WITH THE OPTION. i.e. if you want 30 additionals, DO NOT type '30', instead, type '3'.

5. The script should tell you when each satellite is complete though I'll admit, without a status bar amid a slow process, it can be a little daunting just twiddling thumbs hoping it's doing its job; Opening the StateDatabase folder might help ease the tension since you can actually see files be edited and altered in there. You'll note that the StateDatabase folder will start to fill up. One thing worth noting is that this tool appends to each file, but doesn't check to see if the data from that TLE is already present in it. As such, I'd recommend any time you want to rerun it, just clear out the whole StateDatabasefolder so the tool has some fresh space to work with... checking for present TLEs might be something I add to it in time, but admittedly this project has changed forms a number of times, particularly after the streamlit interface was ditched. Might reattack that effort in the future, but I'd rather you have a minimum-viable product now to make the most of your time; I can always make it play nicer and improve the user experience and subsequent accessibility later.

