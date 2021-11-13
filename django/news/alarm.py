import os
from abc import ABCMeta, abstractmethod

class NewsPublisher:
    def __init__(self):
        self.__alarm_types = []  # attach, detach 를 통해 디비랑 연동
        self.__latestNews = []
    
    def attach(self, alarm_type):
        self.__alarm_types.append(alarm_type)  
        # 디비에 넣자
    
    def detach(self):
        return self.__alarm_types.pop()  
        # 디비에서 삭제하자
    
    def notifyAlarms(self):
        for alarm in self.__alarm_types:
            alarm.update()
    
    def addNews(self, alerted_articles):
        self.__latestNews = alerted_articles  # 기업이름도 같이 넘어와야해
    
    def getNews(self):
        return self.__latestNews


class Alarm(metaclass=ABCMeta):
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)
    
    @abstractmethod
    def update(self):
        pass


class SMSAlarm(Alarm):   
    def update(self):
        articles = self.publisher.getNews()
        
        from twilio.rest import Client

        account_sid = os.getenv("ACCOUNT_SID")
        auth_token = os.getenv("AUTH_TOKEN")
        from_ = os.getenv("PHONE")

        # 해당 기업과 SMS알람 선택자를 DB에서 찾아 to_lst 에 넣는다.
        to_lst = [os.environ.get('to_phone')]
        client = Client(account_sid, auth_token)

        for article in articles:
            for to in to_lst:
                url = article.get('link', '')
                title = article.get('title', '')
                body = f'{title}\n{url}'
                msg = client.messages.create(to, from_=from_, body=body)


class EmailAlarm(Alarm):        
    def update(self):
        articles = self.publisher.getNews()

        import smtplib
        from email.mime.text import MIMEText

        id = os.environ.get("ID")
        pw = os.environ.get("PASSWORD2")
        from_ = id + "@gmail.com"
        sess = smtplib.SMTP("smtp.gmail.com", 587)
        sess.starttls()
        sess.login(id, pw)
        
        # 해당 기업과 이메일알람 선택자를 DB에서 찾아 to_lst 에 넣는다.
        to_lst = [os.environ.get('to_email')]
        
        for article in articles:
            msg = MIMEText(article.get('link', ''))
            msg["Subject"] = '[기업뉴스]' + article.get('title', '')

            for to in to_lst:
                sess.sendmail(from_, to, msg.as_string())
            sess.quit()


news_publisher = NewsPublisher()
SMSAlarm(news_publisher)
EmailAlarm(news_publisher)