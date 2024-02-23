from multiprocessing import Process
import subprocess


def start_stream(parent_process: Process):
    # Inicie o mjpg-streamer em uma subprocesso
    process = subprocess.Popen(
        [
            "mjpg_streamer",
            "-o",
            "output_http.so -w ./www",
            "-i",
            "input_uvc.so",
        ]
    )

    # Mantenha o processo em execução enquanto o processo pai estiver ativo
    while parent_process.is_alive():
        # Verifique se o processo ainda está em execução
        if process.poll() is not None:
            # O processo terminou, então pare o loop
            break

        # Faça outras coisas enquanto o mjpg-streamer estiver em execução

    # Feche o processo mjpg-streamer
    process.terminate()