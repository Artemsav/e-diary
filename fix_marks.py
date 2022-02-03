import argparse
import os
import random
import django
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid, Subject,
                               )


def find_schoolkid(schoolkid):
    kid = Schoolkid.objects.get(full_name__contains=schoolkid)
    return kid


def find_subject(subject, schoolkid):
    subject = Subject.objects.get(title=subject,
                                  year_of_study=schoolkid.year_of_study,
                                  )
    return subject


def fix_marks(schoolkid):
    marks_for_kid = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    marks_for_kid.update(points=5)


def remove_chastisements(schoolkid):
    comments = Chastisement.objects.filter(schoolkid=schoolkid)
    comments.delete()


def create_commendation(schoolkid, subject):
    commendations = ('Молодец!', 'Отлично!', 'Хорошо!',
                     'Сказано здорово – просто и ясно!',
                     'Ты меня приятно удивил!', 'Великолепно!',
                     'Прекрасно!', 'Ты меня очень обрадовал!',
                     'Ты, как всегда, точен!',
                     )
    last_lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                        group_letter=schoolkid.group_letter,
                                        subject=subject,
                                        ).last()
    Commendation.objects.create(text=random.choice(commendations),
                                created=last_lesson.date,
                                schoolkid=schoolkid,
                                subject=subject,
                                teacher=last_lesson.teacher,
                                )


def parse_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('schoolkid_surname_name',
                        nargs=2,
                        help='Please type name and surname',
                        )
    parser.add_argument('-s',
                        '--subject',
                        action='store',
                        nargs=1,
                        help='Subject for commendation'
                        )
    args = parser.parse_args()
    if args.subject and args.schoolkid_surname_name:
        user_input = dict(schoolkid=' '.join(args.schoolkid_surname_name),
                          subject=''.join(args.subject),
                          )
        return user_input
    else:
        user_input = dict(schoolkid=' '.join(args.schoolkid_surname_name))
        return user_input


if __name__ == '__main__':
    try:
        input_schoolkid_subject = parse_user_input()
        schoolkid = input_schoolkid_subject['schoolkid']
    except SystemExit:
        print('Программа завершила работу неправильно,'
              'проверьте задаваемые атрибуты',
              )
        exit()
    try:
        fix_marks(find_schoolkid(schoolkid))
        print('Ученик найден')
        print('Оценки исправлены')
        remove_chastisements(find_schoolkid(schoolkid))
        print('Замечания удалены')
    except ObjectDoesNotExist:
        print('Ученик не найден. '
              'Пожалуйста проверьте имя ученика. Имя {schoolkid} некорректно. '
              'Для поиска необходимо использовать как имя, '
              'так и фамилию ученика.'.format(schoolkid=schoolkid),
              )
    except MultipleObjectsReturned:
        print('Найдено несколько учеников по данному запросу. '
              'Пожалуйста проверьте имя ученика. Имя {schoolkid} некорректно.'
              'Для поиска необходимо использовать как имя, так и фамилию'
              'ученика.'.format(schoolkid=schoolkid),
              )
    try:
        if input_schoolkid_subject.get('subject'):
            subject = input_schoolkid_subject['subject']
            create_commendation(find_schoolkid(schoolkid),
                                find_subject(subject,
                                find_schoolkid(schoolkid),
                                             ),
                                )
            print('Благодарность присвоена')
    except ObjectDoesNotExist:
        print('Предмет не найден. Пожалуйста проверьте название предмета.'
              'Название предмета {subject} некорректно. Для поиска необходимо'
              'использовать корректное название.'.format(subject=subject),
              )
    except MultipleObjectsReturned:
        print('Найдено несколько предметов по данному запросу.'
              'Пожалуйста проверьте название предмета. Название'
              'предмета {subject} некорректно. Для поиска необходимо'
              'использовать корректное название.'.format(subject=subject),
              )
