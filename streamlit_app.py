import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import av

# Show title and description.
st.title("🤟 ASL Recognition System")
st.write(
    "Welcome to the ASL Recognition System! This app will soon integrate a model for recognizing American Sign Language. "
    "For now, you can use the buttons below to record videos and simulate ASL recognition."
)

# Instructions for ease of use.
st.markdown("### Instructions:")
st.markdown("""
1. **Enable Camera**: Check the box below to allow the app to access your webcam.
2. **Start Recording**: Click the '🎥 Start Recording' button to begin recording a video.
3. **Stop Recording**: Click the '🛑 Stop Recording' button to stop recording.
4. **Process Video**: Click the '⚙️ Process Video' button to simulate ASL recognition.
5. **View Results**: The recognized gesture will be displayed below.
""")

# Add a checkbox to enable/disable the camera.
enable_camera = st.checkbox("Enable Camera", value=False)

# Initialize session state to manage video recording.
if "recording" not in st.session_state:
    st.session_state.recording = False
if "video_frames" not in st.session_state:
    st.session_state.video_frames = []
if "recognized_gesture" not in st.session_state:
    st.session_state.recognized_gesture = None

# Custom VideoProcessor to capture frames.
class VideoRecorder(VideoProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        if st.session_state.recording:
            self.frames.append(frame.to_ndarray(format="bgr24"))
        return frame

# Start the WebRTC streamer.
if enable_camera:
    st.markdown("### Webcam Feed")
    webrtc_ctx = webrtc_streamer(
        key="video-recorder",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=VideoRecorder,
        media_stream_constraints={"video": True, "audio": False},
    )

# Buttons to start/stop recording.
col1, col2 = st.columns(2)
with col1:
    if st.button("🎥 Start Recording", disabled=not enable_camera or st.session_state.recording):
        st.session_state.recording = True
        st.session_state.video_frames = []  # Clear previous frames.
        st.write("Recording started! (Placeholder for video recording functionality.)")
with col2:
    if st.button("🛑 Stop Recording", disabled=not st.session_state.recording):
        st.session_state.recording = False
        if webrtc_ctx.video_processor:
            st.session_state.video_frames = webrtc_ctx.video_processor.frames
        st.write("Recording stopped! (Placeholder for video recording functionality.)")

# Display the recorded video frames if available.
if st.session_state.video_frames:
    st.markdown("### Recorded Video")
    for frame in st.session_state.video_frames:
        st.image(frame, caption="Recorded Frame", use_column_width=True)

# Placeholder buttons for processing and saving videos.
col1, col2 = st.columns(2)
with col1:
    if st.button("⚙️ Process Video", disabled=not st.session_state.video_frames):
        st.write("Processing video... (Placeholder for ASL recognition model.)")
        # Simulate a recognized gesture.
        st.session_state.recognized_gesture = "Hello"
with col2:
    if st.button("💾 Save Video", disabled="recognized_gesture" not in st.session_state):
        st.write("Video saved! (Placeholder for saving functionality.)")

# Placeholder for displaying recognized ASL gesture.
if st.session_state.recognized_gesture is not None:
    st.markdown("### Recognized ASL Gesture")
    st.write(f"Recognized Gesture: **{st.session_state.recognized_gesture}**")

# Optional: Add a button to clear results.
if st.button("🧹 Clear Results"):
    st.session_state.video_frames = []
    st.session_state.recognized_gesture = None
    st.write("Results cleared!")
