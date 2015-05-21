import os, sys, urllib2
from pprint import pprint as pp
from BeautifulSoup import BeautifulSoup

print "\n"*30

soup = BeautifulSoup(open("got.html"))
person_list = []
class Person(object):
    def __init__(self, first, last=None, middle=None, nickname=None, relation=None, title=None, location=None, culture=None):
        self.first = first
        self.last = last
        self.middle = middle
        self.nickname = nickname
        self.relation = relation
        self.title = title
        self.location = location
        self.culture = culture


def return_weird_title(name_list):
    if u"of" in name_list:
        record_the_rest_of_name = False
        weird_title_list = []
        for item in name_list:
            if item == u"of":
                record_the_rest_of_name = True
            if record_the_rest_of_name == True:
                weird_title_list.append(str(item))
        if weird_title_list:
            weird_title = " ".join(weird_title_list)
    elif u"the" in name_list:
        record_the_rest_of_name = False
        weird_title_list = []
        for item in name_list:
            if item == u"the":
                record_the_rest_of_name = True
            if record_the_rest_of_name == True:
                weird_title_list.append(str(item))
        if weird_title_list:
            weird_title = " ".join(weird_title_list)
    else:
        print "WOAH: this shit is fucked:" + name_list
    return weird_title


def get_nickname(html_string_after_name_anchor):
    if 'called "' in str(html_string_after_name_anchor):
        split_string = html_string_after_name_anchor.split('called "')
        nickname_string_with_extra_text = split_string[1]
        nickname = nickname_string_with_extra_text.split('"')[0]
        return nickname

for name_list in soup.findAll(id='mw-content-text'):
    unordered_list_list = name_list.findAll('ul')
    #print unordered_list_list
    for unordered_list in unordered_list_list:
        list_item_list = unordered_list.findAll('li')
        #print list_item_list.prettify()
        for list_item in list_item_list:
            person = None
            full_name = None
            nickname = None
            title = None
            middle_name = None
            relation = None
            giant = False
            anchors = list_item.findAll('a')
            if not anchors:
                continue
            first_anchor = anchors[0]
            full_name = first_anchor.get("title")
            #print list_item
            if len(list_item.contents) >= 3:
                nickname_string = str(list_item.contents[2])
                nickname = get_nickname(nickname_string)
                if (nickname != None) and (nickname != "None"):
                    if nickname[-1] in [',','.']:
                        nickname = nickname[:-1]
            if "(" in full_name:
                name_split = full_name.split("(")
                full_name = name_split[0][:-1]
                relation = name_split[1][:-1]
                #print full_name, "|", relation
            if " " not in full_name:
                name_list = [full_name]
            else:
                name_list = full_name.split(" ")
            #print name_list
            if u"of" in name_list:
                title = return_weird_title(name_list)
                position = name_list.index(u"of")
                name_list = name_list[:position]
                #print "-" * 30
            elif u"the" in name_list:
                title = return_weird_title(name_list)
                position = name_list.index(u"the")
                name_list = name_list[:position]
                #print "-" * 30
                #print full_name, position
            elif [i for i in name_list if i in [u"I", u"II", u"III", u"IV", u"V", u"VI", u"VII", u"VIII", u"IX", u"X", u"XI", u"XII", u"XIII", u"XIV", u"XV", u"XVI", u"XVII", u"XVIII", u"XIX", u"XX"]]:
                title = [i for i in name_list if i in [u"I", u"II", u"III", u"IV", u"V", u"VI", u"VII", u"VIII", u"IX", u"X", u"XI", u"XII", u"XIII", u"XIV", u"XV", u"XVI", u"XVII", u"XVIII", u"XIX", u"XX"]][0]
                position = name_list.index(title)
                name_list.pop(position)
                #print name_list, "the", title + "th of his name"
                #print "-" * 30
            elif [i for i in [u"Old", u"Young", u"Sleepy", u"Small", u"Sour", u"Spotted", u"Mad", u"Iron", u"Fearless", u"Elder", u"Lord", u"Yellow", u"Blue", u"Black"] if i in name_list]:
                position = name_list.index([i for i in [u"Old", u"Young", u"Sleepy", u"Small", u"Sour", u"Spotted", u"Mad", u"Iron", u"Fearless", u"Elder", u"Lord", u"Yellow", u"Blue", u"Black"] if i in name_list][0])
                title = name_list[position]
                name_list.pop(position)
                #print "-" * 30
            elif u"Left" == name_list[0] and u"Hand" == name_list[1]:
                title = name_list[0] + u" " + name_list[1]
                name_list.pop(0)
                name_list.pop(0)
            elif (u"Wife" in name_list) or (u"House" == name_list[0]) or (u"Waif" == name_list[0]) or (u"Easy" == name_list[0]) or (u"Rat" == name_list[0]):
                #print "-" * 30
                pass
            elif [i for i in [u"zo", u"mo", u"na"] if i in name_list]:
                position = name_list.index([i for i in [u"zo", u"mo", u"na"] if i in name_list][0])
                title = name_list[position]
                name_list.pop(position)
                if len(name_list) != 2:
                    print len(name_list), ":", name_list
            elif len(name_list) > 2:
                if name_list[1] in [u"White", u"Red", u"Silver"]:
                    continue
                if len(name_list) == 3:
                    middle_name = name_list[1]
                    name_list.pop(1)
                else:
                    giant = True
                #pass
            if giant:
                for name in full_name.split(" "):
                    person = Person(name)
                    #print 'GIANT:', person.first
                    person_list.append(person)
            else:
                if len(name_list) > 2:
                    print 'SOMETHING FUCKED UP:', name_list
                if len(name_list) == 1:
                    person = Person(name_list[0],
                                    middle = middle_name,
                                    nickname = nickname,
                                    relation = relation,
                                    title = title)
                else:
                    person = Person(name_list[0],
                                    last = name_list[1],
                                    middle = middle_name,
                                    nickname = nickname,
                                    relation = relation,
                                    title = title)
                    person_list.append(person)



#person_list = sorted(person_list, key = lambda x: (x[1], x[2]))

for person in person_list:
    if not person.last:
        print person.first + ":"
    else:
        print person.first, person.last + ":"
    for attribute in dir(person):
        if not attribute.startswith("__"):
            if getattr(person, attribute):

                print "\t", attribute+":", getattr(person, attribute)
    print "\n"













