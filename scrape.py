#! /usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from datetime import timezone

def get_event_video_url(url: str) -> str:
    global driver
    driver.get(url)
    xp="//*[contains(@src, 'player.vimeo')]"
    while True:
        sleep(1)
        try:
            vimeo = driver.find_element_by_xpath(xp)
            return vimeo.get_attribute('src')
        except:
            pass

def get_events():
    global driver
    xpath = "//*[contains(@href, '/event/risc-v-summit/planning/')]"
    results = driver.find_elements_by_xpath(xpath)
    ret = []
    for r in results:
        link = r.get_attribute('href')
        r.find_element_by_tag_name('h3')
        val = split_description(r.text)
        val['link'] = link
        ret.append(val)
    return ret

def get_all_videos(events):
    global driver
    for ev in events:
        url = get_event_video_url(ev['link'])
        ev['url'] = url

eventday=1
def split_description(descr: str):
    topics = [ 'Community Ecosystem',
               'Hardware Cores/SoCs',
               'Keynote Program',
               'Meet the Speakers: Room A',
               'Meet the Speakers: Room B',
               'Security & Functional Safety',
               'Software & Tools',
               'System Architectures',
               'Tech Talk',
               'Verification'
             ]
    kinds = [ 'Conference',
              'Keynote',
              'Meet the Speakers',
              'Tech Talk',
              'Tutorial' ]

    global eventday
    l = descr.split('\n')
    d = {}

    dt1 = datetime.strptime(l[0], '%I:%M %p')
    dt2 = datetime.strptime(l[1], '%I:%M %p')
    if dt2 > dt1:
        dt1 = dt1.replace(year=2020,month=12,day=8+eventday-1)
        dt2 = dt2.replace(year=2020,month=12,day=8+eventday-1)
    else:
        dt1 = dt1.replace(year=2020,month=12,day=8+eventday-1)
        dt2 = dt2.replace(year=2020,month=12,day=8+eventday-1+1)


    dt1 = dt1.astimezone(timezone.utc)
    dt2 = dt2.astimezone(timezone.utc)
    d['utcstarttime'] = dt1
    d['utcendtime'] = dt2

    i = 2
    d['title'] = l[i]

    i = 3
    if l[i] in topics or l[i] in kinds:
        d['description'] = None
    else:
        d['description'] = l[i]
        i = i+1

    if l[i] in topics:
        d['topic'] = l[i]
        i = i+1
    else:
        d['topic'] = None

    if l[i] in kinds:
        d['kind'] = l[i]
        i = i+1
    else:
        d['kind'] = None

    if '·' in l[i]:
        d['presenter'] = l[i]
        i = i+1
    else:
        d['presenter'] = None

    if not len(l) >= i:
        d['organization'] = l[i]
        i = i+1
    else:
        d['organization']  = None

    if not len(l) >= i:
        print(len(l) - i, "remaining items for topic", d['topic'])

    return d

def rewrite_description(events):

    for ev in events:
        d = split_description(ev['description'])
        ev['utcstarttime'] = d['utcstarttime']
        ev['utcendtime'] = d['utcendtime']
        ev['title'] = d['title']
        ev['description'] = d['description']
        ev['topic'] = d['topic']
        ev['kind'] = d['kind']
        ev['presenter'] = d['presenter']
        ev['organization'] = d['organization']

import json
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return super().default(o)

def rewrite():
    global eventday
    for d in range(1,5):
        x = 'day0'+str(d)+'/day0'+str(d)+'.json'
        print(x)

        fp = open('day0'+str(d)+'/day0'+str(d)+'.json')
        fp2 = open('day0'+str(d)+'/day0'+str(d)+'_2.json', 'w+')
        obj = json.load(fp)
        rewrite_description(obj)
        json.dump(obj, fp2, cls=DateTimeEncoder,indent=2)
        fp2.close()
        fp.close()
        eventday = eventday+1


def main():
    global driver
    driver = webdriver.Firefox()
    driver.get('https://riscvsummit.app.swapcard.com/event/risc-v-summit')

def foo():
    url = 'https://riscvsummit.app.swapcard.com/event/risc-v-summit/planning/UGxhbm5pbmdfMjc1NTc2'
    print(get_event_video_url(url))


if __name__ == '__main__':
    main()

