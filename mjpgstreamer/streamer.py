import subprocess


def start_stream():
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

    return process
