import traceback
import StringIO
from django.db import connection
import re
import datetime
from django.contrib.auth.models import User
import models

def user_exists(email):
    user_count = User.objects.filter(email=email).count()
    if user_count == 0:
        return False
    return True

def data_dump(user):
    keys = ['happiness', 'work', 'case', 'content']
    data = user.day_set.all().order_by('day').values(*list(['day']+keys))
    output = '|'.join(['MM/DD/YY', 'happiness', 'hours_worked', 'case_code', 'worked_on_comment']) + "\n"
    for record in data:
        output += '|'.join([record['day'].strftime("%x")] + [str(record[key]) for key in keys]) + "\n"
    return output
def ingest(user, str):
    buffer = str.split("\n")
    for line in buffer[1:]:
        l = line.strip().split("|")
        if l[0] != '':
            try:
                day = datetime.datetime.strptime(l[0],"%x").date()
            except:
                return False
            if len(l) == 1 or "".join(l[1:]) == "":
                models.Day.objects.filter(user=user, day=day).delete()
            elif len(l) == 5:
                try:
                    happiness = cast_and_clean(l[1], int, 0, 100)
                    work = cast_and_clean(l[2], float, 0, 24) 
                    case = l[3][:10]
                    content = l[4][:140]
                    create_or_update(models.Day, {'user':user, 'day':day}, {'happiness':happiness, 'work':work, 'case':case, 'content':content})
                except:
                    return False
            else:
                return False
    return True
            
            
            
    #TODO: finish ingest

def cast_and_clean(str, cast, min, max):
    val = cast(str)
    assert min <= val and val <= max
    return val
            
def record_day(user, day, happiness, work, case, content):
    create_or_update(models.Day, {'user':user, 'day':day}, {'happiness':happiness, 'work':work, 'case':case, 'content':content})

def create_or_update(cls, unique_fields, other_fields):
    q = cls.objects.filter(**unique_fields)
    if q.count() == 0:
        obj = cls(**dict(unique_fields, **other_fields))
    else:
        obj = q[0]
        for k, v in other_fields.iteritems():
            obj.__setattr__(k, v)
    try:
        obj.save()
    except Exception, e:
        connection._rollback()
        raise e

def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return user

def user_history(user):
    days_query = user.day_set.all().values('day', 'happiness', 'work').order_by('day')
    days = []
    happiness = []
    work = []
    for record in days_query:
        days.append(record['day'].strftime("%b %d, %Y"))
        happiness.append(record['happiness'])
        work.append(record['work'])
    days_dict = {'days':days, 'happiness':happiness, 'work':work}
    return days_dict
    