import argparse
import os
import random
import django
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
                        help='Please type name and surname',
                        )
    parser.add_argument('-s',
                        '--subject',
                        action='store',
                        help='Subject for commendation'
                        )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    input_schoolkid_subject = parse_user_input()
    schoolkid_surname_name = input_schoolkid_subject.schoolkid_surname_name
    try:
        schoolkid = find_schoolkid(schoolkid_surname_name)
        fix_marks(schoolkid)
        print('Ученик найден')
        print('Оценки исправлены')
        remove_chastisements(schoolkid)
        print('Замечания удалены')
        try:
            if input_schoolkid_subject.subject:
                subject = input_schoolkid_subject.subject
                create_commendation(schoolkid,
                                    find_subject(subject,
                                                 schoolkid,
                                                 ),
                                    )
            print('Благодарность присвоена')
        except Subject.DoesNotExist:
            print('Предмет не найден. Пожалуйста проверьте название предмета.'
                  'Название предмета {subject} некорректно. Для поиска необходимо'
                  'использовать корректное название.'.format(subject=subject),
                  )
        except Subject.MultipleObjectsReturned:
            print('Найдено несколько предметов по данному запросу.'
                  'Пожалуйста проверьте название предмета. Название'
                  'предмета {subject} некорректно. Для поиска необходимо '
                  'использовать корректное название.'.format(subject=subject),
                  )
    except Schoolkid.DoesNotExist:
        print('Ученик не найден. '
              'Пожалуйста проверьте имя ученика. Имя {schoolkid} некорректно. '
              'Для поиска необходимо использовать как имя, '
              'так и фамилию ученика.'.format(schoolkid=schoolkid_surname_name),
              )
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников по данному запросу. '
              'Пожалуйста проверьте имя ученика. Имя {schoolkid} некорректно.'
              'Для поиска необходимо использовать как имя, так и фамилию'
              'ученика.'.format(schoolkid=schoolkid_surname_name),
              )
