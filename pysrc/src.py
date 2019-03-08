# -*- coding: cp1252 -*-
import time
from datetime import datetime
import calendar

orologio=datetime.now()

#Ideated, made and coded by Trainax

WEEKDAY_WEIGHT = [4, 2, 1]
DAY_WEIGHT = [20, 10, 8, 4, 2, 1]
MONTH_WEIGHT = [10, 8, 4, 2, 1]
YEAR_WEIGHT = [80, 40, 20, 10, 8, 4, 2, 1]
HOUR_WEIGHT = [20, 10, 8, 4, 2, 1]
MINUTE_WEIGHT = [40, 20, 10, 8, 4, 2, 1]

global avviso_secondo_intercalare
avviso_secondo_intercalare = "00"

def generate_bit(value, weights):
    bits = ""
    for weight in weights:
        bits += str(value/weight)
        value %= weight
    return bits


def generate_weekday_bit(weekday):
    weekday += 1
    return generate_bit(weekday, WEEKDAY_WEIGHT)


def generate_day_bit(day):
    return generate_bit(day, DAY_WEIGHT)


def generate_month_bit(month):
    return generate_bit(month, MONTH_WEIGHT)


def generate_year_bit(year):
    year = int(str(year)[2:])
    return generate_bit(year, YEAR_WEIGHT)


def generate_hour_bit(hour):
    return generate_bit(hour, HOUR_WEIGHT)


def generate_minute_bit(minute):
    return generate_bit(minute, MINUTE_WEIGHT)


def is_dst(date):
    dst = time.localtime(time.mktime(date.timetuple())).tm_isdst
    return "0" if dst == 0 else "1"


def generate_first_segment(date):
    first_segment = "01" #Bit identificativi del primo segmento. NON MODIFICARE MAI!
    first_segment += generate_hour_bit(date.hour) #Aggiunta dei bit dell'ora
    first_segment += generate_minute_bit(date.minute) #Aggiunta dei bit dei minuti
    first_segment += is_dst(date) #Aggiunta del bit ora estiva\solare (0=Ora solare, 1=Ora estiva)
    first_segment +=  str((sum([int(b) for b in first_segment]) +1) % 2) #P1: Primo bit di parità del primo segmento
    first_segment += generate_month_bit(date.month) #Aggiunta del bit del mese
    first_segment += generate_day_bit(date.day) #Aggiunta bit del giorno
    first_segment += generate_weekday_bit(date.weekday()) #Aggiunta bit del giorno della settimana
    first_segment +=  str((sum([int(b) for b in first_segment[17:]]) +1) % 2) #P2: Secondo bit di parità del primo segmento
    return first_segment #Return del primo segmento


def generate_second_segment(date):
    second_segment = "10" #Bit identificativi del secondo segmento. NON MODIFICARE MAI!
    second_segment += generate_year_bit(date.year) #Aggiunta del bit dell'anno

    anno=date.year
    oggi=date.day
    ora=date.hour
    minuti=date.minute
    mese=date.month


    segmento_cambio = "111"

    if(mese==3 or mese==10):

        #Calcolo della data del cambio dell'ora estiva/solare

        month = calendar.monthcalendar(anno, 10)
        giorno_di_ottobre = max(month[-1][calendar.SUNDAY], month[-2][calendar.SUNDAY])
        month = calendar.monthcalendar(anno, 3)
        giorno_di_marzo = max(month[-1][calendar.SUNDAY], month[-2][calendar.SUNDAY])

        if((oggi==giorno_di_marzo - 6 and mese==3) or (oggi==giorno_di_ottobre - 6 and mese==10)):
            segmento_cambio = "110"
        elif((oggi==giorno_di_marzo - 5 and mese==3) or (oggi==giorno_di_ottobre - 5 and mese==10)):
            segmento_cambio = "101"
        elif((oggi==giorno_di_marzo - 4 and mese==3) or (oggi==giorno_di_ottobre - 4 and mese==10)):
            segmento_cambio = "100"
        elif((oggi==giorno_di_marzo - 3 and mese==3) or (oggi==giorno_di_ottobre - 3 and mese==10)):
            segmento_cambio = "011"
        elif((oggi==giorno_di_marzo - 2 and mese==3) or (oggi==giorno_di_ottobre - 2 and mese==10)):
            segmento_cambio = "010"
        elif((oggi==giorno_di_marzo - 1 and mese==3) or (oggi==giorno_di_ottobre - 1 and mese==10)):
            segmento_cambio = "001"
        elif(oggi == giorno_di_marzo and mese==3 and is_dst(date)==0):
            segmento_cambio = "000"
        elif(oggi == giorno_di_ottobre and mese==10 and is_dst(date)==1):
            segmento_cambio = "000"

    second_segment += segmento_cambio                                   #SE: Aggiunta bit preavviso cambio ora solare/estiva (Vedi nota in fondo)

    global avviso_secondo_intercalare                                   #(Vedi nota in fondo) Questi bit sono da settare manualmente, a inizio pagina.
                                                                        #Modificare questo valore se si intende inserire il preavviso per il secondo intercalare al termine del mese di luglio o di dicembre


    if(avviso_secondo_intercalare != "00"):                             #Il secondo intercalare può essere aggiunto solo al termine del mese di luglio o del mese di dicembre.
                                                                        #se il mese è diverso da luglio o dicembre si tratta di una impostazione errata che viene corretta con questa serie di istruzioni.
        if((mese != 1) and (mese != 6) and (mese != 7) and (mese != 12)):
            avviso_secondo_intercalare = "00"
        elif(mese == 1 and oggi >= 1 and ora > 0):
            avviso_secondo_intercalare = "00"
        elif(mese == 7 and oggi >= 1 and ora > 1):
            avviso_secondo_intercalare = "00"



    second_segment += avviso_secondo_intercalare  #SI: Aggiunta bit preavviso secondo intercalare
    second_segment +=  str((sum([int(b) for b in second_segment]) +1) % 2) #PA: Bit di parità del secondo segmento
    return second_segment                       #Return del secondo segmento


def generate_packet(date):
    first_segment = generate_first_segment(date)
    second_segment = generate_second_segment(date)

    return first_segment, second_segment, avviso_secondo_intercalare


#Significato dei bit del preavviso del cambio ora solare\estiva:

# 111 = Nessun cambio previsto nei prossimi 7 giorni
# 110 = Previsto un cambio entro 6 giorni
# 101 = Previsto un cambio entro 5 giorni
# 100 = Previsto un cambio entro 4 giorni
# 011 = Previsto un cambio entro 3 giorni
# 010 = Previsto un cambio entro 2 giorni
# 001 = Previsto un cambio entro 1 giorno
# 000 = Alle ore 02:00 si passa all'ora estiva oppure alle 03:00 si passa all'ora solare



#Significato dei bit del preavviso secondo intercalare. QUESTI BIT SONO DA SETTARE MANUALMENTE!!! ATTENZIONE!!!

# 00 = Nessun secondo intercalare entro il mese
# 10 = Ritardo di 1 secondo a fine mese
# 11 = Anticipo di 1 secondo a fine mese

#Per modificare il valore di questi bit all'interno dei segnali da generare cambiare i bit da "00" a "10" o "11" ad esempio. Questi bit vanno riportati a 00 dopo l'aggiunta/la sottrazione del secondo intercalare

#Per ulteriori informazioni sull'argomento visitare questo sito: https://www.ietf.org/timezones/data/leap-seconds.list
