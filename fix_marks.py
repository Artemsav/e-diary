import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from datacenter.models import Commendation, Lesson, Schoolkid, Mark, Chastisement, Subject


def find_schoolkid(schoolkid):
    kid = Schoolkid.objects.filter(full_name__contains=schoolkid)
    if len(kid)==1:
        return kid[0]
    else:
        print('Пожалуйста проверьте имя ученика. Имя {schoolkid} некорректно. Для поиска необходимо использовать как имя, так и фамилию ученика'.format(schoolkid=schoolkid))

def find_subject(subject, years=6):
    find_subject = Subject.objects.filter(title=subject, year_of_study=years)
    print(find_subject)
    if len(find_subject)==1:
        return find_subject[0]
    else:
        print('Пожалуйста проверьте название предмета. Название предмета {subject} некорректно. Для поиска необходимо использовать корректное название'.format(subject=subject))

def fix_marks(schoolkid):
    marks_for_kid = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for i in range(len(marks_for_kid)):
        marks_for_kid[i].points = 5
        marks_for_kid[i].save()

def remove_chastisements(schoolkid):
    comments = Chastisement.objects.filter(schoolkid=schoolkid)
    comments.delete()

def create_commendation(schoolkid, subject, year_of_study=6, group_letter='А'):
    Commendation_truple = ('Молодец!', 'Отлично!', 'Хорошо!', 'Сказано здорово – просто и ясно!', 'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!','Ты, как всегда, точен!')
    last_lesson = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter, subject=subject).last()
    Commendation.objects.create(text=random.choice(Commendation_truple), created=last_lesson.date, schoolkid=schoolkid, subject=subject, teacher=last_lesson.teacher)
      

if __name__ == '__main__':
    try:
        fix_marks(find_schoolkid('Фролов Иван'))
        remove_chastisements(find_schoolkid('Голубев Феофан'))
        create_commendation(find_schoolkid('Фролов Иван'), find_subject('Муsзыка'))
    except AttributeError:
        print('Программа завершила работу неправильно, проверьте задаваемые атрибуты')
