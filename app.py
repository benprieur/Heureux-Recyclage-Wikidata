# -*- coding: utf-8 -*

import pywikibot
from pywikibot import pagegenerators
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

import csv, sys

'''
gen = pagegenerators.WikibaseSearchItemPageGenerator('USA', language='fr', total='1', site=site)
print(gen)
country = None
for q in gen:

    print(q.title())
    country = q.title()
    it = pywikibot.ItemPage(repo, q.title())
    item_dict = it.get()
    print(item_dict['labels']['fr'])
'''

def create_wd_item(site, label_dict):
    new_item = pywikibot.ItemPage(site)
    new_item.editLabels(labels=label_dict, summary=u"Create new element")
    return new_item.getID()

with open('liste.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in reader:

        if line_count > 7:

            isHeureux = False
            if row[0] == 'Oui':
                isHeureux = True

            nom = row[1]
            address = row[2]
            postalcode = row[3]
            citysource = row[4]
            countrysource = row[5]
            latitude = row[6]
            longitude = row[7]

            # create WD
            some_labels = {"fr": nom}
            new_item_id = create_wd_item(site, some_labels)
            print(new_item_id)

            item = pywikibot.ItemPage(repo, new_item_id)
            item.get()

            claim = pywikibot.Claim(repo, u'P31')
            target = pywikibot.ItemPage(repo, 'Q96983545')
            claim.setTarget(target)
            item.addClaim(claim, summary=u'Nature')

            latI = float(latitude)
            lonI = float(longitude)
            print(f'Lat: {latI}, lon: {lonI}')
            coordinateclaim = pywikibot.Claim(repo, u'P625')
            coordinate = pywikibot.Coordinate(lat=latI, lon=lonI, precision=0.0001, site=site)
            coordinateclaim.setTarget(coordinate)
            item.addClaim(coordinateclaim, summary=u'Coordinates')

            #P17, country
            gen = pagegenerators.WikibaseSearchItemPageGenerator(countrysource, language='fr', total='1', site=site)

            country = None
            countryprint = ''

            for q in gen:

                print(q.title())
                country = q.title()
                it = pywikibot.ItemPage(repo, q.title())
                item_dict = it.get()
                countryprint = item_dict['labels']['fr']
                print(countryprint)

            claim = pywikibot.Claim(repo, u'P17')
            target = pywikibot.ItemPage(repo, country)
            claim.setTarget(target)
            item.addClaim(claim, summary=u'Country')

            #P131, location
            gen = pagegenerators.WikibaseSearchItemPageGenerator(citysource, language='fr', total='1', site=site)

            city = None
            cityprint = ''

            for q in gen:
                print(q.title())
                city = q.title()
                it = pywikibot.ItemPage(repo, q.title())
                item_dict = it.get()
                cityprint = item_dict['labels']['fr']
                print(cityprint)

            claim = pywikibot.Claim(repo, u'P131')
            target = pywikibot.ItemPage(repo, city)
            claim.setTarget(target)
            item.addClaim(claim, summary=u'Location')

            if isHeureux == True:
                    claim = pywikibot.Claim(repo, u'P463')
                    target = pywikibot.ItemPage(repo, 'Q16651108') # Heureux Cyclage
                    claim.setTarget(target)
                    item.addClaim(claim, summary=u'Heureux Cyclage')

            description = 'atelier de réparation de cycles à ' + cityprint + ', ' + countryprint
            desc = { u'fr': description }
            item.editDescriptions(desc, summary=u'Set description')

            claim = pywikibot.Claim(repo, u'P281')
            claim.setTarget(postalcode)
            item.addClaim(claim, summary=u'Postal Code')

            claim = pywikibot.Claim(repo, u'P6375')
            addr = pywikibot.WbMonolingualText(language='fr', text=address)
            claim.setTarget(addr)
            item.addClaim(claim, summary=u'Address')

        line_count += 1
        print(line_count)