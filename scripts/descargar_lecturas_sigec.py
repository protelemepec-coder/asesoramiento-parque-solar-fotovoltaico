#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conector de Extracción Automatizada Oracle / SIGEC EPEC
Descarga datos catastrales, contrato, medidor y lecturas históricas de un suministro.
"""

import os
import sys
import oracledb
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def consultar_suministro(srv_codigo=3091044):
    lib_dir = os.getenv("OR_INSTANT_CLIENT", r"C:\app\client\product\19.0.0\client_2\bin")
    try:
        oracledb.init_oracle_client(lib_dir=lib_dir)
    except Exception:
        pass

    conn = oracledb.connect(
        user=os.getenv("OR_USER"),
        password=os.getenv("OR_PASS"),
        host=os.getenv("OR_HOST"),
        port=os.getenv("OR_PORT", 1521),
        service_name=os.getenv("OR_SERVICE_NAME")
    )
    cursor = conn.cursor()
    print(f"[*] Consultando datos en SIGEC para suministro {srv_codigo}...")

    # Suministro
    cursor.execute("""
    SELECT s.srv_codigo, s.srv_direccion, s.srv_calle, s.srv_nro, s.srv_c_postal,
           s.srv_gps_latitud, s.srv_gps_longitud, s.scf_codigo, s.agf_codigo, s.bar_codigo
    FROM xxsigec.servicios s WHERE s.srv_codigo = :srv
    """, srv=srv_codigo)
    srv = cursor.fetchone()
    print("Suministro:", srv)

    # Lecturas desde Nov 2025
    query = """
    SELECT 
        l.lct_codigo,
        l.lct_fecha_lectura_anterior,
        l.lct_fecha_lectura,
        TRUNC(l.lct_fecha_lectura) - TRUNC(l.lct_fecha_lectura_anterior) AS dias_periodo,
        l.lct_valor_leido_anterior,
        l.lct_valor_leido,
        l.lct_consumo,
        l.doc_numero
    FROM xxsigec.lecturas l
    WHERE l.srv_codigo = :srv
      AND l.lct_fecha_lectura >= TO_DATE('2025-10-01', 'YYYY-MM-DD')
    ORDER BY l.lct_fecha_lectura ASC
    """
    cursor.execute(query, srv=srv_codigo)
    cols = [d[0] for d in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=cols)
    print("
Lecturas encontradas:")
    print(df.to_string())
    conn.close()

if __name__ == "__main__":
    srv = int(sys.argv[1]) if len(sys.argv) > 1 else 3091044
    consultar_suministro(srv)
