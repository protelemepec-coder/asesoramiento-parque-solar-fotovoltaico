# 🛰️ Base de Datos de Radiación Solar Georreferenciada (NASA POWER)

## 1. Fuente Oficial Satelital
La información de radiación solar empleada en este simulador proviene de la API temporal del programa **NASA POWER** (*Prediction of Worldwide Energy Resources* - Langley Research Center, NASA):
- **Parámetro**: `ALLSKY_SFC_SW_DWN` (All Sky Surface Shortwave Downward Irradiance).
- **Unidad**: $\text{Wh/m}^2$ por hora o $\text{kWh/m}^2/\text{día}$ (Horas Sol Pico - HSP).
- **Resolución Espacial**: Celdas globales de $0{,}5^\circ \times 0{,}5^\circ$ (~50 km x 50 km).
- **Coordenadas de Referencia (Villa Allende / Córdoba)**: `-31.25194° S, -64.29087° O`.

---

## 2. Irradiación Solar Mensual Promedio (HSP en kWh/m²/día)

| Mes | HSP Diario (kWh/m²/día) | Calidad de Recurso | Características Estacionales |
| :--- | :---: | :---: | :--- |
| **Enero** | **7,21** | Excelente | Máxima radiación, días largos, solsticio estival. |
| **Febrero** | **5,71** | Muy Bueno | Nubosidad estival moderada, excelente aporte. |
| **Marzo** | **4,90** | Bueno | Transición equinoccial de otoño. |
| **Abril** | **3,43** | Medio | Disminución de declinación solar. |
| **Mayo** | **3,56** | Medio | Inicio de régimen seco invernal. |
| **Junio** | **3,09** | Mínimo | Solsticio invernal, ángulo de incidencia bajo. |
| **Julio** | **2,67** | Mínimo | Mayor impacto de frentes fríos y sombras largas. |
| **Agosto** | **3,88** | Bueno | Recuperación notable de la radiación directa. |
| **Septiembre** | **5,28** | Muy Bueno | Equinoccio de primavera, cielo despejado. |
| **Octubre** | **6,51** | Muy Bueno | Elevación del cenit solar. |
| **Noviembre** | **7,17** | Excelente | Régimen estival temprano de alta insolación. |
| **Diciembre** | **7,38** | Máximo Anual | Pico histórico de radiación solar en Córdoba. |
| **MEDIA ANUAL** | **5,065 HSP** | **Clase Mundial** | **Rendimiento específico: ~1.500 kWh/kWp/año.** |

---

## 3. Algoritmo de Ponderación Día a Día por Intervalo de Lectura
Dado que las tomas de lectura de medidores no coinciden con los meses calendario, el simulador calcula el promedio ponderado exacto:
$$HSP_{\text{intervalo}} = \frac{1}{N} \sum_{d=1}^{N} HSP_{\text{mes}(d)}$$
Donde $N$ es la cantidad exacta de días entre `LCT_FECHA_LECTURA_ANTERIOR` y `LCT_FECHA_LECTURA`.
