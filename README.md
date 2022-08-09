# Making A Harmonic DJ Set

In this project I chose to use Spotipy, a Python library for the Spotify API that is lightweight and can give full access to music data that is on Spotify’s platform. Spotipy’s ability to easily access client music data has played a significant role in this project. I highly recommend using Spotipy for any curiosity within music. Their website is https://spotipy.readthedocs.io/en/master/. 

This project develops a harmonic DJ set, or playlist, from a playlist already made in Spotify. The program uses the Spotify users’ credentials to find the selected playlist. The user then selects a starting song they would like to hear first. The final product is a purely harmonic set that follows the given tempo constraints.

## Motivation

With a Data Analyst background and music being a crucial role in my life, I was interested in these two coming together. After searching, I found Data Science for DJing by James Camagong (https://medium.com/swlh/data-science-for-djing-b4c7a422c197). The author, using Spotipy, goes into detail on different headlining DJs and analyses their styles during each set. This analysis was fascinating to me. As an avid music listener, I wanted to create something that would give the same feeling as the DJs did while performing, but I did not have have any DJ equipment and I was more interested on why they chose the songs they did during their set. 

For this project, I had an idea to create my own DJ set using a playlist of house music I made on Spotify. House music is a type of music that allows the artist to convey a fun rhythm to it to help the listener feel good and maybe dance. Once I started college, I was introduced to house music on various occasions and found a deep passion for it. Over the past four years, I found favorite artists that made songs I appreciated and started to listen to their sets that they make for concerts and music festivals. Finally, I dove deeper into the basics of DJing and found that different audio features of a song are used for a DJ to create an enjoyable set.

## Simple DJ Techniques

DJs use several techniques to make sure the listener can have an enjoyable experience. Two primary audio features they use to their advantage are tempo and key / the Camelot Wheel. The tempo of a song can range from 1-200+ beats per minute or BPM. House music, for example, usually ranges around 120 BPM (https://en.wikipedia.org/wiki/House_music). The other portion they use is key / the Camelot Wheel. The Camelot Wheel shows what songs mix with other songs harmonically. If a DJ is mixing towards the next song, they will usually use a tempo constraint and the Camelot Wheel to find smooth transitions. For more information on what the Camelot Wheel is and how harmonic mixing works, please visit https://mixedinkey.com/harmonic-mixing-guide/. 

## Producing the Algorithm

After getting the specific client credentials, the user gives the index of the starting song. The output is a data frame of a DJ set. First, the algorithm would get two audio features of the starting song, tempo and Camelot Score. Camelot Score is the value from the Camelot Wheel, but Spotify does not include this. The key and mode given from Spotify were used to make the Camelot Score. 

The first algorithm implemented would then randomly select a song from the rest of the data frame, get the tempo and Camelot Score, and check if the song satisfied the constraint for tempo and harmony. If it did, it would be dropped from the data frame and added to the final set, and the tempo and Camelot Score of the next song would become the previous songs’ tempo and Camelot Score. If not, a new song was chosen and the process would repeat until there were no more songs to harmonically mix with or an iterator’s value was met. This produced a correct set but was terribly inefficient.

For the second implementation of the algorithm, a dictionary of Camelot Scores was made, as well as, a dictionary where keys were the Camelot Scores and a list of all songs with the corresponding key’s Camelot Score was the value. This implementation required searching the songs that were harmonic with the previous song until a song met the tempo constraint. At this point, the new song is added to the set and removed from the pool of songs. Finally, the new song added becomes the previous song for the next iteration. This would run until there were no more songs that were harmonic with the previous song. 

## Results from Both Algorithms

My house music playlist that I was using only had, at the time, 160 songs in it. To see the change in the runtime of the algorithms, I needed to use a bigger data set. I found a playlist of 10,000 songs on Spotify from Alex Marty (https://open.spotify.com/playlist/6FKDzNYZ8IW1pvYVF4zUN2). After running each algorithm 100 times, I found the following results.  


To go to the notebook for this process, click here *insert book url*
Not only did it take the first algorithm, on average, 48x longer than that of the second algorithm, but it also had 15.8% less songs in it. This showed not only what algorithm was faster, but also which algorithm was asymptoticly less complex given the large factor of difference.

## Final Results and Future Work

After figuring out a more efficient algorithm, I finally produced a harmonic set from my house music playlist. I manually added the resulting songs to a new playlist. Myself and others listened to the new playlist during a night with a crossfade between songs and we all agreed it sounded very natural and not choppy. Success!

Data visuals were also produced to show the danceability, energy, and loudness across the set that was produced

One idea I have to expand functionality is to have the algorithm run several times and then having the user pick the set with the preferred energy or danceability distribution. Another idea would be including the option for multiple playlists for the algorithm to pick from that would increase the variety of sets possible. Finally, having a constraint on the amount of songs for the set would allow the user to taylor the length of the set. Thank you for time and please explore and reach out if you have any comments on this project. Below I will describe what is needed for you to reproduce this with your own playlist.

Using this On Your Own Spotify Playlist
Need: 
A Spotify account
Spotify client credentials: Client ID, Client Secret, User ID, and Playlist ID
