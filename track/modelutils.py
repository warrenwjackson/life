'''
Created on Oct 12, 2012

@author: Warren.Jackson
'''
from django.contrib.auth.models import User
import models

def user_exists(email):
    user_count = User.objects.filter(email=email).count()
    if user_count == 0:
        return False
    return True

def record_day(user, day, happiness, work, case, content):
    create_or_update(models.Day, {'user':user, 'day':day}, {'happiness':happiness, 'work':work, 'case':case, 'content':content})
#    day = models.Day(user=user, day=day, happiness=happiness, work=work, case=case, content=content)
#    day.save()
def create_or_update(cls, unique_fields, other_fields):
    q = cls.objects.filter(**unique_fields)
    if q.count() == 0:
        print 'Creating day'
        obj = cls(**dict(unique_fields, **other_fields))
    else:
        print 'updating day    '
        obj = q[0]
        for k, v in other_fields.iteritems():
            obj.__setattr__(k, v)
    obj.save()

def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return user

def user_history(user):
    days_query = user.day_set.all().values('day', 'happiness', 'work')
    days = []
    happiness = []
    work = []
    for record in days_query:
        days.append(record['day'].strftime("%b %d, %Y"))
        happiness.append(record['happiness'])
        work.append(record['work'])
    days_dict = {'days':days, 'happiness':happiness, 'work':work}
#    print days_dict
    return days_dict
    