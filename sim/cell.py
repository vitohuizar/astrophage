"""Virtual Samsung INR18650-30Q cell.

A 1st-order Thevenin equivalent-circuit model (ECM): an ideal OCV source in
series with an ohmic resistance R0 and one parallel RC branch. This is the
workhorse model in real BMS work -- it captures the instantaneous IR step and
the slower polarization tail without needing electrochemistry, and it is the
exact plant the Phase-1 coulomb-counter / EKF will estimate against.

    I --->[ R0 ]---+--[ R1 ]--+---  +
                   |          |
                  (V_rc)    [ C1 ]   V_terminal
                   |          |
            ( OCV(SOC) )------+---  -

Sign convention: current is current INTO the cell.
    I > 0  -> charging    (terminal voltage rises above OCV)
    I < 0  -> discharging  (terminal voltage sags below OCV)
Drive it with any current profile via step() and read .voltage / .soc.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# Open-circuit voltage vs SOC for an NMC 18650, measured at rest (no load).
# Coarse but monotonic table; np.interp fills in between. The flat 40-80%
# region is the classic NMC plateau that makes voltage-only SOC unreliable
# and is the whole reason coulomb counting (and later an EKF) is needed.
_SOC_BREAKPOINTS = np.array(
    [0.00, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
)
_OCV_BREAKPOINTS = np.array(
    [3.00, 3.30, 3.42, 3.53, 3.60, 3.65, 3.72, 3.80, 3.89, 3.98, 4.08, 4.20]
)


@dataclass
class Cell:
    """A single INR18650-30Q modeled as a 1st-order Thevenin ECM.

    Parameter values are representative room-temperature numbers for a 30Q;
    they are constant here (no temperature or SOC dependence yet) so the model
    stays simple and debuggable. Tune them later against real telemetry.
    """

    capacity_ah: float = 3.0      # rated 3000 mAh
    r0_ohm: float = 0.025         # ohmic resistance -> instantaneous IR step
    r1_ohm: float = 0.012         # polarization resistance (RC branch)
    c1_farad: float = 2500.0      # polarization capacitance; tau = R1*C1 ~ 30 s
    v_max: float = 4.20           # full-charge cutoff
    v_min: float = 2.50           # discharge cutoff

    soc: float = 1.0              # state of charge, 0..1
    v_rc: float = 0.0             # voltage across the RC branch (state)

    # Cached terminal voltage so .voltage reflects the last step's current.
    _v_terminal: float = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self.soc = float(np.clip(self.soc, 0.0, 1.0))
        if self._v_terminal is None:
            # At t=0 with no current applied, terminal voltage == OCV.
            self._v_terminal = self.ocv

    @property
    def ocv(self) -> float:
        """Rested open-circuit voltage for the current SOC (V)."""
        return float(np.interp(self.soc, _SOC_BREAKPOINTS, _OCV_BREAKPOINTS))

    @property
    def voltage(self) -> float:
        """Terminal voltage as of the last step() (V)."""
        return self._v_terminal

    def terminal_voltage(self, current: float) -> float:
        """Terminal voltage for an applied current without advancing state."""
        return self.ocv + current * self.r0_ohm + self.v_rc

    def step(self, current: float, dt: float) -> float:
        """Advance the model by dt seconds at constant current; return voltage.

        current : amps into the cell (+ charge, - discharge)
        dt      : timestep in seconds
        """
        # Coulomb counting: charge moved = I * dt, normalized by capacity.
        # capacity_ah * 3600 converts Ah -> As (coulombs).
        self.soc = float(
            np.clip(self.soc + current * dt / (self.capacity_ah * 3600.0), 0.0, 1.0)
        )

        # Exact discretization of the RC branch over the step (zero-order hold
        # on current). At steady state v_rc -> I*R1; the exp() is the tail.
        tau = self.r1_ohm * self.c1_farad
        alpha = np.exp(-dt / tau)
        self.v_rc = self.v_rc * alpha + current * self.r1_ohm * (1.0 - alpha)

        self._v_terminal = self.ocv + current * self.r0_ohm + self.v_rc
        return self._v_terminal

    def run(self, current: np.ndarray, dt: float) -> dict[str, np.ndarray]:
        """Drive the cell with a current profile; return time/voltage/soc arrays.

        current : 1-D array of amps into the cell, one entry per timestep
        dt      : seconds per sample
        """
        current = np.asarray(current, dtype=float)
        n = current.size
        t = np.arange(n) * dt
        v = np.empty(n)
        soc = np.empty(n)
        for k in range(n):
            v[k] = self.step(current[k], dt)
            soc[k] = self.soc
        return {"t": t, "current": current, "voltage": v, "soc": soc}


def _demo() -> None:
    """Drive a full 30Q through 1C discharge -> rest -> 0.5C charge -> rest."""
    dt = 1.0  # 1 s timestep
    profile = np.concatenate(
        [
            np.full(2700, -3.0),  # 45 min @ -3 A   (1C discharge)
            np.zeros(900),        # 15 min rest     (watch voltage relax up)
            np.full(3600, +1.5),  # 60 min @ +1.5 A (0.5C charge)
            np.zeros(900),        # 15 min rest     (watch voltage relax down)
        ]
    )

    cell = Cell(soc=1.0)
    out = cell.run(profile, dt)
    t_min = out["t"] / 60.0

    print(f"start: SOC={out['soc'][0]*100:5.1f}%  V={out['voltage'][0]:.3f} V")
    print(f"end:   SOC={out['soc'][-1]*100:5.1f}%  V={out['voltage'][-1]:.3f} V")
    print(f"min V={out['voltage'].min():.3f} V   max V={out['voltage'].max():.3f} V")

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    fig, (ax_v, ax_i, ax_s) = plt.subplots(3, 1, sharex=True, figsize=(9, 7))
    ax_v.plot(t_min, out["voltage"], color="tab:blue")
    ax_v.axhline(cell.v_max, ls="--", lw=0.8, color="grey")
    ax_v.axhline(cell.v_min, ls="--", lw=0.8, color="grey")
    ax_v.set_ylabel("V_terminal [V]")
    ax_i.plot(t_min, out["current"], color="tab:red")
    ax_i.set_ylabel("I in [A]")
    ax_s.plot(t_min, out["soc"] * 100.0, color="tab:green")
    ax_s.set_ylabel("SOC [%]")
    ax_s.set_xlabel("time [min]")
    fig.suptitle("Virtual INR18650-30Q — 1C discharge / rest / 0.5C charge / rest")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    _demo()
