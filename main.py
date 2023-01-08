import smtplib
import ssl
from email.message import EmailMessage
import feedparser
import sqlite3
import time
from datetime import datetime
# change tthis to your email
reciever='faisalrasheed442@gmail.com'
# change this time to you value after how many seconeds it  will run like 60 seconed for 1 minutes 
send_time=60

# database connection settings
con = sqlite3.connect('data.db')
cur = con.cursor()

# clean database
clean_time=int(datetime.now().strftime("%H"))+12
#previous feed 
current_feed=[]

# change this url to your rss feed url
url=[{'name':'Python jobs for scraping', 'url':'https://www.upwork.com/ab/feed/jobs/rss?q=python+scraping&sort=recency&proposals=0-4%2C5-9&verified_payment_only=1&paging=0%3B10&api_params=1&securityToken=7356303bdc0190b07ea138bee256831e139dbac0e8c79e4cc3604d50bf1c3409e78700b2396149c6faa724a6dfba86430f25a0cee6afa6dac1cd49edd27e95f8&userUid=1427714294628659200&orgUid=1427714294628659201'},
    {'name': 'Web development job pytthon','url':'https://www.upwork.com/ab/feed/jobs/rss?q=python+script&sort=recency&proposals=0-4%2C5-9&verified_payment_only=1&paging=0%3B10&api_params=1&securityToken=7356303bdc0190b07ea138bee256831e139dbac0e8c79e4cc3604d50bf1c3409e78700b2396149c6faa724a6dfba86430f25a0cee6afa6dac1cd49edd27e95f8&userUid=1427714294628659200&orgUid=1427714294628659201'},
]

def send_email(subject,message,reciever):
    

    # Define email sender and receiver
    email_sender = 'rssfeed@techwithflash.net'
    email_password = 'a933JYaXgH1d'

    
    email_receiver = reciever

    # Set the subject and body of the email
    subject = subject
    body = message

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('mail.techwithflash.net', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


while True:
    try:
        if int(datetime.now().strftime("%M"))==clean_time:
            cur.execute("DELETE FROM info")
            con.commit()
            clean_time=int(datetime.now().strftime("%H"))+12
        for feed_pars in url:
            # setting url and jobs name 
            subject = feed_pars['name']
            url=feed_pars['url']
            f=feedparser.parse(url)

            # getting all result in from rss feed
            for x in range(len(f)): 
                # getting title of job and link and discription
                title=f.entries[x]['title']
                link=f.entries[x]['link']
                sum=f.entries[x]['summary']
                # removing httmlk tages from descipotion

                words=['<br />','<b>','</b>','<a ','</a>','&amp','&rsquo','&nbsp']
                for word in words:
                    sum=sum.replace(word,' ')
                
                # after removing all httml tags now we have final version of desciption

                sum=sum.split("href")[0]
                # getiing data from ttable to match weatther the job exits in our database or not
                res = cur.execute(f"SELECT * FROM info where title='{title}'").fetchall()
                if len(res)==0:
                    cur.execute(f"INSERT INTO info VALUES('{title}')")
                    con.commit()
                    current_feed.append({"title":title,'summary':sum,'link':link})

            if len(current_feed)!=0:
                print(current_feed)
                message=""
                for msg in current_feed:
                    message=message+(f"\nTitle: {msg['title']}\nSummary: {msg['summary']}\nLink: {msg['link']}\n ")
                send_email(subject,message,reciever)
                current_feed.clear()
            time.sleep(send_time)
    except:
        pass
