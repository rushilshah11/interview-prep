SAY: Hello, can I first take some time to get accustomed to the codebase? 
PROMPT: I'm new to this repo. Give me a concise bulleted list of the key functions per class and what they do? What is each file for? What are the main objects and how do they change? 
SAY: As that loads, I will start scanning the codebase. I noticed that functions don't have a lot of comments or detail/notes on what the logic is? 
PROMPT: Can you add one line docstrings to each function, providing a brief explanation the functionality and logic? 
AFTER REVIEWING AI AND CODE, SAY: From my understanding, we're building a subscription billing system. The subscription class is the main driver with plans and invoices classes used to simple return information about a specific plan or invoice. From the AI response, it seems the main objects that change are Subscription objects as they move across the subscription lifecycle and Invoice as that states changes from open to paid. 
SAY: Before moving on, I want to run our test folder to see what is failing. Nothing is failing. seems like we are good. 


DONE. TIME 2:38 - 2:49. 


1. What does this codebase do? (2 sentences, headline first)
 - A subscription billing system that tracks plans, invoices and subscription lifecycle. 
2. What states can a subscription be in, and what moves it between them?
 - TRIAL = "trial", ACTIVE = "active", PAST_DUE = "past_due", CANCELED = "canceled"
3. Step by step, what does `renew()` change on a successful charge? On a failed one?
 - success -> paid, ACTIVE, period advanced, failed reset
4. Where does validation happen, and what happens on bad input?
 - Validation happens in subscription.py. On bad input, we raise a SubscriptionError. 
5. Name two things you'd ask the interviewer about or flag as risky.
 - Can we be more specific with error handling by using unique exceptions? We are not catching bad input in invoice or plans. 

 REVIEW DONE. TIME 2:49 - 2:53