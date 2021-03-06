MASTERMIND/gladiator.py

This is an adaptation of my mastermind project to the praetorian challenge.

Unfortunately, those sneaky praetorians added a level (level 4) that blows up the "dontbedumb" guess generation runtime.  Looking at the runtime analysis I did previously for the mastermind project strongly implies that 6 slots and 25 colors won't be cracked by my dontbedumb algo for a very, very long time.  Certainly not within the 10 seconds that the praetorian API allows between guesses.

As a pathetic ditch attempt, when the time gets to 9.5 seconds after my last guess, I guess either a random guess or the guess that I was currently checking to see if it was dumb.  This, of course, also has very little realistic chance of working.  But now instead of failing by timing out, I fail by exhausing my allowed number of guesses.  Small victories.

The other pathetic ditch attempt was to run this algo on a server, which has 16 cores instead of 4 (with hyperthreading).  This dramatically sped up my shadowcrack project from earlier this year.

This is also unlikely to work.  What I really need is a guess generation algorithm that does something smarter to generate its candidate guesses than naively brute force checking all possible guesses and discarding the "dumb" ones.  For starters, this would involve recognizing when a previous guess had a result of 0 correct colors and then never even considering those colors when generating candidate guesses.  This would exponentially reduce the the candidate guesses that dontbedumb has to check.  

I'd have to put some time into figuring out what this new guess generation algorithm should be so I'm going to put a pin in the project here. 

Well I got lucky, got my hash, hope it doesn't expire, but I can always do the same thing again if I have to

ripped through the later rounds with just a couple code modifications to handle it afterwards.  

Was planning on trying to generate guesses faster with threading-- that would still be a nice upgrade so you don't have to do my terrible hack of repeating it over and over and getting it ~1/25 times.



ROTA
algo: 
(legal moves)
forced moves
non-blunder moves
move out of center but not to single spaces-- only to doubled spaces
don't move to middle
pick randomly

(There may be another trap situation-- "move towards gravity" -- but I'll start with the rules above and analyze why I lose.

Important to have a good way to represent the game that you can easily understand when analyzing why your strategy is failing.

Currently a WIP; rota.py plays a drawing strategy that I *think* works but still hasn't been battle tested and can't be until I get the interface with the API set up and start playing games.
