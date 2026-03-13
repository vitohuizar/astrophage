# Astrophage — 8S1P Battery Management System
 
## Project Overview
 
Astrophage is a bench-scale Battery Management System for an 8S1P lithium-ion pack.
The goal is educational: deeply learn BMS architecture — cell monitoring, protection,
balancing, state estimation, and firmware design — in a way that mirrors utility-scale
BESS systems (Fluence, Tesla Megapack). This is a personal project, not a product.
 
## Hardware
 
### Cells
- **Cell**: Samsung INR18650-30Q
- **Chemistry**: NMC (Li-ion)
- **Nominal voltage**: 3.6V
- **Capacity**: 3000mAh
- **Max continuous discharge**: 15A
- **Max charge voltage**: 4.20V
- **Cutoff voltage**: 2.50V
- **Configuration**: 8S1P
- **Pack nominal voltage**: 28.8V (8 × 3.6V)
- **Pack full voltage**: 33.6V (8 × 4.2V)
- **Pack empty voltage**: 20.0V (8 × 2.5V)
 
### Analog Front End
- **IC**: Texas Instruments BQ76942 (BQ769x2 family)
- **Cell count range**: 3S–10S (we use 8S)
- **Package**: 48-pin TQFP (hand-solderable)
- **Communication**: I2C (primary), SPI and HDQ also supported
- **Key features**:
  - High-accuracy cell voltage measurement
  - Configurable protection subsystem (OV, UV, OC, SC, OT, UT)
  - Autonomous or host-controlled passive cell balancing
  - Integrated high-side charge-pump NFET drivers
  - Dual programmable LDOs (1.8V/2.5V/3.0V/3.3V/5.0V, 45mA each)
  - Up to 9 thermistor inputs
  - OTP memory for production configuration
- **Key documents**:
  - Datasheet: SLUSC15
  - Technical Reference Manual: SLUUBY2
  - Software Development Guide (BQ769x2 family)
  - Calibration and OTP Programming Guide
 
### MCU
- **IC**: STM32F446RE (Nucleo-64 board for initial dev, custom board later)
- **Core**: ARM Cortex-M4, 180 MHz, FPU
- **Flash**: 512 KB
- **RAM**: 128 KB
- **Peripherals used**: I2C, UART, GPIO, ADC, timers
 
### Custom PCB
- **EDA**: KiCad
- **Design stage**: Not yet started — firmware development on Nucleo + EVM first
- **Plan**: Single board with BQ76942, connectors for 8S cell taps, thermistors,
  protection FETs, current sense shunt, STM32, UART/USB debug header
 
## Architecture
 
### Firmware Layers
```
┌─────────────────────────────┐
│     Application Layer       │  BMS state machine, telemetry, balancing logic
├─────────────────────────────┤
│     Driver Layer            │  bq76942 driver (registers, subcommands, CRC)
├─────────────────────────────┤
│     HAL Layer               │  I2C, UART, GPIO, Timer (STM32 HAL or bare register)
└─────────────────────────────┘
```
 
### BMS State Machine
```
INIT → IDLE → PRECHARGE → CHARGING → DISCHARGING → FAULT
                                                      │
                                          (clear faults + manual reset)
                                                      │
                                                    IDLE
```
 
### BQ76942 Communication Protocol
- I2C address: 0x08 (7-bit), supports 400 kHz, uses clock stretching
- Direct commands: single-byte address, 1–2 byte data (cell voltages, status, control)
- Subcommands: via transfer buffer at 0x3E (command) and 0x40 (data), with CRC-8
- CRC polynomial: 0x07 (x^8 + x^2 + x + 1)
- RAM register access: used for configuration (protection thresholds, balancing params)
- All multi-byte values are little-endian
 
## Code Conventions
 
- **Language**: C11 for firmware, Python 3.12 for simulations and tooling
- **Naming**: snake_case for functions/variables, UPPER_CASE for constants/macros
- **File structure**: each module gets a .c + .h pair in matching directories
- **Error handling**: return status codes (BMS_OK, BMS_ERR_COMM, BMS_ERR_OV, etc.)
- **No dynamic allocation** in firmware (no malloc)
- **Comments**: explain why, not what
- **Python env**: managed by uv (pyproject.toml), do not use pip install directly
 
## Build System
 
### Firmware
```bash
cd firmware/build
cmake .. -DCMAKE_BUILD_TYPE=Debug
make -j$(nproc)
```
 
### Flash
```bash
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg \
  -c "program build/astrophage.elf verify reset exit"
```
 
### Python simulations
```bash
uv run python simulations/<script>.py
```
 
## Project Structure
```
astrophage/
├── CLAUDE.md                  # This file
├── pyproject.toml             # Python dependencies (managed by uv)
├── uv.lock                    # Locked dependency versions
├── .gitignore
├── firmware/
│   ├── CMakeLists.txt
│   ├── src/                   # Application code
│   │   ├── main.c
│   │   ├── bms_fsm.c/.h      # State machine
│   │   ├── bms_config.h       # Protection thresholds, cell params
│   │   ├── bms_monitor.c/.h   # Measurement reading and processing
│   │   └── bms_balance.c/.h   # Cell balancing logic
│   ├── drivers/
│   │   ├── bq76942/
│   │   │   ├── bq76942.c/.h   # Register access, subcommands, CRC
│   │   │   └── bq76942_regs.h # Register address definitions
│   │   └── hal/
│   │       ├── i2c.c/.h
│   │       ├── uart.c/.h
│   │       └── gpio.c/.h
│   └── inc/                   # Shared headers, types, error codes
│       └── bms_types.h
├── simulations/
│   ├── balancing_sim.py       # Cell balancing convergence simulation
│   ├── soc_estimation.py      # SOC algorithms (coulomb counting, EKF)
│   ├── thermal_model.py       # Pack thermal behavior
│   └── plot_telemetry.py      # Live UART telemetry dashboard
├── hardware/
│   ├── kicad/                 # Schematic and PCB files
│   ├── bom/                   # Bill of materials
│   └── reference/             # TI EVM schematics, reference designs
├── datasheets/
│   ├── bq76942_datasheet.pdf
│   ├── bq76942_trm.pdf
│   ├── inr18650-30q.pdf
│   └── extracted/             # Markdown extracts of key datasheet sections
├── docs/
│   ├── session_log.md         # Running log of Claude Code session summaries
│   ├── design_decisions.md    # Rationale for key choices
│   └── state_machine.md       # FSM diagram and transition logic
└── tests/
    ├── test_crc.py            # Verify CRC-8 implementation
    └── test_register_config.py
```
 
## Protection Thresholds (Initial — Subject to Tuning)
 
Based on Samsung 30Q datasheet limits with safety margins:
 
| Protection             | Threshold  | Notes                              |
|------------------------|------------|------------------------------------|
| Cell overvoltage       | 4.25V      | 50mV above max charge voltage      |
| Cell undervoltage      | 2.50V      | Matches cell cutoff                |
| Overcurrent charge     | 4A         | 30Q rated for 4A charge max        |
| Overcurrent discharge  | 20A        | Short-duration trip, above 30Q's 15A continuous |
| Short circuit          | 40A        | Hardware protection, fast trip      |
| Overtemp charge        | 45°C       | 30Q max charge temp is 50°C        |
| Overtemp discharge     | 60°C       | 30Q max discharge temp is 75°C     |
| Undertemp charge       | 0°C        | Li-ion plating risk below 0°C      |
| Undertemp discharge    | -20°C      | 30Q rated to -20°C discharge       |
 
## Relationship to Professional Work
 
I'm a Field Engineer at CSI Electrical Contractors working on the Baldy Mesa
50MW/200MWh BESS project (Fluence systems, AES developer). When explaining
design choices or trade-offs, relate them to utility-scale BESS equivalents
where relevant — how thresholds scale, how protection layers differ, how
communication architecture maps from cell-level to rack-level to site-level.
 
## Completed Extractions
 
- [x] BQ76942 TRM → datasheets/extracted/ (markdown format with proper tables)
 
## Current Status
 
- [x] Project structure and uv environment initialized
- [x] Download and extract BQ76942 TRM
- [ ] Download and extract BQ76942 datasheet and 30Q cell datasheet
- [ ] BQ76942 I2C driver (direct commands + subcommands + CRC)
- [ ] Register configuration / initialization
- [ ] Cell voltage and temperature reading
- [ ] Protection threshold configuration
- [ ] BMS state machine
- [ ] Passive cell balancing
- [ ] UART telemetry output (CSV format)
- [ ] Python live telemetry dashboard
- [ ] Balancing simulation
- [ ] SOC estimation (coulomb counting → EKF)
- [ ] KiCad schematic
- [ ] KiCad PCB layout
- [ ] Fabrication and assembly