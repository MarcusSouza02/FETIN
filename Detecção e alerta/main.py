import cv2
import torch
from ultralytics import YOLO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

EMAIL_REMETENTE = 'mvfariadesouza@gmail.com'
EMAIL_DESTINATARIO = 'marcus.souza@ges.inatel.br'
SENHA_APP = ''

def enviar_email_com_foto(imagem_path):
    assunto = 'POSSÍVEL FURTO DETECTADO!'
    corpo = 'Um possivel furto foi detectada pelo sistema de monitoramento. Veja a imagem em anexo.'

    msg = MIMEMultipart()
    msg['Subject'] = assunto
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO
    msg.attach(MIMEText(corpo, 'plain'))

    with open(imagem_path, 'rb') as f:
        imagem = MIMEImage(f.read())
        imagem.add_header('Content-Disposition', 'attachment', filename='pessoa_detectada.jpg')
        msg.attach(imagem)


    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(EMAIL_REMETENTE, SENHA_APP)
            servidor.send_message(msg)
        print("🔔 E-mail com imagem enviado com sucesso!")
    except Exception as e:
        print(f" Erro ao enviar e-mail: {e}")

model = YOLO("yolov8n.pt")

video_source = 0
cap = cv2.VideoCapture(video_source)
cap.set(3, 640)
cap.set(4, 480)

if not cap.isOpened():
    print("Erro ao abrir a câmera!")
    exit()

email_enviado = False 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, device="cpu")

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            label = result.names[int(box.cls[0])]

            if label == "person" and conf > 0.5:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if not email_enviado:
                    pessoa_detectada = frame[y1:y2, x1:x2]
                    caminho_imagem = "pessoa_detectada.jpg"
                    cv2.imwrite(caminho_imagem, pessoa_detectada)

                    enviar_email_com_foto(caminho_imagem)
                    email_enviado = True

    cv2.imshow("Detecção de Pessoas", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
