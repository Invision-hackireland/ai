from invision_ai import VideoAnnotator

# Initialize the annotator (the API key will be loaded from .env if not passed).
annotator = VideoAnnotator()

# Run the analysis for a given camera and video file path.
analysis_report = annotator.run(camera_id="camera1", video_file_path="./sample_data/video.mp4")
print(analysis_report)