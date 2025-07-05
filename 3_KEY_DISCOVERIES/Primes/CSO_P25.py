# --- CSO_P25.py ---
# Caterpillar's Command: [Code-FFT] (from prompt 25)
# Timestamp: 2024-05-21 17:05:00 UTC
# Applicable Rules: 2, 4, 5, 6, 11, 12
# Rule 11: Uses a global statistical method (FFT) ideal for heuristic analysis.
# Rule 12: Standardized program name.

import matplotlib.pyplot as plt
import numpy as np

def generate_primes(n):
    """Generates primes up to n using a Sieve."""
    primes = []
    sieve = [True] * (n + 1)
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for multiple in range(i*i, n + 1, i):
                sieve[multiple] = False
    for i in range(n + 1):
        if sieve[i]:
            primes.append(i)
    return primes

def analyze_spiral_with_fft(num_primes, image_size):
    """
    Generates the PSM spiral, rasterizes it to an image, and performs
    a 2D Fast Fourier Transform to find its frequency fingerprint.
    """
    print("Initializing 2D-FFT Frequency Analysis...")

    # 1. Generate prime coordinates
    n_limit = int(num_primes * (np.log(num_primes) + np.log(np.log(num_primes))))
    primes = generate_primes(n_limit)[:num_primes]
    print(f"Generated {len(primes)} primes.")

    k = np.e - 1
    radii = np.array(primes)
    thetas = (radii / k) * 2 * np.pi
    x_coords = radii * np.cos(thetas)
    y_coords = radii * np.sin(thetas)

    # 2. Rasterize the spiral onto an image plane
    print(f"Rasterizing spiral onto a {image_size}x{image_size} image plane...")
    image_plane = np.zeros((image_size, image_size))
    
    # Find scale to fit all points within the image bounds
    max_coord = np.max(np.abs(np.concatenate([x_coords, y_coords])))
    scale_factor = (image_size / 2 - 1) / max_coord
    
    # Map coordinates to integer pixel indices
    ix = (x_coords * scale_factor + image_size / 2).astype(int)
    iy = (y_coords * scale_factor + image_size / 2).astype(int)
    
    # Place points on the image plane
    image_plane[iy, ix] = 1

    # 3. Perform the 2D-FFT
    print("Performing 2D Fast Fourier Transform...")
    # Perform FFT and shift the zero-frequency component to the center
    fft_result = np.fft.fftshift(np.fft.fft2(image_plane))
    
    # Calculate magnitude and use a log scale to see details
    fft_magnitude = np.log1p(np.abs(fft_result))

    # 4. Plot the results
    print("Displaying results...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    plt.style.use('dark_background')

    # Plot original spiral
    ax1.imshow(image_plane, cmap='gray', origin='lower')
    ax1.set_title(f'PSM Spiral ({num_primes} Primes)', color='white')
    
    # Plot the FFT Frequency Fingerprint
    ax2.imshow(fft_magnitude, cmap='hot', origin='lower')
    ax2.set_title('Frequency Fingerprint (2D-FFT)', color='white')
    
    plt.show()

# --- Execution ---
number_of_primes_to_plot = 50000  # More primes create a clearer signal
image_resolution = 1024          # Standard FFT size (power of 2)
analyze_spiral_with_fft(number_of_primes_to_plot, image_resolution)