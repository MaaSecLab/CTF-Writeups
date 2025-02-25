## WAIT
### Problem Description
We made a game.

**Link:** https://drive.google.com/file/d/1GDYmOiW54pPLFxfQaBOOS5IPEAoplFPy/view?usp=drive_link


### Solution
For this challenge we are again given an executable. Running the game we can see a lot of "pixels" and a countdown at the bottom left. The pixels move as the timer approaches 0, into their correct position. The pixels at the end of the countdown would probably turn into the flag so we knew we had to modify the countdown value. At first, we used CheatEngine and modified the value of the counter but the program kept quitting out. We then realized that the game was written in the godot engine, due to the logo of the application. This meant that we would be able to perform a near perfect decompilation. We used gdsdecomp to get the source code and then imported the files into a project editor. We found the following code that handles the countdown timer:

`	var curr_time = Time.get_datetime_dict_from_system()
	time_left = (ct.month-curr_time.month)*86400*30+(ct.year-curr_time.year)*86400*30*12+(ct.day-curr_time.day)*86400+(ct.hour-curr_time.hour)*3600+(ct.minute-curr_time.minute)*60+(ct.second-curr_time.second)
	time_left=max(0,time_left)`

Modifying the code to decrease the value of time_left and running the application will show us the mostly generated flag. 


Have a great day :)
github.com/johnnnathan
