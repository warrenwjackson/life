import datetime
import random
import modelutils

def fake_history(user, day_count):
    today = datetime.date.today()
    for i in range(day_count):
        modelutils.record_day(user, day=today-datetime.timedelta(i), happiness=random.randint(0,100), work=random.randint(8,20), case="", content="")



