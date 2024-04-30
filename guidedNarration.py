import numpy as np
import soundfile as sf
import sounddevice as sd
import pygame
import threading
import math
import time
from scipy.signal import fftconvolve
from scipy.io import loadmat

# Initialize pygame and create a small window
pygame.init()
screen = pygame.display.set_mode((400, 400))

def load_hrtf(filename):
    data = loadmat(filename)
    hrir_left = data['hrir_l']
    hrir_right = data['hrir_r']
    itd = data['ITD']
    return hrir_left, hrir_right, itd

hrir_left, hrir_right, itd = load_hrtf('CIPIC_58_HRTF.mat')

# User position and direction
user_pos = np.array([0, 0], dtype='float32')  # Initial position
direction = 0  # Initial orientation in degrees
position_lock = threading.Lock()
    
def direction_to_angle(direction):
    angles = {
        'north': 0,
        'east': 90,
        'south': 180,
        'west': 270
    }
    return angles.get(direction, 0)

def process_frame(data):
    if data.shape[0] > 1024:
        return data[:1024]  # Truncate if longer
    elif data.shape[0] < 1024:
        return np.pad(data, ((0, 1024 - data.shape[0]), (0, 0)), mode='constant')  # Pad if shorter
    return data

def azimuth_to_index(azimuth):
    azimuths = [-80, -65, -55, -45] + list(range(-40, 45, 5)) + [55, 65, 80]
    return min(range(len(azimuths)), key=lambda i: abs(azimuths[i] - azimuth)) + 1

def elevation_to_index(elevation):
    if elevation < -45 or elevation > 230.625:
        raise ValueError("Elevation out of range")
    return int((elevation + 45) / 5.625)

def calculate_azimuth(user_pos, user_heading, src_pos):
    user_angle = direction_to_angle(user_heading)
    x_u, y_u = user_pos
    x_s, y_s = src_pos
    dx = x_s - x_u
    dy = y_s - y_u
    if user_heading == "north":
        x_prime, y_prime = dx, dy  # Reversing dy to adjust for typical screen coordinate systems
    elif user_heading == "south":
        x_prime, y_prime = dx, -dy
    elif user_heading == "east":
        x_prime, y_prime = dy, dx
    elif user_heading == "west":
        x_prime, y_prime = -dy, -dx
    azimuth = math.degrees(math.atan2(x_prime, y_prime))  # Adjusted to get correct forward angle
    if azimuth >= -90 and azimuth < 0:
        azimuth = azimuth - 90
    return azimuth
    # theta = math.radians(user_angle)
    # user_vector = [math.cos(theta), math.sin(theta)]
    # source_vector = [x_prime, y_prime]
    # dot_product = user_vector[0] * source_vector[0] + user_vector[1] * source_vector[1]
    # determinant = user_vector[0] * source_vector[1] - user_vector[1] * source_vector[0]
    # azimuth = math.degrees(math.atan2(determinant, dot_product))
    # return azimuth if -90 <= azimuth <= 90 else (azimuth + 360) % 360 - 360

def user_in_proximity(source_position, user_position, threshold):
    return np.linalg.norm(source_position - user_position) <= threshold


def adjust_spatial_audio(data, narrator_position, user_position):
    # Simple panning based on the narrator's position relative to the user
    delta_x = narrator_position[0] - user_position[0]
    delta_y = narrator_position[1] - user_position[1]

    distance = np.sqrt(delta_x**2 + delta_y**2)
    
    pan = delta_x / (abs(delta_x) + abs(delta_y)) if delta_x or delta_y else 0
    left_volume = 0.5 - pan * 0.5
    right_volume = 0.5 + pan * 0.5

    # max_distance = 20.0  # Example max distance for full attenuation
    # volume_adjustment = max(0, 1 - distance / max_distance)
    # left_volume *= volume_adjustment
    # right_volume *= volume_adjustment

    
    # Apply volume adjustment for simple left/right panning
    adjusted_data = np.zeros_like(data)
    adjusted_data[:, 0] = data[:, 0] * left_volume
    adjusted_data[:, 1] = data[:, 1] * right_volume
    
    return adjusted_data

# Load the audio file
audio_data, fs = sf.read('sounds/narrator.wav', always_2d=True)
if audio_data.ndim == 1:
    audio_data = np.stack((audio_data, audio_data), axis=-1)
left_volume = 1.0
right_volume = 1.0
current_index = 0

def audio_callback(outdata, frames, time, status):
    global current_index, audio_data, left_volume, right_volume, adjusted_data
    if current_index + frames > len(audio_data):
        outdata[:] = np.zeros((frames, 2))  # Fill with zeros if we run out of data
        return
    data_slice = audio_data[current_index:current_index+frames]
    adjusted_data = adjust_spatial_audio(data_slice, narrator_position, user_position)
    outdata[:] = adjusted_data
    current_index += frames

# Start audio stream
stream = sd.OutputStream(samplerate=fs, channels=2, callback=audio_callback)
stream.start()

narrator_position = [200, 150]  # Initial narrator position
user_position = [200, 200]  # User position 
pygame.draw.circle(screen, (255, 255, 255), [200, 200], 5)
pygame.draw.circle(screen, (255, 0, 0), [200, 250], 5)

# Function to play adjusted audio
def play_adjusted_audio():
    # adjusted_data = adjust_spatial_audio(audio_data, narrator_position, user_position)
    sd.play(adjusted_data, fs)

# Play audio at the start
# play_adjusted_audio()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                narrator_position[1] = max(0, narrator_position[1] - 50)
            elif event.key == pygame.K_DOWN:
                narrator_position[1] = min(400, narrator_position[1] + 50)
            elif event.key == pygame.K_LEFT:
                narrator_position[0] = max(0, narrator_position[0] - 50)
            elif event.key == pygame.K_RIGHT:
                narrator_position[0] = min(400, narrator_position[0] + 50)
            
            # Adjust and play the audio based on the new narrator position
            play_adjusted_audio()
            
        elif event.type == pygame.QUIT:
            running = False
            sd.stop()  # Stop any ongoing audio playback
    
    screen.fill((0, 0, 0))
    # Draw user as white dot
    pygame.draw.circle(screen, (255, 255, 255), user_position, 5)
    
    # Draw narrator as red dot
    pygame.draw.circle(screen, (255, 0, 0), narrator_position, 5)
    
    pygame.display.flip()  # Update the display

pygame.quit()


pygame.quit()
