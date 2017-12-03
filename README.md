praetorian project copied from mastermind project.

This is an adaptation of my mastermind project to the praetorian challenge.

Unfortunately, those sneaky praetorians added a level (level 4) that blows up the "dontbedumb" runtime.  Looking at the runtime analysis I did previously for the mastermind project strongly implies that 6 slots and 25 colors won't be cracked by my algo for a very, very long time.  Certainly not within the 10 seconds that the praetorian API allows between guesses.

As a pathetic ditch attempt, when the time gets to 9.5 seconds after my last guess, I guess either a random guess or the guess that I was currently checking to see if it was dumb.  This, of course, also has very little realistic chance of working.  But now instead of failing by timing out, I fail by exhausing my allowed number of guesses.  Hooray!

The other pathetic ditch attempt was to run this algo on a server, which has 16 cores instead of 4 (with hyperthreading).  This dramatically sped up my shadowcrack project from earlier this year.

This is also unlikely to work.  What I really need is a guess generation algorithm that isn't naively brute force check all guesses.  For starters, this would involve recognizing when a previous guess had a result of 0 correct colors and then never even considering those colors again.  This would exponentially reduce the the candidate guesses that dontbedumb has to check.  

I'd have to put some time into figuring out what this new guess generation algorithm should be so I'm going to put a pin in the project here. 

