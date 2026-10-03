# 2D FIR Filter ASIC Tapeout Database (SCL 1.2 µm CMOS)

## 1. Chip Overview & Tapeout Information

| Parameter | Value | Remarks |
|:---|:---|:---|
| **Design Name** | 2D FIR Image Filter ASIC | Real-time multi-mode spatial filtering |
| **Top Cell Name** | `fir2d_chip_4mmx4mm` | Top-level full chip hierarchy |
| **Core Cell Name** | `fir2d_top` | Standard cell core macro |
| **Technology Node** | SCL 1.2 µm C1D CMOS | Single poly, double metal (M1, M2) |
| **Operating Voltage** | 5.0 V nominal (4.5 V – 5.5 V) | Native 5V CMOS standard cell library |
| **Die Dimensions** | 4000.0 µm × 4000.0 µm (4.0 mm × 4.0 mm) | SCL standard pad frame `frame4mmx4mm` |
| **Core Cavity Area** | 3390.0 µm × 3390.0 µm (11.49 mm²) | Active standard cell core cavity |
| **Core Cell Count** | 1,350 standard cells + 65,876 filler cells | Fully legalized with alternating row gaps |
| **Detailed Route DRC** | **0 Violations** (TritonRoute clean) | Verified through 56 optimization iterations |
| **Total Pad Count** | 40 Pads (32 Signal I/O + 8 Power/Ground) | Minimum pad pitch = 350 µm |
| **Operating Clock** | 50 MHz (20 ns cycle period) | Pipelined 2D convolution datapath |

---

## 2. Chip Pinout & Pad Assignment

| Pad # | Pad Name | Cell Type | Signal Name | Direction | Function / Description |
|:---|:---|:---|:---|:---|:---|
| **1** | PAD1 | IPAD20 | `CLK` | Input | Master system clock (50 MHz) |
| **2** | PAD2 | IPAD20 | `RST_N` | Input | Asynchronous active-low reset |
| **3** | PAD3 | IPAD20 | `VALID_IN` | Input | Input pixel valid strobe |
| **4** | PAD4 | IPAD20 | `MODE[0]` | Input | Filter mode select bit 0 |
| **5** | PAD5 | IPAD20 | `MODE[1]` | Input | Filter mode select bit 1 |
| **6** | PAD6 | IPAD20 | `DIN[0]` | Input | Pixel data input bit 0 (LSB) |
| **7** | PAD7 | IPAD20 | `DIN[1]` | Input | Pixel data input bit 1 |
| **8** | PAD8 | IPAD20 | `DIN[2]` | Input | Pixel data input bit 2 |
| **33** | PVDD_B | PVDD01 | `VDD` | Power | Core & I/O 5.0V Power Supply (Bottom) |
| **34** | PVSS_B | PVSS01 | `VSS` | Ground | Core & I/O 0.0V Ground (Bottom) |
| **9** | PAD9 | IPAD20 | `DIN[3]` | Input | Pixel data input bit 3 |
| **10** | PAD10 | IPAD20 | `DIN[4]` | Input | Pixel data input bit 4 |
| **11** | PAD11 | IPAD20 | `DIN[5]` | Input | Pixel data input bit 5 |
| **12** | PAD12 | IPAD20 | `DIN[6]` | Input | Pixel data input bit 6 |
| **13** | PAD13 | IPAD20 | `DIN[7]` | Input | Pixel data input bit 7 (MSB) |
| **14** | PAD14 | OPAD02 | `DOUT[0]` | Output | Filtered pixel output bit 0 (LSB) |
| **15** | PAD15 | OPAD02 | `DOUT[1]` | Output | Filtered pixel output bit 1 |
| **16** | PAD16 | OPAD02 | `DOUT[2]` | Output | Filtered pixel output bit 2 |
| **35** | PVDD_R | PVDD01 | `VDD` | Power | Core & I/O 5.0V Power Supply (Right) |
| **36** | PVSS_R | PVSS01 | `VSS` | Ground | Core & I/O 0.0V Ground (Right) |
| **17** | PAD17 | OPAD02 | `DOUT[3]` | Output | Filtered pixel output bit 3 |
| **18** | PAD18 | OPAD02 | `DOUT[4]` | Output | Filtered pixel output bit 4 |
| **19** | PAD19 | OPAD02 | `DOUT[5]` | Output | Filtered pixel output bit 5 |
| **20** | PAD20 | OPAD02 | `DOUT[6]` | Output | Filtered pixel output bit 6 |
| **21** | PAD21 | OPAD02 | `DOUT[7]` | Output | Filtered pixel output bit 7 (MSB) |
| **22** | PAD22 | OPAD02 | `VALID_OUT` | Output | Output pixel valid strobe |
| **23** | PAD23 | OPAD02 | `LINE_DONE` | Output | Horizontal line sync indicator |
| **24** | PAD24 | OPAD02 | `FRAME_DONE` | Output | Complete image frame sync indicator |
| **37** | PVDD_T | PVDD01 | `VDD` | Power | Core & I/O 5.0V Power Supply (Top) |
| **38** | PVSS_T | PVSS01 | `VSS` | Ground | Core & I/O 0.0V Ground (Top) |
| **25**–**32**| PAD25-32 | IPAD00 | `SPARE1..8` | Spare | Spare test pads with ESD protection |
| **39** | PVDD_L | PVDD01 | `VDD` | Power | Core & I/O 5.0V Power Supply (Left) |
| **40** | PVSS_L | PVSS01 | `VSS` | Ground | Core & I/O 0.0V Ground (Left) |

---

## 3. Filter Operating Modes

| Mode [1:0] | Filter Type | 3x3 Convolution Kernel | Normalization / Transfer Function |
|:---|:---|:---|:---|
| `2'b00` | **Gaussian Smoothing** | $\begin{bmatrix} 1 & 2 & 1 \\ 2 & 4 & 2 \\ 1 & 2 & 1 \end{bmatrix}$ | $Y = \left(\sum K \cdot P\right) \gg 4$ (Divide by 16) |
| `2'b01` | **Sharpening (High-Boost)** | $\begin{bmatrix} 0 & -1 & 0 \\ -1 & 5 & -1 \\ 0 & -1 & 0 \end{bmatrix}$ | $Y = \text{clamp}_{[0, 255]}\left(\sum K \cdot P\right)$ |
| `2'b10` | **Sobel X Gradient** | $\begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$ | $Y = \text{clamp}_{[0, 255]}\left(\lvert \sum K \cdot P \rvert\right)$ |
| `2'b11` | **Laplacian Edge Detector** | $\begin{bmatrix} -1 & -1 & -1 \\ -1 & 8 & -1 \\ -1 & -1 & -1 \end{bmatrix}$ | $Y = \text{clamp}_{[0, 255]}\left(\lvert \sum K \cdot P \rvert\right)$ |

---

## 4. Database Files Description

* `final.gds`: Tapeout stream GDSII containing the entire physical mask data for fabrication.
* `fir2d_chip_4mmx4mm.gds`: Top-level chip GDS file.
* `fir2d_core.gds`: Standalone routed core block GDS file.
* `fir2d_chip_4mmx4mm.cdl`: Transistor-level schematic netlist for full-chip LVS sign-off.
* `fir2d_routed.def`: Routed Design Exchange Format (DEF) file with all wire tracks and vias.
* `fir2d.spef`: Extracted Standard Parasitic Exchange Format file.
* `fir2d.sdf`: Standard Delay Format back-annotation file.
* `fir2d.sdc`: Synopsys timing constraints file.
* `fir2d_gate.v`: Synthesized flat gate-level netlist.
* `fir2d_routed_pwr.v`: Post-PnR netlist including power and ground pins.
* `chip_drc.txt`: Physical DRC runset verification report.
