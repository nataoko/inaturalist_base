from shapely.geometry import Polygon, Point

def valid_list(lista):
    if geo_less_than_3(lista):
        return 1
    lista_float = geo_float(lista)
    try:
        return int(lista_float)
    except:
        return lista_float

def valid_poligon(lista):
    polygon = Polygon(lista)
    if not polygon.is_valid:
        return 7
    return polygon

def geo_less_than_3(lista):
    if len(lista) < 3:
        return 1
    return 0

def geo_float(lista):
  lista_float = []
  try:
    for long, lati in lista:
      try:
        long = round(float(long), 5)
        if long < -180 or long > 180:
          return 3
      except:
        return 2
      try:
        lati = round(float(lati), 5)
        if lati < -90 or lati > 90:
          return 5
      except:
        return 4
      lista_float.append((long, lati))
  except:
    return 6
  return lista_float

#polygon.contains(Point(p))
#folium.Marker([0, 10], popup="Znacznik").add_to(mapa)

##print(valid_list([('0'), ('0','1'), ('0','2')]),
##valid_list([('1', '0','4'), ('0','1'), ('0','2')]),
##valid_list([('0','a'), ('0','1'), ('0','2')]),
##valid_list([('a', '0'), ('0','1'), ('0','2')]),
##valid_list([('200', '0'), ('0','1'), ('0','2')]),
##valid_list([('2', '100'), ('0','1'), ('0','2')]),
##valid_list([('1', '0'), ('0','1'), ('0','2')]),
##valid_list([('1', '0'), ('0','1')]),
##valid_list([('1', '0')]))
