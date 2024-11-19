import datetime

def decorator (Old_f):
    def new_f(*args,**kwargs):
        start = datetime.datetime.now() #время начала
        result = Old_f(*args,**kwargs)
        end = datetime.datetime.now() #время окончания
        work_time = end - start
        print(f'Функция {Old_f} работала {work_time}')
        return result
    return new_f