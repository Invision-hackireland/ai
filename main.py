from invision_ai import VideoAnnotator, VideoAnalyzer

CAMERA_ID = "ba318312-f182-11ef-80e2-c3f14977a210"
USER_ID = "ba3197a8-f182-11ef-80e2-77fbe9534181"

def main():
    # Initialize the VideoAnnotator (GOOGLE_API_KEY is loaded from .env if not passed)
    annotator = VideoAnnotator()
    # Run the analysis for a given camera and video file path
    annotations = annotator.run(camera_id=CAMERA_ID, video_file_path="./sample_data/video2.mp4")
    print("Video Annotations:")
    print(annotations)
    
    # Now, initialize the VideoAnalyzer (OPENAI_API_KEY is loaded from .env if not passed)
    analyzer = VideoAnalyzer()
    # Analyze the annotations for potential code-of-conduct breaches
    breach_reports = analyzer.analyze(annotations, camera_id=CAMERA_ID, user_id=USER_ID)

    print("\nBreach Reports:")
    if breach_reports:
        for report in breach_reports:
            print(report)
    else:
        print("No breaches detected.")

if __name__ == "__main__":
    main()
