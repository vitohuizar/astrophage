# BQ76942 - Direct Commands Table

> Source: BQ76942 Technical Reference Manual (SLUUBY1B), Section 12.1

All direct commands use 7-bit register addresses. Data format: little-endian byte order.

**Type key:** H1 = 1-byte hex, H2 = 2-byte hex, I2 = 2-byte signed integer, U2 = 2-byte unsigned

## Direct Commands (Table 12-1)

| Addr   | Name                | Units | Type | Access (Sealed/Unsealed/Full) | Description                              |
|--------|---------------------|-------|------|-------------------------------|------------------------------------------|
| `0x00` | Control Status      | Hex   | H2   | R-W / R-W / R-W              | Device status bits. Behaves like 0x3E/0x3F on write.                       |
| `0x02` | Safety Alert A      | Hex   | H1   | R / R / R                    | Safety alert flags (current faults)      |
| `0x03` | Safety Status A     | Hex   | H1   | R / R / R                    | Safety fault flags (latched faults)      |
| `0x04` | Safety Alert B      | Hex   | H1   | R / R / R                    | Temperature safety alerts                |
| `0x05` | Safety Status B     | Hex   | H1   | R / R / R                    | Temperature safety faults                |
| `0x06` | Safety Alert C      | Hex   | H1   | R / R / R                    | OCD3/SCDL/OCDL/COVL alerts               |
| `0x07` | Safety Status C     | Hex   | H1   | R / R / R                    | OCD3/SCDL/OCDL/COVL faults               |
| `0x0A` | PF Alert A          | Hex   | H1   | R / R / R                    | Permanent Fail alerts A                  |
| `0x0B` | PF Status A         | Hex   | H1   | R / R / R                    | Permanent Fail faults A                  |
| `0x0C` | PF Alert B          | Hex   | H1   | R / R / R                    | Permanent Fail alerts B                  |
| `0x0D` | PF Status B         | Hex   | H1   | R / R / R                    | Permanent Fail faults B                  |
| `0x0E` | PF Alert C          | Hex   | H1   | R / R / R                    | Permanent Fail alerts C                  |
| `0x0F` | PF Status C         | Hex   | H1   | R / R / R                    | Permanent Fail faults C                  |
| `0x10` | PF Alert D          | Hex   | H1   | R / R / R                    | Permanent Fail alerts D                  |
| `0x11` | PF Status D         | Hex   | H1   | R / R / R                    | Permanent Fail faults D                  |
| `0x12` | Battery Status      | Hex   | H2   | R / R / R                    | Battery status flags                     |
| `0x14` | Cell 1 Voltage      | mV    | I2   | R / R / R                    | 16-bit cell 1 voltage                   |
| `0x16` | Cell 2 Voltage      | mV    | I2   | R / R / R                    | 16-bit cell 2 voltage                   |
| `0x18` | Cell 3 Voltage      | mV    | I2   | R / R / R                    | 16-bit cell 3 voltage                   |
| `0x1A` | Cell 4 Voltage      | mV    | I2   | R / R / R                    | 16-bit cell 4 voltage                   |
| `0x1C` | Cell 5 Voltage      | mV    | I2   | R / R / R                    | 16-bit cell 5 voltage                   |
| `0x1E` | Cell 6 Voltage      | mV    | I2   | R / R / R                    | 16-bit cell 6 voltage                   |
| `0x20` | Cell 7 Voltage      | mV    | I2   | R / R / R                    | 16-bit cell 7 voltage                   |
| `0x22` | Cell 8 Voltage      | mV    | I2   | R / R / R                    | 16-bit cell 8 voltage                   |
| `0x24` | Cell 9 Voltage      | mV    | I2   | R / R / R                    | 16-bit cell 9 voltage                   |
| `0x26` | Cell 10 Voltage     | mV    | I2   | R / R / R                    | 16-bit cell 10 voltage                  |
| `0x34` | Stack Voltage       | userV | I2   | R / R / R                    | 16-bit top-of-stack voltage              |
| `0x36` | PACK Pin Voltage    | userV | I2   | R / R / R                    | 16-bit PACK pin voltage                 |
| `0x38` | LD Pin Voltage      | userV | I2   | R / R / R                    | 16-bit LD pin voltage                   |
| `0x3A` | CC2 Current         | userA | I2   | R / R / R                    | 16-bit CC2 current                      |
| `0x62` | Alarm Status        | Hex   | H2   | R-W / R-W / R-W              | Latched alarm flags (write 1 to clear)   |
| `0x64` | Alarm Raw Status    | Hex   | H2   | R / R / R                    | Unlatched alarm flags                    |
| `0x66` | Alarm Enable        | Hex   | H2   | R-W / R-W / R-W              | Alarm enable mask                        |
| `0x68` | Int Temperature     | 0.1 K | I2   | R / R / R                    | Internal die temperature                 |
| `0x6A` | CFETOFF Temperature | 0.1 K | I2   | R / R / R                    | CFETOFF pin thermistor (or mV if ADCIN)  |
| `0x6C` | DFETOFF Temperature | 0.1 K | I2   | R / R / R                    | DFETOFF pin thermistor (or mV if ADCIN)  |
| `0x6E` | ALERT Temperature   | 0.1 K | I2   | R / R / R                    | ALERT pin thermistor (or mV if ADCIN)    |
| `0x70` | TS1 Temperature     | 0.1 K | I2   | R / R / R                    | TS1 pin thermistor (or mV if ADCIN)      |
| `0x72` | TS2 Temperature     | 0.1 K | I2   | R / R / R                    | TS2 pin thermistor (or mV if ADCIN)      |
| `0x74` | TS3 Temperature     | 0.1 K | I2   | R / R / R                    | TS3 pin thermistor (or mV if ADCIN)      |
| `0x76` | HDQ Temperature     | 0.1 K | I2   | R / R / R                    | HDQ pin thermistor (or mV if ADCIN)      |
| `0x78` | DCHG Temperature    | 0.1 K | I2   | R / R / R                    | DCHG pin thermistor (or mV if ADCIN)     |
| `0x7A` | DDSG Temperature    | 0.1 K | I2   | R / R / R                    | DDSG pin thermistor (or mV if ADCIN)     |
| `0x7F` | FET Status          | Hex   | H1   | R / R / R                    | FET and ALERT pin status                 |

> All 2-byte registers span two consecutive addresses (e.g., `0x14` and `0x15` for Cell 1). Read both bytes for a complete 16-bit value. Little-endian: low byte first.

## Register Bit Field Definitions

### Control Status Register (`0x00`)

| Bit | Field      | Description                                  |
|-----|------------|----------------------------------------------|
| 2   | DEEPSLEEP  | 1 = device in DEEPSLEEP mode                 |
| 1   | LD_TIMEOUT | 1 = Load Detect timed out                    |
| 0   | LD_ON      | 1 = LD pullup active during last measurement |

### Safety Alert A / Safety Status A (`0x02` / `0x03`)

| Bit | Field | Description                          |
|-----|-------|--------------------------------------|
| 7   | SCD   | Short Circuit in Discharge           |
| 6   | OCD2  | Overcurrent in Discharge 2nd Tier    |
| 5   | OCD1  | Overcurrent in Discharge 1st Tier    |
| 4   | OCC   | Overcurrent in Charge                |
| 3   | COV   | Cell Overvoltage                     |
| 2   | CUV   | Cell Undervoltage                    |

### Safety Alert B / Safety Status B (`0x04` / `0x05`)

| Bit | Field | Description                  |
|-----|-------|------------------------------|
| 7   | OTF   | FET Overtemperature          |
| 6   | OTINT | Internal Overtemperature     |
| 5   | OTD   | Overtemperature in Discharge |
| 4   | OTC   | Overtemperature in Charge    |
| 2   | UTINT | Internal Undertemperature    |
| 1   | UTD   | Undertemperature in Discharge|
| 0   | UTC   | Undertemperature in Charge   |

### Safety Alert C / Safety Status C (`0x06` / `0x07`)

| Bit | Field | Description                              |
|-----|-------|------------------------------------------|
| 7   | OCD3  | Overcurrent in Discharge 3rd Tier        |
| 6   | SCDL  | Short Circuit in Discharge Latch         |
| 5   | OCDL  | Overcurrent in Discharge Latch           |
| 4   | COVL  | Cell Overvoltage Latch                   |
| 2   | PTO   | Precharge Timeout (Status C only)        |
| 1   | HWDF  | Host Watchdog Fault (Status C only)      |

### Battery Status Register (`0x12`)

| Bit   | Field     | Description                                                                 |
|-------|-----------|-----------------------------------------------------------------------------|
| 15    | SLEEP     | Device in SLEEP mode                                                        |
| 13    | SD_CMD    | Shutdown pending                                                            |
| 12    | PF        | Permanent Fail triggered                                                    |
| 11    | SS        | Safety fault triggered                                                      |
| 10    | FUSE      | FUSE pin state                                                              |
| 9-8   | SEC1-SEC0 | Security state (0=uninit, 1=FULLACCESS, 2=UNSEALED, 3=SEALED)              |
| 7     | OTPB      | OTP blocked                                                                 |
| 6     | OTPW      | OTP write pending                                                           |
| 5     | COW_CHK   | Cell open-wire check active                                                 |
| 4     | WD        | Previous reset by watchdog                                                  |
| 3     | POR       | Power-on reset occurred                                                     |
| 2     | SLEEP_EN  | SLEEP mode allowed                                                          |
| 1     | PCHG_MODE | PRECHARGE mode active                                                       |
| 0     | CFGUPDATE | CONFIG_UPDATE mode active                                                   |

### Alarm Status / Alarm Raw Status (`0x62` / `0x64`)

| Bit | Field       | Description                       |
|-----|-------------|-----------------------------------|
| 15  | SSBC        | Safety Status B or C set          |
| 14  | SSA         | Safety Status A set               |
| 13  | PF          | Permanent Fail triggered          |
| 12  | MSK_SFALERT | Masked safety alert               |
| 11  | MSK_PFALERT | Masked PF alert                   |
| 10  | INITSTART   | Initialization started            |
| 9   | INITCOMP    | Initialization completed          |
| 7   | FULLSCAN    | Full voltage scan complete         |
| 6   | XCHG        | CHG FET off                       |
| 5   | XDSG        | DSG FET off                       |
| 4   | SHUTV       | Stack voltage below shutdown threshold |
| 3   | FUSE        | FUSE pin driven                   |
| 2   | CB          | Cell balancing active             |
| 1   | ADSCAN      | Voltage ADC scan complete         |
| 0   | WAKE        | Woke from SLEEP                   |

### FET Status Register (`0x7F`)

| Bit | Field    | Description           |
|-----|----------|-----------------------|
| 6   | ALRT_PIN | ALERT pin asserted    |
| 5   | DDSG_PIN | DDSG pin asserted     |
| 4   | DCHG_PIN | DCHG pin asserted     |
| 3   | PDSG_FET | PDSG FET on           |
| 2   | DSG_FET  | DSG FET on            |
| 1   | PCHG_FET | PCHG FET on           |
| 0   | CHG_FET  | CHG FET on            |
