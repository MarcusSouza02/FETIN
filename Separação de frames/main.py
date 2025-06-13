import cv2
import os

video_path = r"C:\Users\mvfar\OneDrive\Desktop\mercado1.mp4"

output_dir = 'frames_extraidos'

if not os.path.exists(video_path):
    print("Caminho do vídeo inválido:", video_path)
else:
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Erro: Não foi possível abrir o vídeo.")
    else:
        os.makedirs(output_dir, exist_ok=True)
        count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_filename = os.path.join(output_dir, f"frame_{count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            count += 1

        cap.release()
        print(f"{count} frames salvos na pasta '{output_dir}'")
