# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from prlmro.processors import  ParseDate
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags



class SenatorItem(scrapy.Item):
    nume     			= scrapy.Field()
    url      			= scrapy.Field()
    data_nastere    	= scrapy.Field()
    data_deces			= scrapy.Field()
    data_stop_mdt		= scrapy.Field()
    motiv_stop_mdt		= scrapy.Field()
    circ				= scrapy.Field()
    circ_colegiu		= scrapy.Field()
    circ_nr				= scrapy.Field()
    rol    				= scrapy.Field()
    
    fmt_politica		= scrapy.Field()
    grp_parlamentar		= scrapy.Field()
    comisii_permanente 	= scrapy.Field()
    comisii_speciale	= scrapy.Field()
    
    activitate_politica	= scrapy.Field()
    studii				= scrapy.Field()
    pass
 
def remove_new_line(x):
	if x != None:
		return x.replace('\n', '').replace('\r','')
	return x

def strip_line(x):
	if x != None:
		return x.strip()
	return x
 
def remove_xa0(x):
	return x.replace(u'\xa0', u' ') 
 
def remove_td_dash(x, sep=' '):
	return x.replace('<td>-</td>',sep)
	
def normalize_fmt_pollitica(x):
	x = x.replace(u' - din','#since').replace(u' - până în','#until')
	lst = x.split('#')
	map = dict([])
	
	for idx, itm in enumerate(lst):
		if idx == 0:
			map['formatiune'] = lst[idx]		
		else:
			if itm.find(u'since') >= 0:
				map['since']  = itm.replace('since','').strip()
			if itm.find(u'until') >= 0:
				map['until']  = itm.replace('until','').strip()
	return map

def get_act_politica_item(tip, cols, nbs):
	map = dict([])
	map['tip'] = tip
	for idx, col in enumerate(cols):
		if len(nbs) > idx:
			map[col] = nbs[idx] 
	return map
	
def normalize_act_politica(x):
	if x == '' or x == None:
		return None
	
	fields = x.split(':')
	if len(fields) > 1:
		nbs = [s for s in fields[1].split() if s.isdigit()]
	
	if fields[0] == u'Luări de cuvânt':
		return get_act_politica_item('luari_de_cuvant', ['nr', 'sedinte'], nbs)
	if fields[0] == u'Declaraţii politice':
		return get_act_politica_item('declaratii_politice', ['nr', 'consemnate'], nbs)
	if fields[0] == u'Luări de cuvânt în BP':
		return get_act_politica_item('luari_de_cuvant_bp', ['nr', 'sedinte'], nbs)
	if fields[0] == u'Propuneri legislative initiate':
		return get_act_politica_item('propuneri_legislative', ['nr', 'promulgate_legi'], nbs)
	if fields[0] == u'Întrebari şi interpelari':
		return get_act_politica_item('intrebari_interpelari', ['nr'], nbs)
	if fields[0] == u'Motiuni':
		return get_act_politica_item('motiuni', ['nr'], nbs)
		
		
		
	print x	
	
	return None

def htmllist_to_array(x):
	x = x.replace('<ul>','').replace('</ul>','').replace('</li>','').replace('<li>','',1)
	return x.strip().split('<li>')
	
def normalize_studii(x):
	print x
	return x	
	
def normalize_grp_parlamentar(x):
	x = x.replace(u' - din','#since').replace(u' - până în','#until')
	lst = x.split('#')
	map = dict([])
	
	
	for idx, itm in enumerate(lst):
		if idx == 0:
			map['grup'] = lst[idx].strip()		
		else:
			if itm.find(u'since') >= 0:
				map['since']  = itm.replace('since','').strip()
			if itm.find(u'until') >= 0:
				map['until']  = itm.replace('until','').strip()
	return map
    
class SenatorLoader(ItemLoader):
	nume_out = Join()
	data_nastere_out = ParseDate()
	rol_out = Join()
	url_out = Join()
	circ_out = Join()
	circ_colegiu_out = Join()
	circ_nr_out = Join()
	data_stop_mdt_out = ParseDate()
	motiv_stop_mdt_out =  Join()
	
	fmt_politica_in = MapCompose(remove_xa0,
				remove_new_line, 
				remove_td_dash, 
				remove_tags,
				strip_line,
				normalize_fmt_pollitica)
	
	grp_parlamentar_in = MapCompose(remove_xa0,
				remove_new_line,
				remove_tags,
				strip_line,
				normalize_grp_parlamentar)
	
	
	comisii_permanente_in = MapCompose(remove_xa0,
				remove_new_line,
				remove_tags,
				strip_line)

	comisii_speciale_in = MapCompose(remove_xa0,
				remove_new_line,
				remove_tags,
				strip_line)
	
	activitate_politica_in = MapCompose(remove_xa0,
				remove_new_line,
				remove_tags,
				strip_line,
				normalize_act_politica)
				
	studii_in =  MapCompose(remove_xa0,
				remove_new_line,
				htmllist_to_array,
				normalize_studii)
	
	pass