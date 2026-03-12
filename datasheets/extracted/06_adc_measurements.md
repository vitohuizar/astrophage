# BQ76942 - ADC Measurement Registers

> Source: BQ76942 Technical Reference Manual (SLUUBY1B), Chapter 4

## 1. Cell Voltage Measurements (16-bit, Direct Commands)

Each cell voltage = differential measurement between adjacent VC pins.
Resolution: 1 mV, range: -0.2V to 5.5V recommended.

| Command | Name            | Units | Pins        |
|---------|-----------------|-------|-------------|
| `0x14`  | Cell 1 Voltage  | mV    | VC1 - VC0   |
| `0x16`  | Cell 2 Voltage  | mV    | VC2 - VC1   |
| `0x18`  | Cell 3 Voltage  | mV    | VC3 - VC2   |
| `0x1A`  | Cell 4 Voltage  | mV    | VC4 - VC3   |
| `0x1C`  | Cell 5 Voltage  | mV    | VC5 - VC4   |
| `0x1E`  | Cell 6 Voltage  | mV    | VC6 - VC5   |
| `0x20`  | Cell 7 Voltage  | mV    | VC7 - VC6   |
| `0x22`  | Cell 8 Voltage  | mV    | VC8 - VC7   |
| `0x24`  | Cell 9 Voltage  | mV    | VC9 - VC8   |
| `0x26`  | Cell 10 Voltage | mV    | VC10 - VC9  |

Each is a 16-bit signed integer (I2), little-endian, spanning 2 bytes. Read low byte at address, high byte at address+1.

## 2. Stack and Pin Voltages (16-bit, Direct Commands)

| Command | Name             | Units | Description                              |
|---------|------------------|-------|------------------------------------------|
| `0x34`  | Stack Voltage    | userV | VC10 (top of stack) via internal divider |
| `0x36`  | PACK Pin Voltage | userV | PACK pin voltage via internal divider    |
| `0x38`  | LD Pin Voltage   | userV | LD pin voltage via internal divider      |

`userV` unit = programmable via `Settings:Configuration:DA Configuration`

## 3. Current Measurement (16-bit, Direct Command)

| Command | Name        | Units | Description                       |
|---------|-------------|-------|-----------------------------------|
| `0x3A`  | CC2 Current | userA | 16-bit signed CC2 filtered current |

### userA Unit Configuration

Register: `Settings:Configuration:DA Configuration[USER_AMPS_1:0]`

| USER_AMPS_1 | USER_AMPS_0 | Unit    |
|-------------|-------------|---------|
| 0           | 0           | 0.1 mA  |
| 0           | 1           | 1 mA    |
| 1           | 0           | 10 mA   |
| 1           | 1           | 100 mA  |

- Range: -32768 to +32767 in userA units
- Positive = charging current, Negative = discharging current
- Sense resistor connected between SRP and SRN pins

### CC Gain Formula

```
CC Gain = 10^6 x VREF2 / (5 x 32768 x Rsense_mOhm)
Nominal: CC Gain = 7.5684 / (Rsense in mOhm)
```

## 4. Temperature Measurements (16-bit, Direct Commands)

All temperatures in units of 0.1 K (deciKelvin).
**Conversion:** `Celsius = (value * 0.1) - 273.15`

| Command | Name                | Units | Source                  |
|---------|---------------------|-------|-------------------------|
| `0x68`  | Int Temperature     | 0.1 K | Internal die            |
| `0x6A`  | CFETOFF Temperature | 0.1 K | CFETOFF pin thermistor  |
| `0x6C`  | DFETOFF Temperature | 0.1 K | DFETOFF pin thermistor  |
| `0x6E`  | ALERT Temperature   | 0.1 K | ALERT pin thermistor    |
| `0x70`  | TS1 Temperature     | 0.1 K | TS1 pin thermistor      |
| `0x72`  | TS2 Temperature     | 0.1 K | TS2 pin thermistor      |
| `0x74`  | TS3 Temperature     | 0.1 K | TS3 pin thermistor      |
| `0x76`  | HDQ Temperature     | 0.1 K | HDQ pin thermistor      |
| `0x78`  | DCHG Temperature    | 0.1 K | DCHG pin thermistor     |
| `0x7A`  | DDSG Temperature    | 0.1 K | DDSG pin thermistor     |

> When pin configured as ADCIN instead of thermistor, the temperature command returns the pin voltage in mV (signed 16-bit).

### Thermistor Pullup Options

| Pullup   | Target NTC                                  |
|----------|---------------------------------------------|
| 18 kOhm  | ~10 kOhm NTC (e.g., Semitec 103-AT)        |
| 180 kOhm | ~200 kOhm NTC (e.g., Semitec 204AP-2)      |
> Thermistor pullup options are 18 kOhm or 180 kOhm internal, and are selectable per pin.

## 5. Internal Temperature Formula

```
Int Temp (0.1 K) = (ADC value) x Calibration:Internal Temp Model:Int Gain / 65536
                   + Calibration:Internal Temp Model:Int base offset
                   + Calibration:Temperature:Internal Temp Offset
```

## 6. Cell Voltage Calibration Formulas

### Reported Voltage Formulas

```
Cell # Voltage()   = Calibration:Voltage:Cell # Gain x (16-bit ADC counts) / 65536
                     - Calibration:Vcell Offset:Vcell Offset

Stack Voltage()    = Calibration:Voltage:TOS Gain x (16-bit ADC counts) / 65536
                     - Calibration:Vdiv Offset:Vdiv Offset

PACK Pin Voltage() = Calibration:Voltage:Pack Gain x (16-bit ADC counts) / 65536
                     - Calibration:Vdiv Offset:Vdiv Offset

LD Pin Voltage()   = Calibration:Voltage:LD Gain x (16-bit ADC counts) / 65536
                     - Calibration:Vdiv Offset:Vdiv Offset

ADCIN Voltage      = Calibration:Voltage:ADC Gain x (16-bit ADC counts) / 65536
```

### Calibration Gain Calculation (from two known voltages)

```
Cell Gain = 2^24 x (Voltage_1_mV - Voltage_2_mV)
            / (32-bit ADC counts at V1 - 32-bit ADC counts at V2)

Cell Offset = (Cell Gain x 32-bit ADC counts at V2) / 2^24 - Voltage_2_mV

TOS/PACK/LD Gain = 2^16 x (Voltage_1_cV - Voltage_2_cV)
                   / (16-bit ADC counts at V1 - 16-bit ADC counts at V2)
```

### Nominal Gains (VREF1 = 1.212V)

| Measurement | Nominal Gain |
|-------------|-------------|
| Cell        | 12120       |
| ADCIN       | 4040        |

## 7. Raw ADC Data (32-bit, via Subcommands)

Available through DASTATUS1-3 subcommands for synchronized voltage + current.

### 0x0071 DASTATUS1() - 32 bytes

| Bytes   | Name                 | Unit              |
|---------|----------------------|-------------------|
| 0-3     | Cell 1 Voltage Counts | 32-bit signed ADC |
| 4-7     | Cell 1 Current Counts | 32-bit signed ADC |
| 8-11    | Cell 2 Voltage Counts | 32-bit signed ADC |
| 12-15   | Cell 2 Current Counts | 32-bit signed ADC |
| 16-19   | Cell 3 Voltage Counts | 32-bit signed ADC |
| 20-23   | Cell 3 Current Counts | 32-bit signed ADC |
| 24-27   | Cell 4 Voltage Counts | 32-bit signed ADC |
| 28-31   | Cell 4 Current Counts | 32-bit signed ADC |

### 0x0072 DASTATUS2() - 32 bytes

| Bytes   | Name                 | Unit              |
|---------|----------------------|-------------------|
| 0-3     | Cell 5 Voltage Counts | 32-bit signed ADC |
| 4-7     | Cell 5 Current Counts | 32-bit signed ADC |
| 8-11    | Cell 6 Voltage Counts | 32-bit signed ADC |
| 12-15   | Cell 6 Current Counts | 32-bit signed ADC |
| 16-19   | Cell 7 Voltage Counts | 32-bit signed ADC |
| 20-23   | Cell 7 Current Counts | 32-bit signed ADC |
| 24-27   | Cell 8 Voltage Counts | 32-bit signed ADC |
| 28-31   | Cell 8 Current Counts | 32-bit signed ADC |

### 0x0073 DASTATUS3() - 16 bytes used

| Bytes   | Name                  | Unit              |
|---------|-----------------------|-------------------|
| 0-3     | Cell 9 Voltage Counts  | 32-bit signed ADC |
| 4-7     | Cell 9 Current Counts  | 32-bit signed ADC |
| 8-11    | Cell 10 Voltage Counts | 32-bit signed ADC |
| 12-15   | Cell 10 Current Counts | 32-bit signed ADC |
| 16-31   | Reserved               | -                 |

### LSB Values

| Measurement           | LSB Value                                              |
|-----------------------|--------------------------------------------------------|
| 32-bit cell voltage   | 5 x VREF1 / 2^23 = 5 x 1.212 / 2^23 ~ **0.722 uV**  |
| 32-bit current counts | VREF2 / (5 x 2^23) = 1.24 / (5 x 2^23) ~ **29.56 nV** |

> 24-bit raw data sign-extended to 32 bits (lower 3 bytes contain data).

## 8. Additional Measurements - 0x0075 DASTATUS5()

| Bytes   | Name                 | Unit              |
|---------|----------------------|-------------------|
| 0-1     | V_REG18              | 16-bit ADC counts |
| 2-3     | VSS                  | 16-bit ADC counts |
| 4-5     | Max Cell Voltage     | mV                |
| 6-7     | Min Cell Voltage     | mV                |
| 8-9     | Battery Voltage Sum  | cV (10 mV)        |
| 10-11   | Avg Cell Temperature | 0.1 K             |
| 12-13   | FET Temperature      | 0.1 K             |
| 14-15   | Max Cell Temperature | 0.1 K             |
| 16-17   | Min Cell Temperature | 0.1 K             |
| 18-19   | Avg Cell Temperature | 0.1 K             |
| 20-21   | CC3 Current          | userA              |
| 22-23   | CC1 Current          | userA              |
| 24-27   | CC2 Counts           | 32-bit raw ADC     |
| 28-31   | CC3 Counts           | 32-bit raw ADC     |

## 9. Accumulated Charge - 0x0076 DASTATUS6()

| Bytes   | Name                                    | Unit                            |
|---------|-----------------------------------------|---------------------------------|
| 0-3     | Accumulated charge (integer portion)    | 32-bit signed, userAh           |
| 4-7     | Accumulated charge (fractional portion) | 32-bit, init to 0.5 userAh      |
| 8-11    | Accumulated Time                        | 32-bit unsigned, seconds         |
| 12-15   | CFETOFF Counts                          | 32-bit raw ADC                   |
| 16-19   | DFETOFF Counts                          | 32-bit raw ADC                   |
| 20-23   | ALERT Counts                            | 32-bit raw ADC                   |
| 24-27   | TS1 Counts                              | 32-bit raw ADC                   |
| 28-31   | TS2 Counts                              | 32-bit raw ADC                   |

## 10. Pin ADC Counts - 0x0077 DASTATUS7()

| Bytes   | Name        | Unit           |
|---------|-------------|----------------|
| 0-3     | TS3 Counts  | 32-bit raw ADC |
| 4-7     | HDQ Counts  | 32-bit raw ADC |
| 8-11    | DCHG Counts | 32-bit raw ADC |
| 12-15   | DDSG Counts | 32-bit raw ADC |
| 16-31   | Reserved    | -              |

### Raw ADC LSB Values

| Pin Mode    | LSB Value                                                    |
|-------------|--------------------------------------------------------------|
| Thermistor  | 5/3 x 1.8V / 2^23 ~ **0.358 uV**                           |
| ADCIN       | 5/3 x VREF1 / 2^23 = 5/3 x 1.212 / 2^23 ~ **0.241 uV**    |

## 11. Voltage Measurement Schedule

Measurement loop: all 10 cells, then VC10/PACK/LD, then temp/Vref/VSS, then thermistors.
Full scan = 3 loops. One loop = 12-15 measurement slots.

- Each slot: 3 ms (or 1.5 ms with `FASTADC` bit set)
- Typical loop (15 slots): 45 ms (or 22.5 ms with `FASTADC`)

### Loop Speed Control

Register: `Settings:Configuration:Power Config[LOOP_SLOW_1:0]`

| LOOP_SLOW_1 | LOOP_SLOW_0 | Cycle Time |
|-------------|-------------|------------|
| 0           | 0           | 45 ms      |
| 0           | 1           | 90 ms      |
| 1           | 0           | 180 ms     |
| 1           | 1           | 360 ms     |

## 12. Coulomb Counter Filters

| Filter | Bits  | Output Rate                                | Purpose              |
|--------|-------|--------------------------------------------|----------------------|
| CC1    | 16-bit | Every 250 ms (NORMAL mode)                | Charge integration   |
| CC2    | 24-bit | Every 3 ms (or 1.5 ms with FASTADC)      | Current reporting    |
| CC3    | 16-bit | Programmable average of CC2 (up to 255 samples) | Averaged current |

- CC3 sample count configured by `Settings:Configuration:CC3 Samples`
- CC2 reported as 16-bit via `0x3A` CC2 Current() direct command
- CC2 32-bit raw available in DASTATUS5() bytes 24-27
- CC3 16-bit reported in DASTATUS5() bytes 20-21
- CC1 16-bit reported in DASTATUS5() bytes 22-23
