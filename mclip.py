#! python3

#mclip.py - A milti-clipboard program
TEXT = {'agree':"""Yes. That sounds fine.""",
        'busy':"""Sorry, can we do this later this week or next week?""",
        'upsell':"""Would you consider making this a monthly donation?""",
        'regret':"""I hope you are well. Sorry we were not able to carry out your job as requested.
         Our technician experienced issues that made it difficult to fulfil your request. 
         Kindly allow our technician to do this as the first job of the day.""",
         'forward':"""I hope you are well.
         We will not be able to carry out your job tomorrow as requested. 
         Kindly ask the customer to expect us the day after. We will update you incase of any changes""",
         'sp':"""I hope you are well. Kindly note that we are fully booked for tomorrow.
         Do let me know whether it will be okay to use a service provider on your site.
         Alternatively, you could allow us to reschedule this to he day after.
         Looking forward to your response."""}

#commandline arguments
import sys, pyperclip

if len(sys.argv) < 2:
    print('Usage: python mclip.py [keyphrase] - copy phrase text')
    sys.exit()

keyphrase = sys.argv[1] #First command line argument is the key phrase

if keyphrase in TEXT:
    pyperclip.copy(TEXT[keyphrase])
    print(f'Text for {keyphrase} copied to clipboard')
else:
    print(f'There is no content for {keyphrase}')