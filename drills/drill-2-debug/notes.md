SAY: Hello, to start I'll run the tests to see where things stand. We have 6 failing with 1 pass. Seems like most of the failures are coming as assertionErrors: assertFalse which I'll keep in mind as I skim the codebase. 
SAY: Is there a file you recommend I start with? After skimming, my guess is we are working on a rate limiting system. However I'm not too sure how buckets play a role here. I want to check my guess with AI and ask about buckets. 
PROMPT: I think this is a rate limiting system focused on allowing deciding whether requests should be allowed or not, depending on the current bucket size and current requests per minute,hour, etc. List what each file is for and how buckets play a supporting role in the limiter class. Explain only, don't edit any files. 
SAY: It says this isn't really a rate limiter based off requests and time. It is a limiter that manages buckets per key. 
PROMPT: What is the exact logic that determins whether allow or deny? Is it if buckets are fill with tokens? And what is it deciding exactly? 
SAY: Ahh so it does allow or deny a specific request. Each request has a cost and the bucket needs enough tokens to cover that cost. In summary, we're building a rate limiter that accepts requests only if buckets can consume the cost of the request in tokens. 

DONE WITH CODE COMPREHENSION. 

SAY: To begin with fixing these test cases, I want to start by grouping the testcases together by root cause. My guess is the root cause is in the allow function since most test cases are failing on that assertion. 
PROMPT: Feed in assertion errors and Group them by likely root cause and tell me which to fix first. Don't fix anything yet. Are my errors occurring in the allow function? Can you include a one line docstring at the top of allow walking through the implementation of that fucntion?"
SAY: Errors are showing up in allow but the overall logic of allow is fine. To fix the first set of errors, we need to change bucket: dict = {} to not control all instances and tests using the same bucket dict. Each instance should have its own bucket dictionary. Is that correct? 
PROMPT: To fix Group A, is it correct to insantiate a bucket dictionary for each instance? 
SAY: That fixed 4 tests. The issue was that we were initializing a bucket dictionary at the start of our program as a default, but we needed to instantiate it in our constructor init(). 
SAY: For Group B of tests, int(tokens) inside the bucket.py was dropping the decimal values and resulting in the wrong amount of tokens in the calculation. By switching it to cast as a float, we account for the fractional amount, which is what test_refills_over_fractional_seconds was checking for. 
SAY: Lastly, let me look at test_refill_never_exceeds_capacity. My guess is we are not checking that capacity goes over when refilling. I will add a check there and return early if thats the case. That didn't seem to work. Let me run my guess by with AI. 
PROMPT: My guess for Group C is that we do not check if tokens goes above capacity. I added a check by calculating the refilled amount > capacity. Is this correct or does it need to be hardened? 
SAY: Ahh, the issue with my fix is that we arent updating buckets capacity at all when we refill. If refill causes refilled amount to exceed capacity, we simply want to set it to bucket's capacity, effectively setting a hard cap. We can use the min helper function for this. 
SAY: All 7 test cases passed. We had 3 errors: the buckets dict being instantiated once for all instances, fractional time being dropped by integer casting, and bucket refill causing overflow. 

DONE WITH DEBUGGING TESTS. 