import streamlit as st
import matplotlib.image as image
import pandas as pd
import joblib
import geopy
from geopy.distance import distance
import shapefile
from shapely.geometry import Point
from shapely.geometry import shape
import pydeck as pdk
path='/app/streamlit/orienting/'
geo=geopy.geocoders.Nominatim(user_agent='rp')
with st.container():
  st.image(image.imread(path+'orienting_logo.png'))
  tab1,tab2=st.tabs(['Appartamento','Stanza'])
  with tab1:
    ''
    ind1=st.text_input('Indirizzo:',key='ind1')
    ''
    col1,col2,col3=st.columns(3)
    with col1:
      sup1=st.slider('Superficie dell\'appartamento:',25,250,50,key='sup1')
    with col2:
      cam1=st.slider('Numero di camere da letto:',1,4,1,key='cam1')
    with col3:
      per1=st.slider('Numero di persone:',1,8,2,key='per1')
    ''
    col1,col2,col3,col4=st.columns(4)
    with col1:
      ute1=st.checkbox('Utenze incluse',key='ute1')
      gia1=st.checkbox('Giardino',key='gia1')
    with col2:
      bal1=st.checkbox('Balcone',key='bal1')
      lvt1=st.checkbox('Lavatrice',key='lvt1')
    with col3:
      asc1=st.checkbox('Asciugatrice',key='asc1')
      lvs1=st.checkbox('Lavastoviglie',key='lvs1')
    with col4:
      con1=st.checkbox('Condizionatore',key='con1')
    ''
    try:
      loc1=geo.geocode(ind1)
      if loc1.address.find('Madrid')>-1:
        i1=1
        ds1=shapefile.Reader(path+'madrid_shapes.shp')
        dp1=pd.read_csv(path+'madrid_prices.csv')
        mod1=joblib.load(path+'lr_mf.sav')
        poi1=pd.read_csv(path+'madrid_poi.csv')
      if loc1.address.find('Paris')>-1:
        i1=3
        ds1=shapefile.Reader(path+'paris_shapes.shp')
        dp1=pd.read_csv(path+'paris_prices.csv')
        mod1=joblib.load(path+'lr_pf.sav')
        poi1=pd.read_csv(path+'paris_poi.csv')
      dpr1=min(dp1.Prezzo)
      for s in range(len(ds1.shapes())):
        if Point(loc1.longitude,loc1.latitude).within(shape(ds1.shapes()[s])):
          dpr1=ds1.records()[s][i1]
      for p in dp1.index:
        if dpr1==dp1.Distretto[p]:
          dpr1=int(dp1.Prezzo[p])
      pdd1=pd.DataFrame({'Nome':list(range(7)),'Latitudine':list(range(7)),'Longitudine':list(range(7)),'Icona':[
        {'url':'https://upload.wikimedia.org/wikipedia/commons/a/a7/Map_marker_icon_–_Nicolas_Mollet_–_Subway_–_Transportation_–_Default.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/6/65/Map_marker_icon_–_Nicolas_Mollet_–_Steam_Locomotive_–_Transportation_–_Default.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/f/ff/Map_marker_icon_–_Nicolas_Mollet_–_Supermarket_–_Stores_–_iphone.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/f/f1/Map_marker_icon_–_Nicolas_Mollet_–_Work_office_–_Offices_–_iOS.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/1/16/Map_marker_icon_–_Nicolas_Mollet_–_University_–_Health_%26_Education_–_iOS.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/5/53/Map_marker_icon_–_Nicolas_Mollet_–_Hospital_–_Health_%26_Education_–_iOS.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/9/92/Map_marker_icon_–_Nicolas_Mollet_–_Home_–_People_–_Default.png','width':32,'height':37,'anchorY':37}]})
      dis1=[]
      p=0
      for t in ['Metro','Treno','Supermarket','Coworking','Università','Ospedale']:
        d1=100
        for i in poi1[poi1.Tipologia==t].index:
          if distance((loc1.latitude,loc1.longitude),(poi1.Latitudine[i],poi1.Longitudine[i])).km<d1:
            d1=distance((loc1.latitude,loc1.longitude),(poi1.Latitudine[i],poi1.Longitudine[i])).km
            pdd1.iloc[p,0]=poi1.Nome[i]
            pdd1.iloc[p,1]=poi1.Latitudine[i]
            pdd1.iloc[p,2]=poi1.Longitudine[i]
        dis1.append(round(d1*1000))
        p=p+1
      pdd1.iloc[p,0]=loc1.address
      pdd1.iloc[p,1]=loc1.latitude
      pdd1.iloc[p,2]=loc1.longitude
      pre1=round(mod1.predict([[dpr1,sup1,cam1,per1,gia1,bal1,con1,lvt1,asc1,lvs1,ute1,dis1[0],dis1[1],dis1[2],dis1[3],dis1[4],dis1[5]]])[0])
      st.subheader(f'L\'affitto mensile stimato dell\'appartamento è {pre1}€')
      ''
      with st.expander('Punti di interesse:',False):
        f'- La metro più vicina è "{pdd1.iloc[0,0]}" e dista {dis1[0]}m'
        f'- Il treno più vicino è "{pdd1.iloc[1,0]}" e dista {dis1[1]}m'
        f'- Il supermarket più vicino è "{pdd1.iloc[2,0]}" e dista {dis1[2]}m'
        f'- Il coworking più vicino è "{pdd1.iloc[3,0]}" e dista {dis1[3]}m'
        f'- L\'università più vicina è "{pdd1.iloc[4,0]}" e dista {dis1[4]}m'
        f'- L\'ospedale più vicino è "{pdd1.iloc[5,0]}" e dista {dis1[5]}m'
        ''
        icon_layer=pdk.Layer('IconLayer',data=pdd1,get_icon='Icona',get_position=['Longitudine','Latitudine'],get_size=60,pickable=True)
        view_state=pdk.ViewState(longitude=loc1.longitude,latitude=loc1.latitude,zoom=14)
        st.pydeck_chart(pdk.Deck(layers=[icon_layer], initial_view_state=view_state,tooltip={'text':'{Nome}'}))
    except:
      if ind1!='':
        st.subheader('Indirizzo non valido! Provane un altro.')
  with tab2:
    ''
    ind2=st.text_input('Indirizzo:',key='ind2')
    ''
    col1,col2=st.columns(2)
    with col1:
      sup2=st.slider('Superficie della stanza:',6,30,10,key='sup2')
    with col2:
      per2=st.slider('Numero di inquilini:',1,8,4,key='per2')
    ''
    col1,col2,col3,col4=st.columns(4)
    with col1:
      ute2=st.checkbox('Utenze incluse',key='ute2')
      gia2=st.checkbox('Giardino',key='gia2')
    with col2:
      bal2=st.checkbox('Balcone',key='bal2')
      lvt2=st.checkbox('Lavatrice',key='lvt2')
    with col3:
      asc2=st.checkbox('Asciugatrice',key='asc2')
      lvs2=st.checkbox('Lavastoviglie',key='lvs2')
    with col4:
      con2=st.checkbox('Condizionatore',key='con2')
      wcp2=st.checkbox('WC privato',key='wcp2')
    ''
    try:
      loc2=geo.geocode(ind2)
      if loc2.address.find('Madrid')>-1:
        i2=1
        ds2=shapefile.Reader(path+'madrid_shapes.shp')
        dp2=pd.read_csv(path+'madrid_prices.csv')
        mod2=joblib.load(path+'lr_mr.sav')
        poi2=pd.read_csv(path+'madrid_poi.csv')
      if loc2.address.find('Paris')>-1:
        i2=3
        ds2=shapefile.Reader(path+'paris_shapes.shp')
        dp2=pd.read_csv(path+'paris_prices.csv')
        mod2=joblib.load(path+'lr_pr.sav')
        poi2=pd.read_csv(path+'paris_poi.csv')
      dpr2=min(dp2.Prezzo)
      for s in range(len(ds2.shapes())):
        if Point(loc2.longitude,loc2.latitude).within(shape(ds2.shapes()[s])):
          dpr2=ds2.records()[s][i2]
      for p in dp2.index:
        if dpr2==dp2.Distretto[p]:
          dpr2=int(dp2.Prezzo[p])
      pdd2=pd.DataFrame({'Nome':list(range(7)),'Latitudine':list(range(7)),'Longitudine':list(range(7)),'Icona':[
        {'url':'https://upload.wikimedia.org/wikipedia/commons/a/a7/Map_marker_icon_–_Nicolas_Mollet_–_Subway_–_Transportation_–_Default.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/6/65/Map_marker_icon_–_Nicolas_Mollet_–_Steam_Locomotive_–_Transportation_–_Default.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/f/ff/Map_marker_icon_–_Nicolas_Mollet_–_Supermarket_–_Stores_–_iphone.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/f/f1/Map_marker_icon_–_Nicolas_Mollet_–_Work_office_–_Offices_–_iOS.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/1/16/Map_marker_icon_–_Nicolas_Mollet_–_University_–_Health_%26_Education_–_iOS.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/5/53/Map_marker_icon_–_Nicolas_Mollet_–_Hospital_–_Health_%26_Education_–_iOS.png','width':32,'height':37,'anchorY':37},
        {'url':'https://upload.wikimedia.org/wikipedia/commons/9/92/Map_marker_icon_–_Nicolas_Mollet_–_Home_–_People_–_Default.png','width':32,'height':37,'anchorY':37}]})
      dis2=[]
      p=0
      for t in ['Metro','Treno','Supermarket','Coworking','Università','Ospedale']:
        d2=100
        for i in poi2[poi2.Tipologia==t].index:
          if distance((loc2.latitude,loc2.longitude),(poi2.Latitudine[i],poi2.Longitudine[i])).km<d2:
            d2=distance((loc2.latitude,loc2.longitude),(poi2.Latitudine[i],poi2.Longitudine[i])).km
            pdd2.iloc[p,0]=poi2.Nome[i]
            pdd2.iloc[p,1]=poi2.Latitudine[i]
            pdd2.iloc[p,2]=poi2.Longitudine[i]
        dis2.append(round(d2*1000))
        p=p+1
      pdd2.iloc[p,0]=loc2.address
      pdd2.iloc[p,1]=loc2.latitude
      pdd2.iloc[p,2]=loc2.longitude
      pre2=round(mod2.predict([[dpr2,sup2,per2,wcp2,gia2,bal2,con2,lvt2,asc2,lvs2,ute2,dis2[0],dis2[1],dis2[2],dis2[3],dis2[4],dis2[5]]])[0])
      st.subheader(f'L\'affitto mensile stimato della stanza è {pre2}€')
      ''
      with st.expander('Punti di interesse:',False):
        f'- La metro più vicina è "{pdd2.iloc[0,0]}" e dista {dis2[0]}m'
        f'- Il treno più vicino è "{pdd2.iloc[1,0]}" e dista {dis2[1]}m'
        f'- Il supermarket più vicino è "{pdd2.iloc[2,0]}" e dista {dis2[2]}m'
        f'- Il coworking più vicino è "{pdd2.iloc[3,0]}" e dista {dis2[3]}m'
        f'- L\'università più vicina è "{pdd2.iloc[4,0]}" e dista {dis2[4]}m'
        f'- L\'ospedale più vicino è "{pdd2.iloc[5,0]}" e dista {dis2[5]}m'
        ''
        icon_layer=pdk.Layer('IconLayer',data=pdd2,get_icon='Icona',get_position=['Longitudine','Latitudine'],get_size=60,pickable=True)
        view_state=pdk.ViewState(longitude=loc2.longitude,latitude=loc2.latitude,zoom=14)
        st.pydeck_chart(pdk.Deck(layers=[icon_layer], initial_view_state=view_state,tooltip={'text':'{Nome}'}))
    except:
      if ind2!='':
        st.subheader('Indirizzo non valido! Provane un altro.')