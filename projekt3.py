# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 23:20:59 2019

@author: lenovo
"""

import os
import datetime as dt
from math import floor
import odczyt_gpx as od # Funkcje pomocznicze
from kivy.app import App # Okno aplikacji
from kivy.uix.boxlayout import BoxLayout # Rozmieszczenie elementow
from kivy.properties import ObjectProperty # Połaczenie kv z aplikacja 
from kivy.garden.mapview import MapMarker # Import znacznika 
from kivy.uix.label import Label # Operacje na obiekatch Label
from kivy.uix.popup import Popup # Okno popup
from kivy.uix.floatlayout import FloatLayout # Okno wczytywania pliku

# Klasa definiujaca widok aplikacji
class AddLocationForm(BoxLayout):
    
    # Obiekty i zmienne modyfikowane przez program
    droga = Label()
    przewy = Label()
    ascent = Label()
    descent = Label()
    predk = Label()
    czas = Label()
    wysmin = Label()
    wysmax = Label()
    my_map = ObjectProperty()
    filepath = Label()
    lat = []
    lon = []
    ele = []
    dates = []

    # Metoda obliczajaca paramtery trasy
    def oblicz_param(self):
        
        # Jesli plik nie wczytany zakoncz
        if self.lat == []:
            return
        
        
        alt_dif = [0] # Tablica przewyzszen pomiedzy kolejnymi punktami
        asc_dif = [0] # Tablica podejsc 
        desc_dif = [0] # Tablica zejsc
        
        # Przyporzadkowanie poczatkowej wartosci minimalnej i maksymalnej elewacji
        if str(self.ele[0]).isnumeric():
            h_max = self.ele[0]
            h_min = self.ele[0]
        else:
            h_max = -999999
            h_min = 999999

        time_dif = [0]
        dist = [0] # Tablica odleglosci pomiedyz kolejnymi punktami

        
        # Obliczenie wartosci przewyzszen i odleglosci pomiedzy punktami
        # oraz rysowanie punktow na mapie
        for index in range(len(self.lat)):
            if index == 0:
                pass
            else:
                start = index-1
                stop = index
                
                # Wyliczenie roznicy wysokosci i dodanie do odpowiednich list
                # Sprawdzenie czy dana wysokosc jest minimum lub maksimum
                if (self.ele[start] != None) and (self.ele[stop] != None):
                    h1 = self.ele[start]
                    h2 = self.ele[stop]
                    if h2 > h_max:
                        h_max = h2
                    if h2 < h_min:
                        h_min = h2 
                else:
                    h1 = 0
                    h2 = 0
                dh = h2 - h1     
                alt_dif.append(dh)
                if dh > 0:
                    asc_dif.append(dh)
                if dh < 0:
                    desc_dif.append(dh)
                
                # Wyliczenie roznicy odleglosci i dodanie do listy
                try:
                    dist_part = od.distance(self.lat[start], self.lon[start], h1, self.lat[stop], self.lon[stop], h2)
                except:
                    dist_part = 0
                dist.append(dist_part)
                
                # Wyliczenie roznicy czasu i dodanie do listy
                try:
                    deltat =  self.dates[stop] - self.dates[start]
                    time_dif.append(deltat.seconds)
                except:
                    time_dif.append(0)
                
                
                # Narysowanie punktu na mapie   
                self.draw_marker(self.lat[start], self.lon[start])    
        self.draw_marker(self.lat[-1], self.lon[-1])
        
        # Obliczenia i wyswietlanie wartosci zsumowanych i srednich
        self.droga.text = "{0:.3f}m".format(sum(dist))
        self.przewy.text = "{0:.3f}m".format(sum(alt_dif))
        self.ascent.text = "{0:.3f}m".format(sum(asc_dif)) 
        self.descent.text = "{0:.3f}m".format(-sum(desc_dif))
        self.wysmin.text = "{0:.3f}m".format(h_min)
        self.wysmax.text = "{0:.3f}m".format(h_max)
        time_sum = sum(time_dif)       
        if time_sum != 0:
            time_h = floor(time_sum/3600)
            time_m = floor(time_sum/60 % 60)
            time_s = floor(time_sum % 60)
            self.czas.text = "{}h {}m {}s".format(time_h, time_m, time_s) 
            self.predk.text = "{0:.3f}km/h".format(sum(dist)/time_sum*3.6) 
        else:
            self.czas.text = "Brak danych"
            self.predk.text = "Brak danych"

    # Metoda rysujaca punkt o podanych wspolrzednych na mapie
    def draw_marker(self, lati, long):
        marker = MapMarker(lat = lati, lon = long)
        self.my_map.add_marker(marker)
        
    # Metoda otwierajaca okno wczytania pliku   
    def show_load(self):
        content = LoadDialog(load=self.load_list, cancel=self.dismiss_popup) 
        self._popup = Popup(title="Wczytaj plik", content=content, size_hint=(1, 1))
        self._popup.open()
       
    # Metoda wczytujaca wybrany plik
    def load_list(self, path, filename):
        path = os.path.join(path, filename[0])
        try:
            self.lat, self.lon,  self.ele, self.dates = od.importGpx(path)
        except:
            return
        self.filepath.text = str(filename[0])
        self.dismiss_popup()

    # Metoda zamyakajaca okno wyboru pliku
    def dismiss_popup(self): 
        self._popup.dismiss()
            
# Klasa definujaca aplikacje           
class MapViewApp(App):
    def build(self):
        return AddLocationForm()

# Klasa do odczytu pliku
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

# Uruchomienie aplikacji
MapViewApp().run()
