# 📡 Analog OOK Demodulator

## 📖 Project Description

This project presents an analog signal processing chain consisting of several functional blocks:

1. Photodiode
2. Transimpedance Amplifier (TIA)
3. Active bandpass filter (~40 kHz) with small gain
4. Buffer (voltage follower)
5. Main signal gain stage
6. Envelope detector + comparator

---

## 🧩 Block Diagram

```
[ Photodiode / current source ]
              ↓
    Transimpedance Amplifier
              ↓
   Active Bandpass Filter (~40 kHz)
              ↓
        Buffer (Voltage Follower)
              ↓
         Main Signal Gain
              ↓
   Envelope Detector + Comparator
```

---

## 🔧 Block Description

### 1. Transimpedance Amplifier (TIA)

* Converts input current from a photodiode into voltage
* Key parameters:

  * feedback resistor (Rf)
  * compensation capacitor (Cf)

---

### 2. Active Bandpass Filter (~40 kHz)

* Filters the signal around the center frequency (~40 kHz)
* Reduces out-of-band noise
* Provides small gain

---

### 3. Buffer (Voltage Follower) 

* Unity-gain buffer (op-amp voltage follower)

**Why it is needed:**

* The gain stage loads the filter
* This changes the effective impedance seen by the filter
* Effects:

  * shift in center frequency
  * change in Q factor
  * degraded filter response

**Buffer function:**

* stage isolation
* stabilization of filter characteristics
* improved repeatability

---

### 4. Main Signal Gain

* Provides the required signal amplification
* TODO

---

### 5. Envelope Detector + Comparator

* Envelope detection (diode + RC)
* Comparator converts analog signal to digital output

---
