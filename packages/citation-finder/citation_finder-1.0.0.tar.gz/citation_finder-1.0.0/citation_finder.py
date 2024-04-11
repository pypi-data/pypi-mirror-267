#!/usr/bin/env python
# coding: utf-8

import re
import pandas as pd
import dhlab as dh
import datetime

def findone(regex, s):
    res = re.findall(regex,s)
    try:
        r = res[0]
    except:
        r = "itj no"
    return r

#### Bygge korpus
#### corpus = dh.Corpus(doctype="digibok", subject = "språkvitenskap", limit = 1000, from_year=1950)

#### Finne konkordanser med årstall mellom 1000 og 2023


curr_year = datetime.datetime.today().year


def citation_finder(corpus, yearspan=(1000,curr_year), conc_limit=4000, get_concs=False):
    """Finds citations in text using regular expressions"""

    tall = list(range(yearspan[0],yearspan[1]))

    tallOR = ' OR '.join([str(x) for x in tall])

    tallconc = dh.Concordance(corpus, tallOR, limit=conc_limit)

    concs = tallconc.frame
    concs.concordance = concs.concordance.apply(lambda x:x.replace('<b>', '').replace('</b>', '').replace('...', ''))
    concs1 = concs[['urn', 'concordance']]

    #### Regex1
    #### finner alle konkordanser med parentes (eller semikolon) med årstall.

    regex1 = r'[\(;].*?\D\d{4}\D.*?[\);]'

    concs1['parentes'] = concs1.concordance.apply(lambda x: findone(regex1, x))

    concs2 = concs1[concs1['parentes'] != 'itj no']
    concs2 = concs2[['urn', 'concordance']]

    #### Navn i parentes
    #### Regex2
    #### finner alle konkordanser med navn, årstall og potensielt sidetall før sluttparentes (eller semikolon). Navnet kan følges av "et
    #### al." eller "m.fl.".

    regex2 = r'(?:[A-ZÀ-Ž](?:[A-zÀ-ž-]+|\s*\.)\s*,?\s*)+(?:\s*(?:et\s*al\.?|m(?:ed|\s*\.?)\s*fl(?:ei?re?|\s*\.?))\s*)?,?\s*\[?\s*\d{4}\s*[a-zæøå]?\s*\.?\s*\]?(?:\s*[,;:/\)\s]\s*(?:[PpSs]\s*\.?)?\[?\s*\d{1,4}\s*[a-zæøå]?\s*\.?\s*\]?(?:\s*[,-]\s*\d{1,4}\s*[a-zæøå]?\s*\.?)?)*\s*[\);]'

    concs2['navn i parentes'] = concs2.concordance.apply(lambda x: findone(regex2, x))

    concs3 = concs2[concs2['navn i parentes'] != 'itj no']
    concs3 = concs3[['urn', 'concordance']]

    if get_concs:
        return concs3

    #### Regex3
    #### finner alle treff i alle konkordanser som macther parenteser (eller semikolon) som består av minst én bokstav, årstall og hva som
    #### helst annet. Antakelsen er at vi allerede har filtrert på parentes-konstruksjoner som ligner på siteringer med navn, årstall og
    #### sidetall og at alle parenteser med minimum én bokstav og et årstall derfor er siteringer.

    regex3 = r'(?<=[\(;])[^(;\d]*?[A-zÀ-ž-][^(;]*?\d{4}[^);]*?(?=[\);])'

    match = []

    for i in concs3.values:
        m = re.findall(regex3, i[1])
        if m != []:
            match.append((i[0],m))

    match_df = pd.DataFrame(match)
    match_explode = match_df.explode(column=1)

    #### Navn utenfor parentes
    #### Regex4
    #### finner alle treff i alle konkordanser som macther navn utenfor parentes (eller semikolon) som består av et årstall og hva som helst
    #### annet. Navnekonstruksjonene kan bestå av flere navn etter hverandre, potensielt skilt av komma eller "og/and/&", eller etterfulgt
    #### av "et al." eller "m.fl.".

    regex4 = r'(?:(?:[A-ZÀ-Ž](?:[A-zÀ-ž-]+|\s*\.)\s*,?\s*)+(?:og|and|&)\s*)?(?:[A-ZÀ-Ž](?:[A-zÀ-ž-]+|\s*\.)\s*,?\s*)+(?:\s*(?:et\s*al\.?|m(?:ed|\s*\.?)\s*fl(?:ei?re?|\s*\.?))\s*)?\s*\(\s*\d{4}\s+(?:\)|[^-–—)][^)]*?\))'

    matchu = []

    for i in concs2.values:
        mu = re.findall(regex4, i[1])
        if mu != []:
            matchu.append((i[0],mu))

    matchu_df = pd.DataFrame(matchu)
    matchu_explode = matchu_df.explode(column=1)

    #### NOU, Stortingsmelding og Proposisjon
    #### Regex5
    #### finner alle treff i alle konkordanser som matcher NOU-er, stortingsmeldinger eller proposisjoner.

    regex5 = r'(?:(?:NOU|nou)\s*\(?\s*\d{4}\s*:\s*\d{1,4}|(?:St\s*\.?\s*)?Meld\s*\.?\s*(?:St\s*\.?\s*)?(?:nr\s*\.?\s*)?\d{1,3}\s*\(?\s*\d{4}\s*-\s*\d{4}\s*\)?|Prop\s*\.?\s*\d{1,3}\s*[A-ZÆØÅ]\s*\(?\s*\d{4}\s*-\s*\d{4}\s*\)?)(?:\s*[,(]?\s*[PpSs]\s*\.?\s*\d{1,4})?'

    matchn = []

    for i in concs1.values:
        mn = re.findall(regex5, i[1])
        if mn != []:
            matchn.append((i[0],mn))

    matchn_df = pd.DataFrame(matchn)
    matchn_explode = matchn_df.explode(column=1)

    #### match_sorted
    #### setter sammen datarammene med siteringer for navn i parentes, navn utenfor parentes og NOU-er, stortingsmeldinger og proposisjoner,
    #### og sorterer på URN.

    match_concat = pd.concat([match_explode, matchu_explode, matchn_explode], axis=0, ignore_index=True)
    match_sorted = match_concat.sort_values(by=0, ignore_index=True)

    return match_sorted
