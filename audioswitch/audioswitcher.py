import subprocess
import os
import sys

# Nomes exatos dos dispositivos de áudio
headphones = "Headphones (HypereX Cloud Alpha Wireless)"
speakers = "SMT22A550 (NVIDIA High Definition Audio)"

# Caminho para o AudioSwitch
audio_switch_path = r"C:\Program Files (x86)\AudioSwitch\AudioSwitch.exe"

def get_current_device():
    try:
        result = subprocess.check_output([audio_switch_path, "-get"], stderr=subprocess.STDOUT)
        return result.decode().strip()
    except subprocess.CalledProcessError as e:
        print("Erro ao obter dispositivo atual:", e.output.decode().strip())
        sys.exit(1)
    except FileNotFoundError:
        print("AudioSwitch.exe não encontrado no caminho especificado.")
        sys.exit(1)

def set_device(device_name):
    try:
        subprocess.run([audio_switch_path, "-set", device_name], check=True)
        print(f"Dispositivo alterado para: {device_name}")
    except subprocess.CalledProcessError as e:
        print("Erro ao alterar dispositivo:", e)
        sys.exit(1)

def main():
    current_device = get_current_device().strip()
    if current_device == headphones:
        set_device(speakers)
    elif current_device == speakers:
        set_device(headphones)
    else:
        print(f"Dispositivo atual não reconhecido: {current_device}")
        # sys.exit(1)

if __name__ == "__main__":
    main()
