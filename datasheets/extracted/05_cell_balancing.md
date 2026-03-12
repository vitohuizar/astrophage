# BQ76942 - Cell Balancing Registers and Timing

> Source: BQ76942 Technical Reference Manual (SLUUBY1B), Chapter 10

## 1. Overview

Passive cell balancing via integrated bypass switches or external bypass FET switches.

| Mode             | Description                                              |
|------------------|----------------------------------------------------------|
| Autonomous       | Voltage-based algorithm, no host interaction required. Only non-adjacent cells in use are balanced. |
| Host-controlled  | Via subcommands. Adjacent and non-adjacent cells can be balanced. |

## 2. Host-Controlled Balancing Subcommands

| Subcommand               | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `0x0083` CB_ACTIVE_CELLS | **Read:** bitmask of cells being balanced. **Write:** bitmask to start balancing specified cells. Write `0x0000` to stop all balancing. Command may take ~1 sec to take effect. |
| `0x0084` CB_SET_LVL      | **Write:** 16-bit cell voltage threshold (mV). Device balances cells above this threshold. **Read:** returns the current threshold. |

## 3. Balancing Status Subcommands

| Subcommand            | Description                                                                               |
|-----------------------|-------------------------------------------------------------------------------------------|
| `0x0085` CBSTATUS1    | 16-bit time in seconds that balancing has been active                                     |
| `0x0086` CBSTATUS2    | 32-byte block: cumulative balance time per cell (cells 1-8), 32-bit unsigned seconds each. Resets on device reset or CONFIG_UPDATE entry. |
| `0x0087` CBSTATUS3    | 8-byte block: cumulative balance time (cells 9-10), 32-bit unsigned seconds each          |

## 4. Autonomous Balancing Configuration

Register: `Settings:Cell Balancing Config:Balancing Configuration`

| Bit          | Description                                      |
|--------------|--------------------------------------------------|
| `[CB_CHG]`   | Allow balancing during charge                    |
| `[CB_RLX]`   | Allow balancing during relax                     |
| `[CB_SLEEP]` | Allow balancing in SLEEP mode                    |
| `[CB_NOSLEEP]` | Prevent SLEEP during balancing (wake to balance) |
| `[CB_NO_CMD]` | Disable host-controlled balancing subcommands   |

### CB_SLEEP / CB_NOSLEEP Combinations

| CB_SLEEP | CB_NOSLEEP | Description                                                        |
|----------|------------|--------------------------------------------------------------------|
| 0        | 0          | Balancing stops at SLEEP, waits for NORMAL                         |
| 0        | 1          | Invalid (CB_NOSLEEP requires CB_SLEEP)                             |
| 1        | 0          | Balancing continues in SLEEP mode                                  |
| 1        | 1          | Device exits SLEEP to balance, blocks re-entry during balancing    |

## 5. Voltage Thresholds for Autonomous Balancing

### During Charge

| Setting                                                       | Description                                           |
|---------------------------------------------------------------|-------------------------------------------------------|
| `Cell Balancing Config:Cell Balance Min Cell V (Charge)`      | Minimum cell voltage to allow balancing during charge  |
| `Cell Balancing Config:Cell Balance Min Delta (Charge)`       | Minimum (max - min) cell voltage delta to trigger      |
| `Cell Balancing Config:Cell Balance Stop Delta (Charge)`      | Stop when all cells within this delta of minimum cell  |

### During Relax

| Setting                                                       | Description                                           |
|---------------------------------------------------------------|-------------------------------------------------------|
| `Cell Balancing Config:Cell Balance Min Cell V (Relax)`       | Minimum cell voltage to allow balancing during relax   |
| `Cell Balancing Config:Cell Balance Min Delta (Relax)`        | Minimum (max - min) cell voltage delta to trigger      |
| `Cell Balancing Config:Cell Balance Stop Delta (Relax)`       | Stop when all cells within this delta of minimum cell  |

> Stop Delta should be < Min Delta to create hysteresis.

## 6. Timing Configuration

| Setting                                                | Description                                                                    |
|--------------------------------------------------------|--------------------------------------------------------------------------------|
| `Cell Balancing Config:Cell Balance Interval`          | Interval for re-evaluating balancing conditions (seconds). Also safety timeout for host-controlled balancing. |
| `Cell Balancing Config:Cell Balance Max Cells`         | Maximum number of cells balanced simultaneously (limits power dissipation)     |

## 7. Temperature Limits

| Setting                                          | Description                                                    |
|--------------------------------------------------|----------------------------------------------------------------|
| `Cell Balancing Config:Min Cell Temp`            | Minimum cell temperature for balancing                         |
| `Cell Balancing Config:Max Cell Temp`            | Maximum cell temperature for balancing                         |
| `Cell Balancing Config:Max Internal Temp`        | Maximum internal die temperature for balancing                 |

Balancing disabled if temperature outside these limits.

## 8. Current Thresholds for Charge/Relax Detection

| Setting                                          | Description                                                    |
|--------------------------------------------------|----------------------------------------------------------------|
| `Current Thresholds:Chg Current Threshold`       | Current above this = charging (for CB_CHG mode)                |
| `Current Thresholds:Dsg Current Threshold`       | Current below negative of this = discharging. Between the two thresholds = relax (for CB_RLX mode). |

## 9. Balancing and Measurement Interaction

During the measurement loop:
- Balancing temporarily disabled on cell being measured
- Balancing disabled on cells adjacent to cell being measured
- Balancing disabled on top cell during stack voltage measurement
- This reduces average balancing current

### Cell Balancing Loop Slow-Down

Register: `Settings:Configuration:Power Config[CB_LOOP_SLOW_1:0]`

| CB_LOOP_SLOW_1 | CB_LOOP_SLOW_0 | Description                         |
|----------------|----------------|-------------------------------------|
| 0              | 0              | Full speed during balancing         |
| 0              | 1              | Half speed during balancing         |
| 1              | 0              | Quarter speed during balancing      |
| 1              | 1              | Eighth speed during balancing       |

> `CB_LOOP_SLOW` and regular `LOOP_SLOW` operate independently.

## 10. Balancing and Protection Interaction

- COV/CUV checks normally operate every 3.3 ms when not balancing
- During balancing: COV/CUV schedule disabled; device briefly stops balancing every 1 second to allow COV/CUV checks, then restarts
- If CUV or COV alert detected at 1-second check, balancing immediately disabled
- This means ~1 second additional delay for CUV/COV detection during balancing

## 11. Balancing Current

Each balancing switch draws ~35 uA through VC10 pin per cell being balanced. Use appropriate VC10 input resistor to minimize IR drop affecting Cell 10 measurement.

## 12. Balancing Disable Conditions

Balancing is immediately disabled if:
- Device enters CONFIG_UPDATE mode
- Enabled protection alert from Protections A fires
- Enabled protection fault from Protections A fires (except COV)
- Enabled Permanent Fail occurs
- Device enters DEEPSLEEP mode
- Device enters SHUTDOWN mode
