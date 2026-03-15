# Astrophage — 8S1P Battery Management System

## Purpose

Educational BMS for an 8S1P lithium-ion pack. Goal: deeply learn BMS architecture
(cell monitoring, protection, balancing, state estimation) in a way that mirrors
utility-scale BESS systems. Personal project, not a product.

I'm a Field Engineer on a Fluence Gridstack BESS project — relate design choices
to utility-scale equivalents when relevant.

## Hardware

- **Cells**: Samsung INR18650-30Q, NMC, 3.6V nom, 3000mAh, 15A cont, 8S1P config
- **AFE**: TI BQ76942 (I2C, 8S, 48-pin TQFP). Docs: SLUSC15, SLUUBY2
- **MCU**: STM32H743 (Cortex-M7, 480MHz, 1MB flash, 2MB RAM)
- **MCU ↔ AFE link**: I2C
- **Dev approach**: Nucleo-H743ZI2 for firmware bring-up, then custom PCB with
  BQ76942 + STM32H743 on one board
- **EDA**: KiCad

## Phase Roadmap

**Phase 1** — Classical BMS (current focus)
- BQ76942 I2C driver, protection config, cell balancing
- SOC estimation: coulomb counting → EKF
- BMS state machine, UART telemetry
- KiCad schematic + PCB for unified board

**Phase 2** — TinyML SOH Layer
- On-device SOH estimation using quantized LSTM or TCN
- Trained on real charge/discharge telemetry from Phase 1
- Deployed via STM32Cube.AI
- Classical SOC (EKF) stays; TinyDL is for SOH only

## Current Project State

Early stage. The repo currently contains only datasheets (PDF + extracted markdown),
this CLAUDE.md, a README, and a uv-managed Python environment. No firmware, no
schematic, no simulations yet. Everything needs to be built from scratch.

## Build & Flash (for when firmware exists)

```bash
# Firmware
cd firmware/build && cmake .. -DCMAKE_BUILD_TYPE=Debug && make -j$(nproc)

# Flash
openocd -f interface/stlink.cfg -f target/stm32h7x.cfg \
  -c "program build/astrophage.elf verify reset exit"

# Python simulations
uv run python simulations/<script>.py
```

## Code Conventions

- C11 firmware, Python 3.12 simulations (uv-managed, no pip install)
- snake_case functions/variables, UPPER_CASE constants
- Return status codes (BMS_OK, BMS_ERR_COMM, etc.), no dynamic allocation
- Each module: .c + .h pair. Comments explain *why*, not what.

## BQ76942 Gotchas

- I2C addr 0x08 (7-bit), 400kHz, uses clock stretching
- Subcommands use transfer buffer at 0x3E/0x40 with CRC-8 (poly 0x07)
- All multi-byte values are little-endian
- Config writes go to RAM registers, not direct command space

## Key Design Decisions

- STM32H743 chosen for Phase 2 TinyML headroom (2MB RAM)
- SOC uses classical EKF (interpretable, debuggable); SOH uses TinyDL (nonlinear degradation)