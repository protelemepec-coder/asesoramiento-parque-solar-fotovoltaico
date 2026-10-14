# ☀️ Asesoramiento para Parque Solar Fotovoltaico
### Simulador Georreferenciado, Análisis de Consumo por Fecha de Lectura SIGEC y Modelado Comercial Growatt

[![GitHub](https://img.shields.io/badge/GitHub-inventarioenergycpy-blue.svg)](https://github.com/inventarioenergycpy)
[![Ecosistema](https://img.shields.io/badge/Ecosistema-PROTELEM--EPEC-orange.svg)](https://github.com/PROTELEM-EPEC)
[![Licencia](https://img.shields.io/badge/Licencia-Privada-green.svg)](#)
[![Metodología](https://img.shields.io/badge/Metodolog%C3%ADa-6%20Etapas-purple.svg)](#)

Repositorio especializado en el dimensionamiento, simulación matemática y asesoramiento integral para instalaciones solares fotovoltaicas on-grid en la Provincia de Córdoba (Argentina), integrando **datos de radiación solar satelital georreferenciada (NASA POWER)**, consumo histórico extraído directamente del sistema comercial de EPEC (**Oracle / XXSIGEC**), y la gama de **inversores trifásicos comerciales Growatt**.

---

## 📌 1. Caso de Estudio: Suministro Residencial El Terrón (Villa Allende)

- **Cliente / Titular**: `SFERCO RUDY DELFINA` (Cliente N°: `6000840`)
- **CUIT / DNI Oficial**: `27-45696222-5` | DNI `45.696.222`
- **Suministro Comercial**: **`3091044`**
- **Contrato Activo**: `0309104402` (Suministro 3091044, Contrato 2) | Vigente (`V`)
- **Tarifa y Categoría**: Residencial T1 Monofásica/Trifásica (`TCL 140`, `CLA 1`, `CAT 110`)
- **Tipo de Suministro**: **Trifásico (`T`)**
- **Medidor Físico Activo**: `STE_NUMERO = 9039488` (instalado el 22/10/2025)
- **Ubicación Catastral**: `BARRIO EL TERRON - EL TERRON LOTE 454`, Villa Allende (CP 5107)
- **Georreferencia Oficial SIGEC**:
  - **Latitud**: `-31.2519431° S`
  - **Longitud**: `-64.2908749° O`

---

## ⚡ 2. Marco Metodológico y Reglas Rectoras de Simulación

1. **Trabajo por Fecha de Lectura Real**:
   - En lugar de promediar meses calendario o períodos bimestrales teóricos, se toman las fechas exactas de lectura del medidor (`LCT_FECHA_LECTURA_ANTERIOR` a `LCT_FECHA_LECTURA`) y los días de intervalo efectivo.
2. **Ponderación Solar Día a Día (NASA POWER)**:
   - Se calcula el **HSP (Horas Sol Pico en kWh/m²/día)** específico y ponderado para cada intervalo exacto entre lecturas con la base satelital oficial.
3. **Restricción Práctica de Coincidencia (46% Máximo)**:
   - Tomando la consideración práctica de que la coincidencia entre el consumo diurno del cliente y la generación solar fotovoltaica **nunca supera el 46%** en un caso real residencial:
     - **Autoconsumo Inmediato**: $\min(	ext{Generación Solar} 	imes 0{,}46, 	ext{Consumo Medido})$.
     - **Inyección a Red EPEC**: $	ext{Generación Solar} - 	ext{Autoconsumo}$ (el 54% restante inyectado a la red bajo la Ley 27.424 / Ley 10.604).
     - **Toma de Red**: $	ext{Consumo Medido} - 	ext{Autoconsumo}$.
4. **Performance Ratio (PR)**: Se adopta un factor conservador del **81%** (considera temperatura sobre cubierta, polvo, caídas de tensión DC/AC y rendimiento del inversor).

---

## 📊 3. Registro Base de Lecturas Reales en SIGEC (22/10/2025 al 19/08/2026)

| # | Fecha Lectura | Intervalo Físico Medido | Días | Estado Anterior | Estado Leído | Consumo Medido (kWh) | Consumo Diario (kWh/d) | Radiación Solar Ponderada (HSP) | Documento SIGEC |
| :-: | :---: | :---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **1** | **17/11/2025** | 22/10/2025 al 17/11/2025 | 26 | 90.580 | 92.340 | **1.760** | 67,7 | **6,92** | `72626712` |
| **2** | **18/12/2025** | 17/11/2025 al 18/12/2025 | 31 | 92.340 | 94.439 | **2.099** | 67,7 | **7,29** | `72626714` |
| **3** | **18/01/2026** | 18/12/2025 al 18/01/2026 | 31 | 94.439 | 97.670 | **3.231** | 104,2 | **7,29** | `72642208` |
| **4** | **20/02/2026** | 18/01/2026 al 20/02/2026 | 33 | 97.670 | 101.109 | **3.439** | 104,2 | **6,35** | `72642210` |
| **5** | **23/03/2026** | 20/02/2026 al 23/03/2026 | 31 | 101.109 | 102.956 | **1.847** | 59,6 | **5,14** | `706637593` |
| **6** | **22/04/2026** | 23/03/2026 al 22/04/2026 | 30 | 102.956 | 104.743 | **1.787** | 59,6 | **3,87** | `706642712` |
| **7** | **18/05/2026** | 22/04/2026 al 18/05/2026 | 26 | 104.743 | 107.986 | **3.243** | 124,7 | **3,52** | `709082333` |
| **8** | **12/06/2026** | 18/05/2026 al 12/06/2026 | 25 | 107.986 | 111.104 | **3.118** | 124,7 | **3,35** | `709087458` |
| **9** | **16/07/2026** | 12/06/2026 al 16/07/2026 | 34 | 111.104 | 117.431 | **6.327** | 186,1 | **2,90** | `711394244` |
| **10** | **19/08/2026** | 16/07/2026 al 19/08/2026 | 34 | 117.431 | 123.758 | **6.327** | 186,1 | **3,31** | `711399375` |
| **TOTAL** | **Período de 298 días** | — | **298** | **90.580** | **123.758** | **33.178 kWh** | **111,3** | **4,92 media** | — |

---

## ☀️ 4. Comparativa de Modelos Comerciales Growatt Trifásicos

| Modelo Growatt | Potencia AC / DC | Paneles (580W) | Sup. Techo (m²) | Generación (298 días) | Autoconsumo (46%) | Inyección a Red (54%) | Cobertura Gen / Consumo | Ahorro Directo en Compra | Presupuesto Llave en Mano (USD) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Growatt MOD 6KTL3-X** | 6 kW / 6,38 kWp | 11 | 28,6 m² | 7.766 kWh | 3.572 kWh | 4.194 kWh | **23,4%** | **10,8%** | USD 5.900 |
| **Growatt MOD 8KTL3-X** | 8 kW / 8,70 kWp | 15 | 39,0 m² | 10.594 kWh | 4.873 kWh | 5.721 kWh | **31,9%** | **14,7%** | USD 7.200 |
| **Growatt MOD 10KTL3-X ⭐ (Recomendado)** | **10 kW / 10,44 kWp** | **18** | **46,8 m²** | **12.713 kWh** | **5.848 kWh** | **6.865 kWh** | **38,3%** | **17,6%** | **USD 8.500** |
| **Growatt MOD 12KTL3-X** | 12 kW / 12,76 kWp | 22 | 57,2 m² | 15.538 kWh | 7.147 kWh | 8.390 kWh | **46,8%** | **21,5%** | USD 9.900 |
| **Growatt MID 15KTL3-X** | 15 kW / 15,08 kWp | 26 | 67,6 m² | 18.363 kWh | 8.447 kWh | 9.916 kWh | **55,3%** | **25,5%** | USD 11.800 |

---

## 🚀 5. Uso del Simulador por Consola (CLI)

```bash
# Simular con el modelo recomendado de 10 kW (MOD 10KTL3-X)
python scripts/simulador_solar.py --modelo MOD-10K

# Simular con modelo de máxima cobertura invernal de 15 kW (MID 15KTL3-X)
python scripts/simulador_solar.py --modelo MID-15K

# Simular con coincidencia personalizada (ej. 40%) y PR de 82%
python scripts/simulador_solar.py --modelo MOD-10K --coincidencia 0.40 --pr 0.82
```

---

## 📂 6. Estructura Documental del Repositorio

- [`docs/01-Marco-Normativo-y-Regulacion-EPEC.md`](docs/01-Marco-Normativo-y-Regulacion-EPEC.md): Ley 27.424, Ley Provincial 10.604, ERSeP, medidor bidireccional y régimen tarifario.
- [`docs/02-Base-Radiacion-Solar-NASA-POWER.md`](docs/02-Base-Radiacion-Solar-NASA-POWER.md): Algoritmo de ponderación día a día e irradiación satelital oficial.
- [`docs/03-Analisis-Consumo-Suministro-3091044.md`](docs/03-Analisis-Consumo-Suministro-3091044.md): Análisis detallado de las 10 lecturas de medidor y estacionalidad invernal.
- [`docs/04-Simulador-Modelos-Growatt.md`](docs/04-Simulador-Modelos-Growatt.md): Lógica matemática del simulador y fichas técnicas Growatt.
- [`docs/05-Presupuesto-Tecnico-Comercial.md`](docs/05-Presupuesto-Tecnico-Comercial.md): Presupuesto llave en mano, lista de materiales e ingeniería.
