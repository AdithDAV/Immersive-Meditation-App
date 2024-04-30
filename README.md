# Project Title

## Description
This project is a Python-based application that uses 3D audio to enhance user experiences through two main features: Guided Narration and Nature Canvas. Users can interact with audio elements in a 3D space, providing an immersive sound environment. The application leverages the CIPIC HRTF database to simulate audio directionality and distance.

### Features
- **Guided Narration:** Play guided audio narratives with dynamic 3D sound effects allowing the narrator's position to move around the user.
- **Nature Canvas:** Explore a virtual environment where sound sources emit 3D audio as the user moves around them.

## Prerequisites
Before you run the application, ensure you have Python installed on your system. Python 3.6 or higher is recommended. The application depends on several Python libraries and external modules as outlined below.

## Install Dependencies

Before running the application, you need to install the required Python libraries. Ensure you have Python and Pip installed on your machine. Run the following command in your terminal to install all necessary dependencies:

```bash
pip install numpy soundfile pyaudio sounddevice pygame scipy tkinter
```

## Usage

To start the application, navigate to the project root directory and execute:
```bash
python home.py
```

## GUI Interaction

The application interface provides two main options for user interaction:

- **Guided Narration:**
  - To begin, click on the "Guided Narration" button in the main GUI.
  - This feature plays a narrative with 3D audio effects. The audio's spatial characteristics change dynamically as you use the GUI controls to move the narrator around the listener.
  - This interactive experience allows the listener to perceive the narrator from different directions, enhancing the realism of the audio playback.

- **Enjoy the Nature:**
  - Click on the "Enjoy the Nature" button to open the nature canvas.
  - In this mode, you enter a virtual environment populated with various sound sources.
  - As you navigate through this environment, the sound sources emit 3D audio. The spatial sound changes depending on your position relative to the sources, simulating a real-world experience.
  - This mode provides an immersive auditory experience that mimics walking through a natural landscape with varying audio cues depending on location and movement.

Each feature is designed to showcase the capabilities of 3D audio processing and the dynamic alteration of sound based on user interaction. Utilize the controls provided in the GUI to explore different aspects of auditory perception in a virtual space.

## Libraries Used

This application relies on a variety of Python libraries to handle different functionalities, from audio processing to GUI management. Below is a list of the main libraries used, along with their purposes:

- **Tkinter:** A standard GUI library for Python, used to create and manage graphical user interfaces. It provides widgets and tools to make interactive windows and controls.

- **PyAudio:** Acts as a Python binding for PortAudio, a cross-platform audio API. It is used for low-level audio playback, recording, and streaming.

- **SoundFile:** A library to read from and write to audio files in various formats. It is crucial for handling sound data input and output within the application.

- **SoundDevice:** An alternative to PyAudio that simplifies audio playback and recording tasks. Offers a more user-friendly interface for real-time audio processing.

- **Pygame:** Utilized for multimedia content in Python, extending capabilities in interactive sound elements and possibly for visual representations if needed in future developments.

- **NumPy:** Essential for numerical processing, particularly beneficial in handling large arrays and matrices which are often used in audio processing tasks.

- **SciPy:** Provides tools for scientific and technical computing. Within this project, it's particularly useful for signal processing tasks such as filtering and Fourier transforms.

- **Threading:** A module for running different parts of the program concurrently, enabling the application to perform intensive computations while maintaining a responsive GUI.

- **Queue:** Helps in managing threads, especially useful for handling data exchange between multiple threads without risking data corruption.

These libraries collectively support the complex functionality required to manipulate and present 3D audio effectively, ensuring a seamless and interactive user experience.

## Design Decisions for Perceptual Consideration

In developing this application, several key design decisions were made with a focus on enhancing user perception and interaction:

- **Spatial Audio Localization:**
  - **Decision:** Integration of the CIPIC HRTF database for accurate 3D audio localization.
  - **Perceptual Consideration:** This enhances the realism and immersion of the audio experience, aiding users in navigating virtual environments through auditory cues, especially in visually complex scenes.

- **Dynamic Audio Adjustment:**
  - **Decision:** Audio properties such as volume, pitch, and echo dynamically adjust in response to the user's relative movement in the environment.
  - **Perceptual Consideration:** Mimics real-world acoustic behavior, making the interaction more intuitive and engaging by aligning sound changes with user movements.

- **User-Controlled Interaction:**
  - **Decision:** Users can manipulate the positions of audio sources and their own listener position within the virtual space.
  - **Perceptual Consideration:** Provides users with control and agency, enhancing engagement and allowing for personal exploration of the sound landscape, which can be particularly beneficial for educational and entertainment purposes.
 
- **Guided Narration:**
  Our application controls the narrator's movement using keyboard keys, enabling the narrator’s voice to emanate from various directions. This decision enhances cognitive engagement by leveraging the benefits of spatial audio cues, which stimulate different brain signals related to attention and spatial awareness.

  Core Functionality and Future Enhancements:
     - **Current Implementation:** Uses straightforward keyboard controls to ensure the application is accessible and easy to use, laying a solid foundation for core functionality.
     - **AI Integration Potential:** Future updates can incorporate AI to automate and enhance narrator movements, improving the dynamic interaction and personalization of the narrative experience based on user feedback and advances in technology.

- **Enjoy the Nature feature:**
  - **Multisensory Stimulation:** Movement in our app is designed to interact with the 3D audio environment, providing a multisensory experience that can deepen the meditative state. As users move, the changing audio cues can help to anchor their attention in the present moment, a fundamental aspect of meditation.

These decisions are fundamental in creating an interactive and immersive auditory environment that is both intuitive and enjoyable for users.

## Authors
- Uma Saisree Avula
- Darshini Ram Mattaparthi
- Dharmesh Adith Varma Penmetsa

