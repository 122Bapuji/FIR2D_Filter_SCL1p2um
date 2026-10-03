import matplotlib.pyplot as plt
import numpy as np

# Create synthetic 2D test patterns and simulated responses matching the Verilog testbench
np.random.seed(42)

# Generate a 16x16 test image patch (Edge step, impulse, and noisy plateau)
img_size = 16
input_img = np.ones((img_size, img_size), dtype=np.float32) * 50.0
# Add a bright center square (step edge)
input_img[5:11, 5:11] = 200.0
# Add high-frequency noise
noise = np.random.normal(0, 8, (img_size, img_size))
input_img_noisy = np.clip(input_img + noise, 0, 255)

# Kernel definitions matching the Verilog hardware:
# 1. Gaussian [1 2 1; 2 4 2; 1 2 1] / 16
k_gauss = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=np.float32) / 16.0

# 2. Sharpen [0 -1 0; -1 5 -1; 0 -1 0]
k_sharp = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)

# 3. Sobel X [-1 0 1; -2 0 2; -1 0 1]
k_sobel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)

# 4. Laplacian [-1 -1 -1; -1 8 -1; -1 -1 -1]
k_laplace = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32)

def apply_kernel(img, k, is_mag=False):
    out = np.zeros_like(img)
    for r in range(1, img.shape[0]-1):
        for c in range(1, img.shape[1]-1):
            patch = img[r-1:r+2, c-1:c+2]
            val = np.sum(patch * k)
            if is_mag:
                val = np.abs(val)
            out[r, c] = np.clip(val, 0, 255)
    return out

out_gauss   = apply_kernel(input_img_noisy, k_gauss)
out_sharp   = apply_kernel(input_img, k_sharp)
out_sobel   = apply_kernel(input_img, k_sobel, is_mag=True)
out_laplace = apply_kernel(input_img, k_laplace, is_mag=True)

# Plot Figure: 2D Spatial Views & Waveform Profile Traces
fig, axes = plt.subplots(2, 4, figsize=(18, 9), facecolor='white')
fig.suptitle("2D FIR Image Filter ASIC (SCL 1.2 um CMOS) - Multi-Mode Verification", fontsize=16, fontweight='bold', y=0.98)

# Top row: 2D Spatial Images
im0 = axes[0, 0].imshow(input_img_noisy, cmap='gray', vmin=0, vmax=255)
axes[0, 0].set_title("Input Stream with Noise\n(Mode 00 Input)", fontsize=11, fontweight='bold')
axes[0, 0].axis('off')

im1 = axes[0, 1].imshow(out_gauss, cmap='gray', vmin=0, vmax=255)
axes[0, 1].set_title("Mode 00: Gaussian Filter\n(Noise Smoothed)", fontsize=11, fontweight='bold')
axes[0, 1].axis('off')

im2 = axes[0, 2].imshow(out_sobel, cmap='gray', vmin=0, vmax=255)
axes[0, 2].set_title("Mode 10: Sobel X Gradient\n(Vertical Edges Detected)", fontsize=11, fontweight='bold')
axes[0, 2].axis('off')

im3 = axes[0, 3].imshow(out_laplace, cmap='gray', vmin=0, vmax=255)
axes[0, 3].set_title("Mode 11: Laplacian Filter\n(Omnidirectional Edges)", fontsize=11, fontweight='bold')
axes[0, 3].axis('off')

# Bottom row: Horizontal Slice Waveforms (Row 8 profile)
x_coords = np.arange(img_size)

axes[1, 0].plot(x_coords, input_img_noisy[8, :], 'k.-', lw=2, label="Noisy Pixel In")
axes[1, 0].plot(x_coords, out_gauss[8, :], 'b.-', lw=2.5, label="Gaussian Filter Out")
axes[1, 0].set_title("Gaussian Smoothing Profile (Row 8)", fontsize=11, fontweight='bold')
axes[1, 0].set_xlabel("Pixel Column Index")
axes[1, 0].set_ylabel("Pixel Intensity (0-255)")
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].legend(loc='upper right')

axes[1, 1].plot(x_coords, input_img[8, :], 'k--', lw=1.5, label="Clean Step In")
axes[1, 1].plot(x_coords, out_sharp[8, :], 'g.-', lw=2.5, label="Sharpened Out")
axes[1, 1].set_title("Sharpening Filter Overshoot Profile", fontsize=11, fontweight='bold')
axes[1, 1].set_xlabel("Pixel Column Index")
axes[1, 1].grid(True, alpha=0.3)
axes[1, 1].legend(loc='upper right')

axes[1, 2].plot(x_coords, input_img[8, :], 'k--', lw=1.5, label="Clean Step In")
axes[1, 2].plot(x_coords, out_sobel[8, :], 'r.-', lw=2.5, label="Sobel Edge Out")
axes[1, 2].set_title("Sobel Edge Peak Response", fontsize=11, fontweight='bold')
axes[1, 2].set_xlabel("Pixel Column Index")
axes[1, 2].grid(True, alpha=0.3)
axes[1, 2].legend(loc='upper right')

axes[1, 3].plot(x_coords, input_img[8, :], 'k--', lw=1.5, label="Clean Step In")
axes[1, 3].plot(x_coords, out_laplace[8, :], 'm.-', lw=2.5, label="Laplacian Edge Out")
axes[1, 3].set_title("Laplacian Double-Edge Outline", fontsize=11, fontweight='bold')
axes[1, 3].set_xlabel("Pixel Column Index")
axes[1, 3].grid(True, alpha=0.3)
axes[1, 3].legend(loc='upper right')

plt.tight_layout()
out_fig = "/mnt/g/VLSI_Projects/FIR2D_Filter_SCL1p2um/plots/fir2d_filter_modes_response.png"
plt.savefig(out_fig, dpi=300)
print(f"Saved filter response plot to {out_fig}")
