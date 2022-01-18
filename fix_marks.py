import os
import sys
import django
import random
import argparse
from argparse import ArgumentError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from datacenter.models import Commendation, Lesson, Schoolkid, Mark, Chastisement, Subject


def find_schoolkid(schoolkid):
    kid = Schoolkid.objects.filter(full_name__contains=schoolkid)
    if len(kid)==1:
        return kid[0]
    else:
        print('Пожалуйста проверьте имя ученика. Имя {schoolkid} некорректно. Для поиска необходимо использовать как имя, так и фамилию ученика'.format(schoolkid=schoolkid))

def find_subject(subject, schoolkid):
    find_subject = Subject.objects.filter(title=subject, year_of_study=schoolkid.year_of_study)
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

def create_commendation(schoolkid, subject):
    Commendation_truple = ('Молодец!', 'Отлично!', 'Хорошо!', 'Сказано здорово – просто и ясно!', 'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!','Ты, как всегда, точен!')
    last_lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter, subject=subject).last()
    Commendation.objects.create(text=random.choice(Commendation_truple), created=last_lesson.date, schoolkid=schoolkid, subject=subject, teacher=last_lesson.teacher)

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('schoolkid_surname_name', nargs=2, help = 'Please type name and surname')
    parser.add_argument('-s', '--subject', action='store', nargs=1, help = 'Subject for commendation')
    try:    
        args = parser.parse_args()
        if args.subject and args.schoolkid_surname_name:
            user_input = dict(schoolkid=' '.join(args.schoolkid_surname_name), subject = ''.join(args.subject))
            return user_input
        else:
            user_input = dict(schoolkid=' '.join(args.schoolkid_surname_name))
            return user_input
    except SystemExit:
        print('Программа завершила работу неправильно, проверьте задаваемые атрибуты, имя ученика должно содержать сначало Фамилию, затем Имя, через пробел')
         

if __name__ == '__main__':
    try:
        user_input = parser()
        fix_marks(find_schoolkid(user_input['schoolkid']))
        print('Ученик найден')
        print('Оценки исправлены')
        remove_chastisements(find_schoolkid(user_input['schoolkid']))
        print('Замечания удалены')
        if user_input.get('subject'):
            create_commendation(find_schoolkid(user_input['schoolkid']), find_subject(user_input['subject'], find_schoolkid(user_input['schoolkid'])))
            print('Благодарность присвоена')
    except AttributeError:
        print('Программа завершила работу неправильно, проверьте задаваемые атрибуты')
