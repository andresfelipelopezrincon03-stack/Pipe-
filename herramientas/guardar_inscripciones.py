"""Pasa las inscripciones nuevas (cifradas) del canal de envío a la carpeta de datos.

Uso: guardar_inscripciones.py <nuevos.jsonl> <carpeta_datos>
No puede leer el contenido: todo llega cifrado y solo se abre con la clave del panel.
"""
import json, os, re, sys, urllib.request

TOPE = 5000                    # máximo de inscripciones guardadas
TOPE_SOPORTE = 3 * 1024 * 1024  # tamaño máximo de un soporte cifrado
ID_OK = re.compile(r'^[A-Za-z0-9]{8,40}$')
ADJUNTO = 'https://ntfy.sh/file/'


def descargar(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        datos = r.read(TOPE_SOPORTE + 1)
    if not datos or len(datos) > TOPE_SOPORTE:
        raise ValueError('tamaño')
    return datos


def texto(s, k, n):
    return isinstance(s.get(k), str) and 0 < len(s[k]) <= n


def main(nuevos, carpeta, bajar=descargar):
    ruta = os.path.join(carpeta, 'inscripciones.jsonl')
    os.makedirs(os.path.join(carpeta, 'soportes'), exist_ok=True)
    guardados, por_id = [], {}
    if os.path.exists(ruta):
        for linea in open(ruta, encoding='utf-8'):
            try:
                s = json.loads(linea)
            except ValueError:
                continue
            if isinstance(s, dict) and ID_OK.match(str(s.get('id', ''))):
                guardados.append(s); por_id[s['id']] = s
    cambios = 0
    for linea in open(nuevos, encoding='utf-8'):
        try:
            m = json.loads(linea)
            if m.get('event') != 'message':
                continue
            s = json.loads(m.get('message', ''))
        except ValueError:
            continue
        if not isinstance(s, dict) or s.get('v') != 1:
            continue
        if not (texto(s, 'id', 40) and ID_OK.match(s['id']) and texto(s, 'k', 700) and texto(s, 'iv', 40) and texto(s, 'c', 2400)):
            continue
        if s['id'] not in por_id:
            if len(guardados) >= TOPE:
                continue
            nuevo = {'v': 1, 'id': s['id'], 't': int(m.get('time', 0)), 'k': s['k'], 'iv': s['iv'], 'c': s['c']}
            if texto(s, 'iv2', 40) and texto(s, 'f', 200) and s['f'].startswith(ADJUNTO):
                nuevo['iv2'] = s['iv2']; nuevo['f'] = s['f']
            guardados.append(nuevo); por_id[s['id']] = nuevo; cambios += 1
        g = por_id[s['id']]
        if 'f' in g and g.get('fs') != 1:   # falta guardar su soporte: se intenta en cada pasada
            try:
                datos = bajar(g['f'])
                with open(os.path.join(carpeta, 'soportes', g['id'] + '.bin'), 'wb') as f:
                    f.write(datos)
                g['fs'] = 1; cambios += 1
            except Exception as e:
                print('soporte pendiente', g['id'], type(e).__name__)
    if cambios or not os.path.exists(ruta):
        with open(ruta, 'w', encoding='utf-8') as f:
            for s in guardados:
                f.write(json.dumps(s, separators=(',', ':')) + '\n')
    print('cambios:', cambios, 'total:', len(guardados), 'con soporte guardado:', sum(1 for s in guardados if s.get('fs') == 1))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
