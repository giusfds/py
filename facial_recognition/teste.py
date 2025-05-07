import cv2
import numpy as np
import math

# Inicializa a captura da webcam
cap = cv2.VideoCapture(0)

while True:
    try:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        kernel = np.ones((3, 3), np.uint8)

        # Define a região de interesse (ROI)
        roi = frame[100:300, 100:300]

        cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Define o intervalo de cor da pele em HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)

        # Extrai a máscara da imagem HSV
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # Aplica morfologia
        mask = cv2.dilate(mask, kernel, iterations=4)
        mask = cv2.GaussianBlur(mask, (5, 5), 100)

        # Encontra os contornos
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Encontra o contorno máximo
        cnt = max(contours, key=lambda x: cv2.contourArea(x))

        # Aproxima o contorno
        epsilon = 0.0005 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Cria o casco convexo
        hull = cv2.convexHull(cnt)

        # Desenha os contornos
        cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
        cv2.drawContours(roi, [hull], -1, (0, 0, 255), 2)

        # Encontra os defeitos convexos
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)

        count_defects = 0

        # Conta os defeitos para estimar o número de dedos
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])

            # Calcula os lados do triângulo
            a = math.dist(start, end)
            b = math.dist(start, far)
            c = math.dist(end, far)

            # Calcula o ângulo usando a lei dos cossenos
            angle = math.acos((b**2 + c**2 - a**2) / (2*b*c)) * (180 / math.pi)

            # Se o ângulo for menor que 90°, considera como defeito
            if angle <= 90:
                count_defects += 1
                cv2.circle(roi, far, 5, (0, 0, 255), -1)

        # Exibe o número de dedos detectados
        if count_defects == 0:
            cv2.putText(frame, "1", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 1:
            cv2.putText(frame, "2", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 2:
            cv2.putText(frame, "3", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 3:
            cv2.putText(frame, "4", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 4:
            cv2.putText(frame, "5", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        else:
            cv2.putText(frame, "Reajuste a mao", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

    except:
        pass

    # Mostra a imagem final
    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    # Sai com a tecla Esc
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
