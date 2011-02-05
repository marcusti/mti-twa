#-*- coding: utf-8 -*-

from datetime import date
from members.csvutf8 import UnicodeReader, UnicodeWriter
from operator import itemgetter
import os, sys
from import_members import convert_date, add_graduation
from members.models import Country, Dojo, Graduation, Person

def import_members():
    filename = 'data-it.csv'
    if not os.path.exists(filename) or not os.path.isfile(filename):
        print 'exit. file does not exist: %s' % filename
        sys.exit(2)

    print 'deleting italian members'
    for p in Person.objects.filter(country__code='IT'):
        for g in Graduation.objects.filter(person=p):
            g.delete()
        p.delete()

    header = None

    print 'reading file %s' % filename
    with open(filename) as f:
        for i, line in enumerate(UnicodeReader(f)):
            if i == 0:
                header = line
            else:
                dojo_name = line[header.index('DOJO')].title().strip()
                lastname = line[header.index('LASTNAME')].title().strip()
                firstname = line[header.index('FIRSTNAME')].title().strip()
                street = line[header.index('STREET')].title().strip()
                zipp = line[header.index('ZIP')].strip()
                city = line[header.index('CITY')].title().strip()
                countrycode = line[header.index('COUNTRY')].strip()
                birth = line[header.index('BIRTH')].strip()
                gender = line[header.index('GENDER')].strip()
                phone = line[header.index('PHONE')].strip()
                email = line[header.index('EMAIL')].strip()
                rank_string = line[header.index('RANK')].strip()

                print firstname, lastname, street, city

                try:
                    # try to find a person by name
                    person = Person.objects.get(firstname=firstname, lastname=lastname)
                    print 'person found by name: id=%s, %s' % (person.id, person)
                except:
                    person = Person(firstname=firstname, lastname=lastname)

                try:
                    country = Country.objects.get(code=countrycode)
                except:
                    country = Country(name='Italy', name_de='Italien', name_ja='イタリア', code='IT')
                    country.save()

                person.street = street
                person.zip = zipp
                person.city = city
                person.country = country
                person.birth = convert_date(birth)
                person.phone = phone
                person.email = email
                person.gender = gender

                person.save()

                try:
                    dojo = Dojo.dojos.get(name=dojo_name)
                except:
                    dojo = Dojo(name=dojo_name)
                    if country:
                        dojo.country = country
                    dojo.save()
                    print 'dojo created: %s, %s' % (dojo.id, dojo.name)

                if not dojo in person.dojos.all():
                    person.dojos.add(dojo)
                    print '%s added to dojo %s' % (person, dojo)

                GRAD_MAPPING = {
                    '6 kyu': 9,
                    '5 kyu': 10,
                    '4 kyu': 20,
                    '3 kyu': 30,
                    '2 kyu': 40,
                    '1 kyu': 50,
                    '1 dan': 100,
                    '2 dan': 200,
                    '3 dan': 300,
                    '4 dan': 400,
                }

                grad = Graduation(rank=GRAD_MAPPING.get(rank_string, None), person=person, date=date(2011, 1, 1))
                grad.save()
                print 'graduation created: %s, %s' % (person, grad)

                person.save()
