import cv2
import numpy as np

from singleton import Singleton


class LightningDetect(Singleton):
    """Detecta relâmpagos em um vídeo usando processamento de imagem e HSV.

    A classe usa captura de vídeo, limiarização HSV e análise de contornos para identificar
    pixels brilhantes que podem representar relâmpagos. O centroide e a área de cada
    relâmpago detectado são enviados através de um pipe para posterior processamento
    ou visualização.

    Atributos:
        detection_id (str, opcional): Identificador único para a detecção.
        pipe (callable, opcional): Função para enviar dados de detecção.
        cap (cv2.VideoCapture): Objeto de captura de vídeo.
        lower (np.array): Limite inferior da faixa de HSV para detecção de relâmpagos.
        upper (np.array): Limite superior da faixa de HSV para detecção de relâmpagos.

    Métodos:
        __init__ (opcional detection_id, opcional pipe): Inicializa a instância.
        _initialize_resources: Inicializa a captura de vídeo e os limites de HSV.
        @classmethod instance: Retorna a instância singleton.
        find_centroid (contour): Encontra o centroide de um contorno.
        detecting_process: Loop principal de detecção de relâmpagos.
    """

    def __init__(self, detection_id=None, pipe=None):
        """
        Inicializa a instância com configuração opcional.

        Args:
            detection_id (str, opcional): Identificador único para a detecção.
            pipe (callable, opcional): Função para enviar dados de detecção.

        Se chamado sem argumentos, acessa atributos da instância existente.
        """

        # Allow accessing attributes on subsequent calls without arguments
        if not (detection_id or pipe):
            return

        # Initialize attributes only on the first call with arguments
        self.pipe = pipe
        self.detection_id = detection_id

        # Initialize resources in a protected method to avoid duplication
        self._initialize_resources()

    def _initialize_resources(self):
        """Inicializa o dispositivo de captura e os limites com tratamento adequado de erros."""
        try:
            self.cap = cv2.VideoCapture(0)
            self.lower = np.array([80, 50, 50])
            self.upper = np.array([90, 255, 255])
        except (cv2.error, Exception) as e:
            print("Error initializing resources:", e)

    @classmethod
    def instance(cls):
        """Retorna a instância singleton."""
        return cls()

    def find_centroid(self, contour):
        """Encontra o centroide de um contorno.

        Args:
            contour: Contorno do objeto detectado.

        Retorna:
            (int, int): Coordenadas (x, y) do centroide.
        """
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return cX, cY
        else:
            return 0, 0

    def detecting_process(self):
        """Loop principal de detecção de relâmpagos."""
        while True:
            ret, frame = self.cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            part_mask = cv2.inRange(hsv, self.lower, self.upper)
            mask = cv2.bitwise_or(part_mask, part_mask)
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:
                area = cv2.contourArea(contour)

                if area > 500:
                    cx, cy = self.find_centroid(contour)

                    self.pipe.send((self.detection_id, cx, cy, area, frame))

                    cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            cv2.imshow("Object Tracking", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()
