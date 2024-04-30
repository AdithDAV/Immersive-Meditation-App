import numpy as np
import soundfile as sf
import pyaudio
import socket
from scipy.signal import fftconvolve
from scipy.io import loadmat
import threading
import queue
import math
import time

# Load HRTF data from a .mat file
def load_hrtf(filename):
    data = loadmat(filename)
    hrir_left = data['hrir_l']
    hrir_right = data['hrir_r']
    itd = data['ITD']
    return hrir_left, hrir_right, itd

hrir_left, hrir_right, itd = load_hrtf('CIPIC_58_HRTF.mat')

# Define sound sources
sound_sources = {
    'pond1': {'position': np.array([450, 450]), 'file': 'sounds/pond.wav', 'azimuth': 0, 'elevation': 0, 'threshhold': 100},
    'pond2': {'position': np.array([150, 150]), 'file': 'sounds/pond.wav', 'azimuth': 0, 'elevation': 0, 'threshhold': 100},
    'ducks': {'position': np.array([100, 450]), 'file': 'sounds/duck.wav', 'azimuth': 0, 'elevation': 0, 'threshhold': 100},
    'tree1': {'position': np.array([50, 50]), 'file': 'sounds/tree.wav', 'azimuth': 0, 'elevation': 90, 'threshhold': 50},
    'tree2': {'position': np.array([250, 250]), 'file': 'sounds/tree.wav', 'azimuth': 0, 'elevation': 90, 'threshhold': 50},
    'tree3': {'position': np.array([300, 400]), 'file': 'sounds/tree.wav', 'azimuth': 0, 'elevation': 90, 'threshhold': 50},
    'tree4': {'position': np.array([550, 550]), 'file': 'sounds/tree.wav', 'azimuth': 0, 'elevation': 90, 'threshhold': 50},
    'tree5': {'position': np.array([400, 100]), 'file': 'sounds/tree.wav', 'azimuth': 0, 'elevation': 90, 'threshhold': 50},
    'birds': {'position': np.array([500, 200]), 'file': 'sounds/birds.wav', 'azimuth': 0, 'elevation': 90, 'threshhold': 100}
}

# Audio player setup
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=2, rate=44100, output=True, frames_per_buffer=1024)

# User position and direction
user_pos = np.array([0, 0], dtype='float32')  # Initial position
direction = 0  # Initial orientation in degrees
position_lock = threading.Lock()
    


# def update_position(new_position, new_direction):
#     with user_pos_lock:
#         global user_pos
#         user_pos[:] = new_position
#     with direction_lock:
#         global direction
#         direction = new_direction

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
    # Normalize azimuth to -90 to +90 range
    # if azimuth > 90:
    #     azimuth -= 180
    # elif azimuth < -90:
    #     azimuth += 180
    if azimuth >= -90 and azimuth < 0:
        azimuth = azimuth - 90
    # return azimuth if -90 < azimuth < 90 else (azimuth + 360) % 360 - 360
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


# Processing thread for each source
def source_processing(source, audio_queue, frame_size):
    global user_pos, direction
    data, sample_rate = sf.read(source['file'])
    num_samples = len(data)
    cursor = 0
    silent_frame = np.zeros((frame_size, 2), dtype='float32') 
    while True:
        with position_lock:
            current_position = user_pos
            current_orientation = direction
        # print(current_position, current_orientation)
        start = cursor
        end = start + frame_size
        if end >= num_samples:
            frame_data = np.concatenate((data[start:], data[:end % num_samples]))
        else:
            frame_data = data[start:end]
        cursor = end % num_samples
        
        if user_in_proximity(source['position'], current_position, source['threshhold']):
            # print("In proximity")
            azimuth = calculate_azimuth(current_position, current_orientation, source['position'])
            elevation = source['elevation']
            distance = np.linalg.norm(source['position'] - current_position)
            processed_frame = process_audio(frame_data, azimuth, elevation, distance, source['threshhold'])
        else:
            processed_frame = silent_frame

        audio_queue.put(processed_frame)
        time.sleep(frame_size / sample_rate)

# Processing audio data with HRTF
def process_audio(data, azimuth, elevation, distance, max_distance):
    print(azimuth)
    azimuth_idx = azimuth_to_index(azimuth)
    elevation_idx = elevation_to_index(elevation)
    attenuation = 1 - (distance / max_distance)
    pan_left, pan_right = 1.0, 1.0

    if direction == 'north':
        relative_azimuth = azimuth
    elif direction == 'east':
        relative_azimuth = (azimuth - 270) % 360
    elif direction == 'south':
        relative_azimuth = azimuth 
    elif direction == 'west':
        relative_azimuth = (azimuth - 90) % 360

    # Determine panning based on relative azimuth
    if 0 <= relative_azimuth < 180:
        pan_left = (360 - relative_azimuth) / 180
        pan_right = 1.0 - (360 - relative_azimuth) / 180
    else:
        pan_left = 1.0 - relative_azimuth / 180
        pan_right = relative_azimuth / 180
        

    pan_left *= attenuation
    pan_right *= attenuation

    lft = np.squeeze(hrir_left[azimuth_idx][elevation_idx][:]) * pan_left
    rgt = np.squeeze(hrir_right[azimuth_idx][elevation_idx][:]) * pan_right
    left_convolved = fftconvolve(data[:, 0], lft, mode='full')
    right_convolved = fftconvolve(data[:, 1], rgt, mode='full')
    # stereo_frame = np.vstack([left_convolved[:buffer_size], right_convolved[:buffer_size]]).T
    # stream.write(stereo_frame.astype(np.float32).tobytes())

    # left_convolved = fftconvolve(data, hrir_left[azimuth_idx][elevation_idx] * pan_left, mode='full')
    # right_convolved = fftconvolve(data, hrir_right[azimuth_idx][elevation_idx] * pan_right, mode='full')

    return np.stack([left_convolved, right_convolved], axis=1)

# Thread for mixing and playback
def mixer_and_playback(audio_queues, frame_size, sample_rate):
    while True:
        mixed_frame = None
        for queue in audio_queues.values():
            if not queue.empty():
                data = queue.get()
                data = process_frame(data)
                mixed_frame = data if mixed_frame is None else mixed_frame + data
        
        if mixed_frame is not None:
            stream.write(mixed_frame.astype(np.float32).tobytes())
        else:
            time.sleep(frame_size / sample_rate)

def client_thread():
    global user_pos, direction
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5001))
    print("Connected to the server.")
    buffer = ""
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            buffer += data.decode()
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if line:
                    position = line.split(',')
                    with position_lock:
                        user_pos = np.array([int(float(position[0])), int(float(position[1]))])
                        direction = position[2]
    finally:
        client_socket.close()
        p.terminate()
        print("Connection closed.")
# Main entry point
if __name__ == "__main__":
    
    threading.Thread(target=client_thread).start()
    audio_queues = {name: queue.Queue(maxsize=1) for name in sound_sources.keys()}
    src_threads = []
    for name, source in sound_sources.items():
        threading.Thread(target=source_processing, args=(source, audio_queues[name], 1024)).start()
    mixer_thread = threading.Thread(target=mixer_and_playback, args=(audio_queues, 1024, 44100))
    mixer_thread.start()
