# BQ76942 - Subcommand Protocol (0x3E/0x40 Transfer Buffer)

> Source: BQ76942 Technical Reference Manual (SLUUBY1B), Sections 3.1, 12.3, 12.4

## 1. Overview

Subcommands use the 7-bit command address space indirectly via registers:

| Address       | Function                                              |
|---------------|-------------------------------------------------------|
| `0x3E`-`0x3F` | Subcommand address (16-bit LE: `0x3E`=LSB, `0x3F`=MSB) |
| `0x40`-`0x5F` | 32-byte transfer buffer (data payload)                |
| `0x60`        | Checksum                                              |
| `0x61`        | Data length                                           |

## 2. Reading Data from a Subcommand (Efficient Method)

1. Write lower byte of subcommand to `0x3E`
2. Write upper byte of subcommand to `0x3F`
3. Read `0x3E` and `0x3F`. If returns `0xFF`, subcommand not completed yet. When completed, readback returns original subcommand value. *(Only applies to subcommands that return data)*
4. Read length from `0x61`
5. Read buffer starting at `0x40` for the expected length
6. Read checksum at `0x60` and verify

### Alternative (simpler, more bus traffic)

1. Write lower byte of subcommand to `0x3E`
2. Write upper byte of subcommand to `0x3F`
3. Read `0x3E` and `0x3F` (poll until != `0xFF`)
4. Read `0x40` to `0x61` in a block (reads all data + checksum + length)

## 3. Writing Data to a Subcommand

1. Write lower byte of subcommand to `0x3E`
2. Write upper byte of subcommand to `0x3F`
3. Write new data into transfer buffer starting at `0x40`
4. Write checksum to `0x60`
5. Write data length to `0x61`

> Checksum and length **MUST** be written together as a word (2 bytes). The device validates as soon as `0x61` is written.

## 4. Checksum Calculation

```
Checksum = ~(sum of bytes) & 0xFF
```

The checksum is the 8-bit sum of:
- The two subcommand bytes (`0x3E` and `0x3F` values)
- All bytes used in the transfer buffer (`0x40` to `0x40+N-1`)

Then the result is **bitwise inverted** (`~`).

The checksum does **NOT** include:
- The checksum byte itself (`0x60`)
- The length byte (`0x61`)

**Example:** subcommand `0x0071`, buffer has 32 bytes of data:
```
sum = 0x71 + 0x00 + buffer[0] + buffer[1] + ... + buffer[31]
checksum = (~sum) & 0xFF
```

## 5. Data Length Format

`0x61` contains: **length of buffer data + 4**

The "+4" accounts for:
- 2 bytes at `0x3E`-`0x3F` (subcommand)
- 2 bytes at `0x60`-`0x61` (checksum + length)

| Buffer bytes used | Length value (`0x61`) |
|-------------------|----------------------|
| 32 (full buffer)  | `0x24` (36)          |
| 2                 | `0x06` (6)           |
| 4                 | `0x08` (8)           |

## 6. Command-Only Subcommands (No Data Transfer)

For subcommands that only trigger an action (no data read/write), simply write the subcommand to `0x3E` and `0x3F`. No need to write length or checksum.

| Addr     | Name              | Access           | Description                                  |
|----------|-------------------|------------------|----------------------------------------------|
| `0x000E` | EXIT_DEEPSLEEP    | Sealed:W         | Exit DEEPSLEEP mode                          |
| `0x000F` | DEEPSLEEP         | Sealed:W         | Enter DEEPSLEEP (send twice in 4s)           |
| `0x0010` | SHUTDOWN          | Sealed:W         | Start shutdown (send twice in 4s if sealed)  |
| `0x0012` | RESET             | Unsealed:W       | Reset device                                 |
| `0x001C` | PDSGTEST          | Unsealed:W       | Toggle PDSG FET (FET Test mode)              |
| `0x001D` | FUSE_TOGGLE       | Unsealed:W       | Toggle FUSE state                            |
| `0x001E` | PCHGTEST          | Unsealed:W       | Toggle PCHG FET (FET Test mode)              |
| `0x001F` | CHGTEST           | Unsealed:W       | Toggle CHG FET (FET Test mode)               |
| `0x0020` | DSGTEST           | Unsealed:W       | Toggle DSG FET (FET Test mode)               |
| `0x0022` | FET_ENABLE        | Unsealed:W       | Toggle FET_EN in Mfg Status                  |
| `0x0024` | PF_ENABLE         | Unsealed:W       | Toggle PF_EN in Mfg Status                   |
| `0x0030` | SEAL              | Unsealed:W       | Enter SEALED mode                            |
| `0x0082` | RESET_PASSQ       | Sealed:W         | Reset charge integration and timer           |
| `0x008A` | PTO_RECOVER       | Sealed:W         | Recover from Precharge Timeout               |
| `0x0090` | SET_CFGUPDATE     | Unsealed:W       | Enter CONFIG_UPDATE mode                     |
| `0x0092` | EXIT_CFGUPDATE    | Sealed:W         | Exit CONFIG_UPDATE mode                      |
| `0x0093` | DSG_PDSG_OFF      | Sealed:W         | Disable DSG and PDSG FETs                    |
| `0x0094` | CHG_PCHG_OFF      | Sealed:W         | Disable CHG and PCHG FETs                    |
| `0x0095` | ALL_FETS_OFF      | Sealed:W         | Disable all FETs                             |
| `0x0096` | ALL_FETS_ON       | Sealed:W         | Enable all FETs                              |
| `0x0097` | FET_CONTROL       | Sealed:W         | Control individual FETs (8-bit field)        |
| `0x0098` | REG12_CONTROL     | Sealed:W         | Control REG1/REG2 LDOs                       |
| `0x0099` | SLEEP_ENABLE      | Sealed:W         | Enable SLEEP mode                            |
| `0x009A` | SLEEP_DISABLE     | Sealed:W         | Disable SLEEP mode                           |
| `0x009B` | OCDL_RECOVER      | Sealed:W         | Recover from OCDL                            |
| `0x009C` | SCDL_RECOVER      | Sealed:W         | Recover from SCDL                            |
| `0x29BC` | SWAP_COMM_MODE    | Unsealed:W       | Switch to configured comm mode               |
| `0x29E7` | SWAP_TO_I2C       | Unsealed:W       | Switch to I2C Fast mode                      |
| `0x7C35` | SWAP_TO_SPI       | Unsealed:W       | Switch to SPI with CRC                       |
| `0x7C40` | SWAP_TO_HDQ       | Unsealed:W       | Switch to HDQ mode                           |

## 7. Subcommands with Data

| Addr     | Name                 | Access    | Offset | Data                       | Type | Description                  |
|----------|----------------------|-----------|--------|----------------------------|------|------------------------------|
| `0x0001` | DEVICE_NUMBER        | R         | 0      | Device Number              | U2   | Device ID                    |
| `0x0002` | FW_VERSION           | R         | 0      | Dev Num (Big-Endian)       | U2   |                              |
|          |                      |           | 2      | FW Version (Big-Endian)    | U2   | Major.Minor                  |
|          |                      |           | 4      | Build Number (Big-Endian)  | U2   | BCD format                   |
| `0x0003` | HW_VERSION           | R         | 0      | Hardware Version           | U2   | HW revision                  |
| `0x0004` | IROM_SIG             | R         | 0      | IROM Signature             | U2   | Instruction ROM sig          |
| `0x0005` | STATIC_CFG_SIG       | R         | 0      | Static Config Sig          | U2   | Config data sig              |
| `0x0009` | DROM_SIG             | R         | 0      | Data ROM Signature         | U2   | Data ROM sig                 |
| `0x0035` | SECURITY_KEYS        | R/W(Full) | 0      | Unseal Key Step 1          | U2   |                              |
|          |                      |           | 2      | Unseal Key Step 2          | U2   |                              |
|          |                      |           | 4      | Full Access Key Step 1     | U2   |                              |
|          |                      |           | 6      | Full Access Key Step 2     | U2   |                              |
| `0x0053` | SAVED_PF_STATUS      | R         | 0      | PF Status A                | U1   |                              |
|          |                      |           | 1      | PF Status B                | U1   |                              |
|          |                      |           | 2      | PF Status C                | U1   |                              |
|          |                      |           | 3      | PF Status D                | U1   |                              |
|          |                      |           | 4      | Fuse Flag                  | U1   |                              |
| `0x0057` | MANUFACTURING_STATUS | R         | 0      | Manufacturing Status       | H2   |                              |
| `0x0070` | MANU_DATA            | R/R/R-W   | 0-31   | Manufacturer Data 0-31     | U1   | 32-byte scratchpad           |
| `0x0071` | DASTATUS1            | R         | 0-31   | Cell 1-4 V+I Cnts         | I4   | 32-bit each, synchronized    |
| `0x0072` | DASTATUS2            | R         | 0-31   | Cell 5-8 V+I Cnts         | I4   | 32-bit each, synchronized    |
| `0x0073` | DASTATUS3            | R         | 0-15   | Cell 9-10 V+I Cnts        | I4   | 32-bit each, synchronized    |
| `0x0075` | DASTATUS5            | R         | 0-31   | Additional measurements    | -    | See ADC section              |
| `0x0076` | DASTATUS6            | R         | 0-31   | Accumulated charge + ADC   | -    | See ADC section              |
| `0x0077` | DASTATUS7            | R         | 0-15   | TS3/HDQ/DCHG/DDSG counts  | I4   | 32-bit raw ADC               |
| `0x0080` | CUV_SNAPSHOT         | R         | 0-19   | Cell voltages at CUV       | I2   | mV per cell                  |
| `0x0081` | COV_SNAPSHOT         | R         | 0-19   | Cell voltages at COV       | I2   | mV per cell                  |
| `0x0083` | CB_ACTIVE_CELLS      | R/W       | 0      | Cell bitmask               | U2   | Write 0 to stop balancing    |
| `0x0084` | CB_SET_LVL           | R/W       | 0      | Voltage threshold          | U2   | mV, balance cells above this |
| `0x0085` | CBSTATUS1            | R         | 0      | Balancing active time      | U2   | Seconds                      |
| `0x0086` | CBSTATUS2            | R         | 0-31   | Per-cell balance time 1-8  | U4   | 32-bit seconds each          |
| `0x0087` | CBSTATUS3            | R         | 0-7    | Per-cell balance time 9-10 | U4   | 32-bit seconds each          |

## 8. Auto-Populate Behavior

When a subcommand is initiated, the device auto-populates the transfer buffer (`0x40`-`0x5F`) with existing data and writes the checksum to `0x60`. If the host intends to **read**, this data is ready after the subcommand completes. If the host intends to **write**, it overwrites the buffer, checksum, and length.
