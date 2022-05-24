from shapely.geometry import Polygon, mapping, Point


def valid_list(lista):
    try:
        lista = [tup.split(',') for tup in lista.split(';')]
    except:
        return 8
    if geo_less_than_3(lista):
        return 1
    lista_float = geo_float(lista)
    try:
        return int(lista_float)
    except:
        return lista_float


def valid_polygon(lista):
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


def valid_name(name, data):
    name = name[4:]
    if not name.isalnum():
        return 1
    if name in data['areas']:
        return 2
    return name