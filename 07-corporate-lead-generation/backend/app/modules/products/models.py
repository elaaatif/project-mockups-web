from app.core.common import Repository

CATEGORIES = [
    {"slug": "pumps", "name": "Industrial pumps", "icon": "Droplets"},
    {"slug": "valves", "name": "Valves & actuators", "icon": "SlidersHorizontal"},
    {"slug": "motors", "name": "Motors & drives", "icon": "Zap"},
    {"slug": "automation", "name": "Automation & sensors", "icon": "Cpu"},
    {"slug": "air", "name": "Compressed air", "icon": "Wind"},
]


def _p(i, sku, name, cat, summary, specs, applications, lead_time, certifications=("CE", "UKCA", "ISO 9001")):
    return {"id": i, "sku": sku, "slug": sku.lower(), "name": name, "category": cat, "summary": summary, "specs": specs,
            "applications": applications, "lead_time_weeks": lead_time, "certifications": list(certifications),
            "datasheet": f"/datasheets/{sku.lower()}.pdf", "moq": 1}


products = Repository([
    _p(1, "VX-CP200", "VX-CP200 Centrifugal Pump", "pumps", "End-suction centrifugal pump for clean water and light chemicals, IE4 motor.",
       {"Flow rate": "up to 240 m³/h", "Head": "up to 95 m", "Power": "4–75 kW", "Materials": "Cast iron / 316 stainless", "Temperature": "-20 to 120 °C"},
       ["Water treatment", "HVAC", "Irrigation"], 4),
    _p(2, "VX-HP50", "VX-HP50 Hygienic Pump", "pumps", "EHEDG-certified hygienic pump with CIP/SIP capability for food and pharma.",
       {"Flow rate": "up to 80 m³/h", "Head": "up to 60 m", "Surface finish": "Ra ≤ 0.8 µm", "Seals": "EPDM / FKM", "Connections": "Tri-clamp, DIN 11851"},
       ["Food & beverage", "Pharmaceutical", "Dairy"], 6, ("CE", "UKCA", "EHEDG", "3-A")),
    _p(3, "VX-DP12", "VX-DP12 Dosing Pump", "pumps", "Diaphragm metering pump with ±1% accuracy and Modbus control.",
       {"Flow rate": "0.1–120 l/h", "Pressure": "up to 16 bar", "Accuracy": "±1%", "Control": "4–20 mA, Modbus RTU"},
       ["Chemical dosing", "Water treatment"], 3),
    _p(4, "VX-BV300", "VX-BV300 Butterfly Valve", "valves", "Wafer-type butterfly valve with pneumatic or electric actuation.",
       {"Sizes": "DN50–DN600", "Pressure rating": "PN16", "Body": "Ductile iron", "Disc": "316 stainless", "Actuation": "Manual / pneumatic / electric"},
       ["Water distribution", "HVAC", "Process isolation"], 3),
    _p(5, "VX-CV40", "VX-CV40 Control Valve", "valves", "Globe control valve with smart positioner and HART diagnostics.",
       {"Sizes": "DN15–DN200", "Pressure rating": "PN40", "Characteristic": "Equal % / linear", "Positioner": "HART 7"},
       ["Steam", "Process control", "Energy"], 8),
    _p(6, "VX-M4", "VX-M4 IE4 Motor Series", "motors", "Super-premium efficiency induction motors, 0.75–355 kW.",
       {"Efficiency class": "IE4", "Power": "0.75–355 kW", "Protection": "IP55 / IP66", "Mounting": "B3, B5, B14", "Insulation": "Class F"},
       ["Pumps & fans", "Conveyors", "Compressors"], 2),
    _p(7, "VX-VSD", "VX-VSD Variable Speed Drive", "motors", "Compact VSD with built-in PID, safe torque off and energy optimiser.",
       {"Power": "0.37–250 kW", "Supply": "380–480 V, 3-phase", "Safety": "STO SIL3", "Comms": "Profinet, EtherNet/IP, Modbus TCP"},
       ["Pumps & fans", "Material handling"], 2),
    _p(8, "VX-PLC9", "VX-PLC9 Modular Controller", "automation", "Modular PLC with integrated edge computing and OPC UA.",
       {"I/O": "up to 2,048 points", "Cycle time": "< 1 ms", "Protocols": "OPC UA, MQTT, Profinet", "Programming": "IEC 61131-3"},
       ["Line automation", "Building management"], 5),
    _p(9, "VX-SENS", "VX-SENS IIoT Sensor Kit", "automation", "Wireless vibration and temperature sensors for predictive maintenance.",
       {"Battery life": "5 years", "Range": "up to 1 km (LoRaWAN)", "Measurements": "Vibration, temperature, RPM", "Rating": "IP68, ATEX Zone 1"},
       ["Predictive maintenance", "Remote monitoring"], 2, ("CE", "UKCA", "ATEX")),
    _p(10, "VX-RC37", "VX-RC37 Rotary Screw Compressor", "air", "Oil-injected rotary screw compressor with integrated dryer and VSD.",
       {"Power": "37 kW", "Free air delivery": "up to 7.2 m³/min", "Pressure": "5.5–13 bar", "Noise": "66 dB(A)"},
       ["Manufacturing plants", "Workshops"], 6),
], key="slug")
