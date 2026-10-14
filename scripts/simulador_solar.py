#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Simulación Solar Fotovoltaica por Fecha de Lectura y Modelos Growatt
Autor: Antigravity AI - Agente 11: Copiloto Orquestador & Selector de Habilidades
Cuenta: inventarioenergycpy / PROTELEM-EPEC
"""

import json
import os
import argparse
import pandas as pd

HSP_MESES = {
    (2025, 10): 6.51, (2025, 11): 7.17, (2025, 12): 7.38,
    (2026, 1): 7.21,  (2026, 2): 5.71,  (2026, 3): 4.90,
    (2026, 4): 3.43,  (2026, 5): 3.56,  (2026, 6): 3.09,
    (2026, 7): 2.67,  (2026, 8): 3.88,  (2026, 9): 5.28,
    (2026, 10): 6.51
}

MODELOS_GROWATT = {
    "MOD-6K":   {"modelo": "Growatt MOD 6KTL3-X (6 kW)",   "kwp": 6.38,  "paneles": 11, "m2": 28.6, "usd": 5900},
    "MOD-8K":   {"modelo": "Growatt MOD 8KTL3-X (8 kW)",   "kwp": 8.70,  "paneles": 15, "m2": 39.0, "usd": 7200},
    "MOD-10K":  {"modelo": "Growatt MOD 10KTL3-X (10 kW)", "kwp": 10.44, "paneles": 18, "m2": 46.8, "usd": 8500},
    "MOD-12K":  {"modelo": "Growatt MOD 12KTL3-X (12 kW)", "kwp": 12.76, "paneles": 22, "m2": 57.2, "usd": 9900},
    "MID-15K":  {"modelo": "Growatt MID 15KTL3-X (15 kW)", "kwp": 15.08, "paneles": 26, "m2": 67.6, "usd": 11800},
}

def cargar_lecturas():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "lecturas_sigec_3091044.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def simular(modelo_key="MOD-10K", pr=0.81, max_coincidencia=0.46):
    mod = MODELOS_GROWATT.get(modelo_key, MODELOS_GROWATT["MOD-10K"])
    lecturas = cargar_lecturas()
    
    tot_c = 0.0
    tot_g = 0.0
    tot_a = 0.0
    tot_i = 0.0
    tot_r = 0.0
    
    filas = []
    for l in lecturas:
        dias = l["dias"]
        hsp = l["hsp_exacto"]
        cons = l["consumo_kwh"]
        
        # Generación = kWp * HSP * días * PR
        gen = mod["kwp"] * hsp * dias * pr
        # Autoconsumo limitado al porcentaje de coincidencia
        auto = min(gen * max_coincidencia, cons)
        iny = max(0.0, gen - auto)
        red = cons - auto
        
        tot_c += cons
        tot_g += gen
        tot_a += auto
        tot_i += iny
        tot_r += red
        
        filas.append({
            "Fecha Lectura": l["fecha_lectura"],
            "Días": dias,
            "HSP": hsp,
            "Consumo kWh": int(cons),
            "Generado kWh": int(round(gen)),
            "Autoconsumo (46%)": int(round(auto)),
            "Inyección (54%)": int(round(iny)),
            "Toma Red kWh": int(round(red)),
            "Cob Gen/Cons": f"{gen/cons*100:.1f}%"
        })
        
    df = pd.DataFrame(filas)
    print("=" * 85)
    print(f"SIMULACIÓN SOLAR GROWATT: {mod['modelo']} ({mod['kwp']} kWp - {mod['paneles']} paneles 580W)")
    print(f"Parámetros: Performance Ratio = {pr*100:.0f}% | Coincidencia Máxima = {max_coincidencia*100:.0f}%")
    print("=" * 85)
    print(df.to_string(index=False))
    print("-" * 85)
    print(f"TOTAL ACUMULADO (22/10/2025 al 19/08/2026 - 298 días):")
    print(f"  * Consumo Medido Total      : {tot_c:,.0f} kWh")
    print(f"  * Generación Solar Total    : {tot_g:,.0f} kWh ({tot_g/tot_c*100:.1f}% de cobertura global)")
    print(f"  * Autoconsumo Directo (46%) : {tot_a:,.0f} kWh ({tot_a/tot_c*100:.1f}% de ahorro en compra directa)")
    print(f"  * Inyección a Red EPEC (54%): {tot_i:,.0f} kWh (crédito inyectado a favor)")
    print(f"  * Energía Residual de Red   : {tot_r:,.0f} kWh")
    print(f"  * Presupuesto Llave en Mano : USD {mod['usd']:,.2f}")
    print("=" * 85)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulador Solar Growatt por Fecha de Lectura SIGEC")
    parser.add_argument("--modelo", default="MOD-10K", choices=list(MODELOS_GROWATT.keys()), help="Modelo de inversor Growatt")
    parser.add_argument("--pr", type=float, default=0.81, help="Performance Ratio (default 0.81)")
    parser.add_argument("--coincidencia", type=float, default=0.46, help="Coincidencia máxima (default 0.46)")
    args = parser.parse_args()
    simular(args.modelo, args.pr, args.coincidencia)
