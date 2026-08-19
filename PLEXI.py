import os
import importlib.util


# ==========================================
# PLEXI / PLX1 V1.0
# NVIDIA ANA MOTOR
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


MODEL_NAME = "PLX1"
VERSION = "V1.0"


# ==========================================
# MODÜL YÜKLEYİCİ
# ==========================================

def load_module(filename, module_name):

    path = os.path.join(
        BASE_DIR,
        filename
    )

    if not os.path.exists(path):
        return None

    try:

        spec = importlib.util.spec_from_file_location(
            module_name,
            path
        )

        module = importlib.util.module_from_spec(
            spec
        )

        spec.loader.exec_module(module)

        return module

    except Exception as error:

        print(f"[HATA] {filename}: {error}")

        return None


# ==========================================
# NVIDIA
# ==========================================

nvidia = load_module(
    "nvidia.py",
    "nvidia"
)


# ==========================================
# SİSTEM DURUMU
# ==========================================

def system_status():

    print()
    print("================================")
    print("          PLEXI / PLX1")
    print("             V1.0")
    print("================================")

    print(
        "NVIDIA:",
        "AKTİF" if nvidia else "YOK"
    )

    print("Brain: KAPALI")
    print("PLX Ultra: HAZIR DEĞİL")
    print("================================")
    print()


# ==========================================
# NVIDIA CEVABI
# ==========================================

def ask_nvidia(question):

    if nvidia is None:
        return None

    if not hasattr(
        nvidia,
        "ask_nvidia"
    ):
        print(
            "[UYARI] NVIDIA fonksiyonu bulunamadı."
        )
        return None

    try:

        return nvidia.ask_nvidia(
            question
        )

    except Exception as error:

        print(
            "[NVIDIA HATASI]",
            error
        )

        return None


# ==========================================
# PLX1 DÜŞÜNME MOTORU
# ==========================================

def think(question):

    question = question.strip()

    if not question:

        return "Bir şey yazmalısın."

    print(
        "\n[PLX1] NVIDIA Nemotron çalışıyor..."
    )

    answer = ask_nvidia(
        question
    )

    if answer:

        return answer

    return (
        "PLX1 şu anda cevap oluşturamadı."
    )


# ==========================================
# KOMUTLAR
# ==========================================

def handle_command(command):

    command = command.lower().strip()

    if command == "durum":

        system_status()

        return True

    if command == "help":

        print()
        print("PLEXI komutları:")
        print()
        print("durum  → sistem durumunu gösterir")
        print("help   → yardım")
        print("çıkış  → programı kapatır")
        print()

        return True

    return False


# ==========================================
# TERMINAL
# ==========================================

def terminal():

    system_status()

    print("PLEXI hazır.")
    print("Çıkmak için 'çıkış' yaz.")
    print()

    while True:

        try:

            question = input(
                "Sen: "
            ).strip()

        except KeyboardInterrupt:

            print(
                "\n\nPLEXI kapatıldı."
            )

            break

        except EOFError:

            print(
                "\n\nPLEXI kapatıldı."
            )

            break

        if not question:
            continue

        if question.lower() == "çıkış":

            print(
                "Plexi: Görüşürüz!"
            )

            break

        if handle_command(question):
            continue

        answer = think(
            question
        )

        print()
        print(
            "Plexi:",
            answer
        )
        print()


# ==========================================
# BAŞLAT
# ==========================================

if __name__ == "__main__":

    terminal()