# BQ76942 - Protection Configuration Registers and Thresholds

> Source: BQ76942 Technical Reference Manual (SLUUBY1B), Chapter 5, Section 13.6

## 1. Protection Enable Registers

### Enabled Protections A (comparator-based)

| Bit    | Protection | Description                    |
|--------|------------|--------------------------------|
| [SCD]  | SCD        | Short Circuit in Discharge     |
| [OCD2] | OCD2       | Overcurrent in Discharge 2     |
| [OCD1] | OCD1       | Overcurrent in Discharge 1     |
| [OCC]  | OCC        | Overcurrent in Charge          |
| [COV]  | COV        | Cell Overvoltage               |
| [CUV]  | CUV        | Cell Undervoltage              |

### Enabled Protections B (firmware-based)

| Bit     | Protection | Description                    |
|---------|------------|--------------------------------|
| [OTF]   | OTF        | FET Overtemperature            |
| [OTINT] | OTINT      | Internal Overtemperature       |
| [OTD]   | OTD        | Overtemperature in Discharge   |
| [OTC]   | OTC        | Overtemperature in Charge      |
| [UTINT] | UTINT      | Internal Undertemperature      |
| [UTD]   | UTD        | Undertemperature in Discharge  |
| [UTC]   | UTC        | Undertemperature in Charge     |

### Enabled Protections C (firmware-based, latching)

| Bit    | Protection | Description                        |
|--------|------------|------------------------------------|
| [OCD3] | OCD3       | Overcurrent in Discharge 3         |
| [SCDL] | SCDL       | Short Circuit in Discharge Latch   |
| [OCDL] | OCDL       | Overcurrent in Discharge Latch     |
| [COVL] | COVL       | Cell Overvoltage Latch             |
| [PTO]  | PTO        | Precharge Timeout                  |
| [HWDF] | HWDF       | Host Watchdog Fault                |

## 2. FET Control on Fault

| Register                                    | Function                          |
|---------------------------------------------|-----------------------------------|
| `Settings:Protection:CHG FET Protections A/B/C` | Which faults disable CHG FET  |
| `Settings:Protection:DSG FET Protections A/B/C` | Which faults disable DSG FET  |

> Disabling CHG also disables PCHG; disabling DSG also disables PDSG.

- For immediate CHG FET action: `CHG FET Protections A` = `0x18` or `0x98`
- For immediate DSG FET action: `DSG FET Protections A` = `0x80` or `0xE4`

## 3. Cell Overvoltage Protection (COV)

| Register                            | Range            | Step   | Units |
|-------------------------------------|------------------|--------|-------|
| `Protections:COV:Threshold`         | 1.0V - 5.5V      | 50 mV  | mV    |
| `Protections:COV:Delay`             | 10 ms - 6762 ms  | 3.3 ms | ms    |
| `Protections:COV:Recovery Hysteresis` | 100 mV - 1.0V  | 50 mV  | mV    |
| `Protections:Recovery:Time`         | configurable     | -      | sec   |

> Actual delay = 3.3 ms x (2 + setting). `0x0` disables.

### COV Latch (COVL)

| Register                            | Description                 |
|-------------------------------------|-----------------------------|
| `Protections:COVL:Latch Limit`      | Latch count limit           |
| `Protections:COVL:Counter Dec Delay` | Counter decrement interval |
| `Protections:COVL:Recovery Time`    | Latch recovery time         |

### COV Operation

| Status  | Condition                                                          | Action                                        |
|---------|--------------------------------------------------------------------|-----------------------------------------------|
| Normal  | Max cell < `COV:Threshold`                                         | Decrement COVL counter                        |
| Alert   | Max cell = `COV:Threshold`                                         | Safety Alert A[COV] = 1                       |
| Trip    | Persists for `COV:Delay`                                           | Safety Status A[COV] = 1, CHG FET off         |
| Recover | Max cell < (`COV:Threshold` - `Recovery Hysteresis`) for `Recovery:Time` | Safety Status A[COV] = 0                |

## 4. Cell Undervoltage Protection (CUV)

| Register                            | Range            | Step   | Units |
|-------------------------------------|------------------|--------|-------|
| `Protections:CUV:Threshold`         | 1.0V - 4.5V      | 50 mV  | mV    |
| `Protections:CUV:Delay`             | 10 ms - 6765 ms  | 3.3 ms | ms    |
| `Protections:CUV:Recovery Hysteresis` | 100 mV - 1.0V  | 50 mV  | mV    |

> Actual delay = 3.3 ms x (2 + setting). `0x0` disables.

### CUV Operation

| Status  | Condition                                                          | Action                                        |
|---------|--------------------------------------------------------------------|-----------------------------------------------|
| Normal  | Min cell > `CUV:Threshold`                                         | -                                             |
| Alert   | Min cell = `CUV:Threshold`                                         | Safety Alert A[CUV] = 1                       |
| Trip    | Persists for `CUV:Delay`                                           | Safety Status A[CUV] = 1, DSG FET off         |
| Recover | Min cell > (`CUV:Threshold` + `Recovery Hysteresis`) for `Recovery:Time` | Safety Status A[CUV] = 0                |

## 5. Short Circuit in Discharge (SCD)

| Register                   | Range                                                                 | Step  | Units |
|----------------------------|-----------------------------------------------------------------------|-------|-------|
| `Protections:SCD:Threshold` | 10, 20, 40, 60, 80, 100, 125, 150, 175, 200, 250, 300, 350, 400, 450, 500 | -     | mV    |
| `Protections:SCD:Delay`    | fastest, or 15-450 us                                                  | 15 us | us    |

> `0x0` disables. "Fastest" = comparator only, < 1 us.

### SCD Latch (SCDL)

| Register                            | Description                      |
|-------------------------------------|----------------------------------|
| `Protections:SCDL:Latch Limit`      | Latch count limit               |
| `Protections:SCDL:Counter Dec Delay` | Counter decrement interval      |
| `Protections:SCDL:Recovery Threshold` | Current threshold for recovery |
| `Protections:SCDL:Recovery Time`    | Latch recovery time              |

## 6. Overcurrent in Charge (OCC)

| Register                        | Range          | Step   | Units |
|---------------------------------|----------------|--------|-------|
| `Protections:OCC:Threshold`     | 4 mV - 124 mV  | 2 mV   | mV    |
| `Protections:OCC:Delay`         | 10 ms - 426 ms  | 3.3 ms | ms    |
| `Protections:OCC:PACK-TOS Delta` | -             | -      | mV    |
| `Protections:OCC:Recovery Threshold` | -          | -      | userA |

> Actual delay = 3.3 ms x (2 + setting). `0x0` disables.

## 7. Overcurrent in Discharge 1 (OCD1)

| Register                    | Range          | Step   | Units |
|-----------------------------|----------------|--------|-------|
| `Protections:OCD1:Threshold` | 4 mV - 200 mV | 2 mV   | mV    |
| `Protections:OCD1:Delay`    | 10 ms - 426 ms | 3.3 ms | ms    |

> Actual delay = 3.3 ms x (2 + setting). `0x0` disables.

## 8. Overcurrent in Discharge 2 (OCD2)

| Register                    | Range          | Step   | Units |
|-----------------------------|----------------|--------|-------|
| `Protections:OCD2:Threshold` | 4 mV - 200 mV | 2 mV   | mV    |
| `Protections:OCD2:Delay`    | 10 ms - 426 ms | 3.3 ms | ms    |

## 9. Overcurrent in Discharge 3 (OCD3) - firmware based

| Register                    | Range     | Step  | Units |
|-----------------------------|-----------|-------|-------|
| `Protections:OCD3:Threshold` | programmable (CC1 current) | - | userA |
| `Protections:OCD3:Delay`    | 0-255 sec | 1 sec | sec   |

### OCD Latch (OCDL)

| Register                             | Description                      |
|--------------------------------------|----------------------------------|
| `Protections:OCDL:Latch Limit`       | Latch count limit               |
| `Protections:OCDL:Counter Dec Delay`  | Counter decrement interval      |
| `Protections:OCDL:Recovery Threshold` | Current threshold for recovery  |
| `Protections:OCDL:Recovery Time`      | Latch recovery time             |

### OCD1/OCD2/OCD3 Recovery

| Register                          | Description               |
|-----------------------------------|---------------------------|
| `Protections:OCD:Recovery Threshold` | Charging current threshold |
| `Protections:Recovery:Time`       | Recovery duration          |

## 10. Temperature Protections Summary

| Protection | Register Prefix        | Threshold Range  | Step | Delay Range | Delay Step |
|------------|------------------------|------------------|------|-------------|------------|
| OTC        | `Protections:OTC:`     | -40C to 120C     | 1C   | 0-255 sec   | 1 sec      |
| OTD        | `Protections:OTD:`     | -40C to 120C     | 1C   | 0-255 sec   | 1 sec      |
| OTF        | `Protections:OTF:`     | 0C to 150C       | 1C   | 0-255 sec   | 1 sec      |
| OTINT      | `Protections:OTINT:`   | -40C to 120C     | 1C   | 0-255 sec   | 1 sec      |
| UTC        | `Protections:UTC:`     | -40C to 120C     | 1C   | 0-255 sec   | 1 sec      |
| UTD        | `Protections:UTD:`     | -40C to 120C     | 1C   | 0-255 sec   | 1 sec      |
| UTINT      | `Protections:UTINT:`   | -40C to 120C     | 1C   | 0-255 sec   | 1 sec      |

Each temperature protection has:
- `Threshold` - trigger temperature
- `Delay` - time before fault
- `Recovery` - recovery temperature threshold

## 11. Host Watchdog (HWD)

| Register                | Range         | Step  | Units |
|-------------------------|---------------|-------|-------|
| `Protections:HWD:Delay` | 0-65535 sec   | 1 sec | sec   |

Triggers when no communication received for `HWD_DLY` seconds.

## 12. Precharge Timeout (PTO)

| Register                          | Range       | Step  | Units |
|-----------------------------------|-------------|-------|-------|
| `Protections:PTO:Delay`           | 0-65535 sec | 1 sec | sec   |
| `Protections:PTO:Charge Threshold` | -          | -     | userA |
| `Protections:PTO:Reset`           | -           | -     | userAh|

## 13. Common Recovery Setting

| Register                   | Description                                    |
|----------------------------|------------------------------------------------|
| `Protections:Recovery:Time` | Shared recovery duration for multiple protections |

## 14. Body Diode Protection

| Register                                    | Description                                                |
|---------------------------------------------|------------------------------------------------------------|
| `Settings:Protection:Body Diode Threshold`  | Current threshold for body diode protection. When series FETs used and one FET is off, current through body diode above this threshold causes the off-FET to be temporarily turned on. |
