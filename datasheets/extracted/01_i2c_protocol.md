# BQ76942 - I2C Communication Protocol

> Source: BQ76942 Technical Reference Manual (SLUUBY1B), Chapter 9

## 1. I2C Address

- Default address: `0x10` (write), `0x11` (read)
- 7-bit address = `0x08` (the 0x10/0x11 includes the R/W bit)
- Configurable via: `Settings:Configuration:I2C Address`

## 2. Comm Type Settings

Register: `Settings:Configuration:Comm Type`

| Value  | Mode                                                          |
|--------|---------------------------------------------------------------|
| `0x00` | Default (I2C Fast on BQ76942, varies for other versions)      |
| `0x07` | I2C (up to 100 kHz bus speed)                                 |
| `0x08` | I2C Fast (above 100 kHz bus speed)                            |
| `0x09` | I2C Fast with timeouts (above 100 kHz)                        |
| `0x11` | I2C with CRC (up to 100 kHz)                                  |
| `0x12` | I2C Fast with CRC (above 100 kHz)                             |
| `0x1E` | I2C with timeouts (100 kHz)                                   |
| `0xFF` | I2C Fast (above 100 kHz)                                      |

## 3. I2C Write Transaction

```
[START] [Addr+W] [ACK] [RegAddr] [ACK] [Data] [ACK] [CRC(opt)] [ACK] [STOP]
```

1. START condition
2. Responder address byte (`0x10` for write) - 7 bits + W bit
3. ACK from device
4. Register address (7-bit command address)
5. ACK from device
6. Data byte(s) - auto-increments register address per byte
7. ACK from device per data byte
8. Optional CRC byte after data
9. STOP condition

Block writes are allowed by sending additional data bytes before STOP. Register address auto-increments after each data byte.

## 4. I2C Read Transaction (Repeated Start)

```
[START] [Addr+W] [ACK] [RegAddr] [ACK] [RepSTART] [Addr+R] [ACK] [Data] [ACK] [CRC(opt)] [NACK] [STOP]
```

1. START condition
2. Responder address byte (`0x10` for write)
3. ACK from device
4. Register address
5. ACK from device
6. REPEATED START condition
7. Responder address byte (`0x11` for read)
8. ACK from device
9. Data byte(s) driven by responder
10. Controller ACKs each byte except last
11. Optional CRC byte driven by responder
12. Controller NACKs the last byte/CRC
13. STOP condition

## 5. I2C Read Transaction (Without Repeated Start)

```
[START] [Addr+W] [ACK] [RegAddr] [ACK] [STOP]
[START] [Addr+R] [ACK] [Data] [ACK] [CRC(opt)] [NACK] [STOP]
```

Two separate transactions. Register address auto-increments on block read.

## 6. CRC Calculation

- **Polynomial:** x^8 + x^2 + x + 1 (CRC-8, same as SMBus PEC)
- **Initial value:** 0

### CRC for Write Transactions

| Scenario                    | CRC calculated over                              |
|-----------------------------|--------------------------------------------------|
| Single-byte write           | `{responder_address, register_address, data}`    |
| Block write, first byte     | `{responder_address, register_address, data}`    |
| Block write, subsequent     | `{data_byte}` only                               |

### CRC for Read Transactions

| Scenario                    | CRC calculated over                                              |
|-----------------------------|------------------------------------------------------------------|
| Single-byte read            | `{responder_addr_W, register_addr, responder_addr_R, data}`     |
| Block read, first byte      | `{responder_addr_W, register_addr, responder_addr_R, data}`     |
| Block read, subsequent      | `{data_byte}` only                                               |

CRC resets after each data byte and after each stop.

### On Bad CRC

- **Write:** responder NACKs, goes to idle state
- **Read:** controller NACKs, responder goes to idle state

## 7. Timeout Behavior

| Comm Type | Condition                                | Action          |
|-----------|------------------------------------------|-----------------|
| `0x1E`    | Clock low > 25-35 ms                     | Reset interface |
| `0x1E`    | Cumulative clock low responder extend > ~25 ms | Reset interface |
| `0x1E`    | Cumulative clock low controller extend > 10 ms | Reset interface |
| `0x09`    | Clock low > 5-20 ms                      | Reset interface |
| All modes | SCL low > 2 seconds                      | Long-term timeout reset |

## 8. Clock Stretching

- Device may clock stretch during read transactions while fetching data.
- **Exception:** subcommand data fetch to 0x40-0x5F buffer does NOT clock stretch.
- Host must wait appropriate time (see operation times below) before reading subcommand results.

## 9. Command/Subcommand Operation Times (approximate)

| Address         | Name                 | Time      |
|-----------------|----------------------|-----------|
| `0x00`          | Control Status()     | 50 us     |
| `0x02`-`0x07`   | Safety Alert/Status  | 50 us     |
| `0x0A`-`0x11`   | PF Alert/PF Status   | 50 us     |
| `0x12`          | Battery Status()     | 50 us     |
| `0x14`-`0x32`   | Cell Voltages()      | 50 us     |
| `0x34`          | Stack Voltage()      | 50 us     |
| `0x36`          | PACK Pin Voltage()   | 50 us     |
| `0x38`          | LD Pin Voltage()     | 50 us     |
| `0x3A`          | CC2 Current()        | 50 us     |
| `0x62`          | Alarm Status()       | 50 us     |
| `0x64`          | Alarm Raw Status()   | 50 us     |
| `0x66`          | Alarm Enable()       | 50 us     |
| `0x68`          | Int Temperature()    | 50 us     |
| `0x6A`-`0x7A`   | Thermistor Temps()   | 50 us     |
| `0x0001`        | DEVICE_NUMBER()      | 400 us    |
| `0x0002`        | FW_VERSION()         | 400 us    |
| `0x0003`        | HW_VERSION()         | 400 us    |
| `0x0004`        | IROM_SIG()           | 8500 us   |
| `0x0005`        | STATIC_CFG_SIG()     | 450 us    |
| `0x0009`        | DROM_SIG()           | 650 us    |
| `0x0071`-`0x0077` | DASTATUS1-7()      | 660 us    |
| `0x0090`        | SET_CFGUPDATE()      | 2000 us   |
| `0x0092`        | EXIT_CFGUPDATE()     | 1000 us   |
