# Interview structure

- Take home problem (est 40 mins) -> 1 hour onsite (est 50 mins for the onsite problem itself)

- I benchmarked the time to completion against myself (`onsite/computer_strategy.py` is actually what I could come up with in 50 mins)

# Some thoughts on using games as interview questions

## 1. Leetcode isn't the best differentiator 

A lot of people don't like Leetcode for various reasons, but pragmatically, this point applies when I was recruiting because most of the good candidates coming out of UWaterloo can comfortably do medium+ problems, and using hard problems imo tests more recall than problem solving.

It's really hard to correctly evaluate problem solving skills because people can rote-memorize Leetcode problems (or worse, cheat with AI https://www.interviewcoder.co/). And at a series A startup every time we had a bad hire it was very costly in time and resources because every individual person was a big part of a small team, so it was quite an existential need to get the technical hiring right. 

## 2. Non-leetcode alternatives have trade-offs

When interviews try to move away from Leetcode and simulate "real world coding", they tend to limit how difficult the problem can be without introducing any "fun" into the interview process. This is because:

### a. Leetcode is simple:

A Leetcode problem is usually an array/tree/graph of input that you need to mutate and return some kind of output. The solution can be difficult, but the input/output and problem description is usually very intuitive.

When interviewers try to inject more "real world skills" into the problems, they're introducing contexts that might not be intuitive for the interviewee, so they need to decrease the difficulty. 

I'm going to take a Ramp onsite problem as an example. They want to test some basic network knowledge, so they reframe a graph traversal problem into a puzzle. Something like:

"Given a starting URL `ramp_interview.com/0` that when visited returns a list of URLs `[ramp_interview.com/322, ramp_interview.com/yellow]`, find the URL that returns `success`" 

It's definitely more interesting than a normal graph traversal problem, and Ramp attempt to test for real world knowledge by hiding easter eggs in network response headers that you need to notice, or fail requests with 5XX so you need to retry a few times before the call passes. 

But the practical result is that the candidate needs too much hand holding and it starts to defeat the purpose of the interview. If the interviewee starts getting 5XX requests they'll usually just ask if the service is down and then the interviewer has to guide them towards the intended interview question which is "how do you handle 5XX requests here".

### b. Leetcode has a very clear measurement of correctness: 

You either pass the test cases or you don't. You either get `O(n log n)` or you get `O(n)` for performance and one is objectively better.

Judging candidates by other things like OOP-standards or code cleanliness or how well they prompt Cursor tends to be very subjective and it's very hard to implement a rubric that ensures consistency across different interviewers in a large company.

This is another reason why even though companies don't want to do Leetcode problems, it's hard to make problems that aren't just Leetcode with a little bit of seasoning sprinkled on top.

## 3. Games are surprisingly good interview problems

### a. Games are usually simple

Tic-tac-toe in this case is so intuitive that I never found myself needing to explain the rules in all the interviews.

Another bonus is that the take home problem somewhat preps the interviewee for the onsite without them knowing it, so no-one is ever completely taken aback and not know how to start, unless they cheated and not write the take-home code themselves (which becomes very obvious when you compare the take-home and on-site performance).

### b. Games have a clear measure of success

In a game, you either win, lose or tie. In the starter code there is a simulator that's basically a wrapper for 10 test cases.

The interesting part is that the testing is adaptive (there's another strategy playing against yours), and interviewees can also reason about what they want to optimize for. Should they write an algorithm that loses once but wins nine times or should they write an algorithm that at least always ties. It's very open ended to their personal interpretation of what's a "good" algorithm.

### c. Bonus point 1: Writing games naturally test real-world coding knowledge

My personal opinion is that experience is most visible when candidates try to fix problems. All of the engineers that I look up to are really fast at pinpointing issues and debugging simply because they've had so much experience fixing issues in their career and they move so natural across all the different areas of code. I think how people navigate their IDE and place debuggers or print statements is a much better judge of experience than their resume.

Open-ended games like this don't usually have an optimal solution on the first try so it naturally nudges the candidates towards reading/tweaking the starter code and debugging their own logic. I think it's a much more enjoyable process than the "I have 10 bugs in this code you should find them" type of interview because we don't need to introduce additional contexts or force our way into a "real world coding experience", we just let it happen naturally and people debug their own mistakes and optimize their own code.

### d. Bonus point 2: It tests culture fit. 

I had a lot of fun making the interview problem and when people have fun trying to solve it, it's a really strong indicator of culture fit and we end up working really well together if they get the job.

### e. Bonus point 3: AI usually really struggles in these problems. 

They can probably one-shot the take-home problem now but I think the onsite problem is still really hard. 

# Sample submissions

+ There are sample submissions for both the take home and the onsite which benchmark the top ~30-ish% of what can be done by an applicant in the allotted time.

+ Really cracked candidates usually tend to completely exceed expectations. I interviewed a candidate that just wrote minimax algorithm off the top of his head without Googling anything and it was an immediate strong hire decision.

# Future improvements

## Leveling 

These problems were originally meant for new hire/mid-level ICs. I think it's not sufficient for senior and above without more interview rounds, and there's probably work to be done to even tweak the problems.

## Language

Note that the problem is Python only. In my previous experience this isn't a big issue because we use Python in our stack and it's very intuitive to pick up as a language. I tend to be lenient on language syntax and guide candidates through those kind of hiccups.

## Take home improvements 

+ I used emails to get submissions for the take home solutions but we can automate that process by spinning up an endpoint that takes the submission number and when it's correct returns a booking link/next stage link.

+ We can also make it closer to an Online Assessment (OA) so there's less cheating and some time control. Like schedule a time to send out the interview problem and check when we get it back

## Onsite improvements

+ We can publicly host the onsite problem and make it a recurring event or challenge. We can run elo calculations by playing all the submitted strategies together and publish that leaderboard as a marketing hook. 

+ There's not a good rubric for the onsite (yet) as I was the only technical interviewer the last time I did it and there wasn't a need to relay the information I'm writing down in the README now.