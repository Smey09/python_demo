import cv2
import os
import subprocess

class RemoveWatermark:
    def __init__(self, input_path, output_path, temp_video_path):
        self.input_path = input_path
        self.output_path = output_path
        self.temp_video_path = temp_video_path

    def inpaint_watermark(self, regions, inpaint_radius=5, frame_step=1):
        cap = cv2.VideoCapture(self.input_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.temp_video_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (frame_width, frame_height))

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process every `frame_step` frame
            if frame_count % frame_step == 0:
                for (x, y, width, height) in regions:
                    mask = cv2.rectangle(
                        frame.copy(), (x, y), (x + width, y + height), (255, 255, 255), -1
                    )
                    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                    mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)[1]

                    # Apply inpainting with a specified radius
                    inpainted_frame = cv2.inpaint(frame, mask, inpaint_radius, cv2.INPAINT_TELEA)
                    frame[y:y + height, x:x + width] = inpainted_frame[y:y + height, x:x + width]

            out.write(frame)
            frame_count += 1

        cap.release()
        out.release()
        print(f"Video processed and saved to {self.temp_video_path}")

    def add_audio(self):
        # Use FFmpeg to add the audio back to the processed video
        command = [
            'ffmpeg', '-y', '-i', self.temp_video_path, '-i', self.input_path,
            '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0',
            self.output_path
        ]
        subprocess.run(command)
        print(f"Final video with audio saved to {self.output_path}")


# Example usage
if __name__ == "__main__":
    input_video = "tiktok_video.mp4"
    temp_video = "temp_video_no_audio.mp4"
    output_video = "tiktok_video_no_watermark_with_audio.mp4"

    watermark_remover = RemoveWatermark(input_video, output_video, temp_video)
    
    # Define the region for the watermark (adjust based on your watermark location)
    regions = [
        (20, 20, 150, 100)  # Example coordinates for the top-left watermark
    ]

    # Run the inpainting process to remove the watermark
    watermark_remover.inpaint_watermark(regions, inpaint_radius=7, frame_step=1)
    
    # Add the original audio back to the processed video
    watermark_remover.add_audio()
