import os
import numpy as np
import sounddevice as sd
from scipy.io import wavfile


class VoiceCloner:
    def __init__(self, language='es'):
        """
        Inicializa el clonador de voz basado en fonemas.

        :param language: Código de idioma (por defecto español)
        """
        self.language = language
        self.phoneme_folder = f"phoneme_samples_{language}"
        self.vowels = ['a', 'e', 'i', 'o', 'u']
        self.consonants = self.get_consonants()

        # Crear carpeta de muestras de fonemas si no existe
        if not os.path.exists(self.phoneme_folder):
            os.makedirs(self.phoneme_folder)

    def get_consonants(self):
        """
        Devuelve una lista de consonantes según el idioma.
        """
        consonants = {
            'es': ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'ñ', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x',
                   'z'],
            'en': ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
        }
        return consonants.get(self.language, [])

    def generate_phoneme_combinations(self):
        """
        Genera todas las combinaciones de fonemas.
        """
        phoneme_combinations = []

        # Vocales individuales
        phoneme_combinations.extend(self.vowels)

        # Consonantes individuales
        phoneme_combinations.extend(self.consonants)

        # Combinaciones vocal-consonante
        for vowel in self.vowels:
            for consonant in self.consonants:
                phoneme_combinations.append(vowel + consonant)

        # Combinaciones consonante-vocal
        for consonant in self.consonants:
            for vowel in self.vowels:
                phoneme_combinations.append(consonant + vowel)

        return phoneme_combinations

    def record_phoneme(self, phoneme):
        """
        Graba un fonema específico.

        :param phoneme: Fonema a grabar
        """
        print(f"Preparándose para grabar el fonema: {phoneme}")

        # Parámetros de grabación
        sample_rate = 44100  # Hz
        duration = 0.5  # segundos

        print(f"Grabe el fonema '{phoneme}'. Tiene {duration} segundos.")
        input("Presione Enter para comenzar la grabación...")

        # Grabar audio
        recording = sd.rec(int(duration * sample_rate),
                           samplerate=sample_rate,
                           channels=1,
                           dtype='float64')
        sd.wait()

        # Normalizar la grabación
        recording = recording / np.max(np.abs(recording))

        # Guardar grabación
        output_path = os.path.join(self.phoneme_folder, f"{phoneme}.wav")
        wavfile.write(output_path, sample_rate, recording)

        print(f"Fonema '{phoneme}' grabado y guardado en {output_path}")

    def synthesize_audio(self, text):
        """
        Sintetiza audio a partir de un texto usando muestras de fonemas.

        :param text: Texto a sintetizar
        :return: Audio sintetizado
        """
        # Dividir texto en palabras
        words = text.lower().split()

        # Lista para almacenar muestras de audio de palabras
        word_samples = []

        for word in words:
            word_audio = self.synthesize_word(word)
            if word_audio is not None:
                word_samples.append(word_audio)

        # Concatenar muestras de palabras
        if word_samples:
            synthesized_audio = np.concatenate(word_samples)
            return synthesized_audio
        else:
            print("No se pudieron sintetizar palabras")
            return None

    def synthesize_word(self, word):
        """
        Sintetiza audio para una palabra específica.

        :param word: Palabra a sintetizar
        :return: Audio de la palabra
        """
        word_length = len(word)
        word_samples = []

        # Estrategias de síntesis según longitud de la palabra
        if word_length == 1:
            # Para palabras de una letra, usar directamente la letra
            sample_path = os.path.join(self.phoneme_folder, f"{word}.wav")
            if os.path.exists(sample_path):
                _, sample = wavfile.read(sample_path)
                return sample

        elif word_length == 2:
            # Para palabras de dos letras, buscar registro de dos letras
            sample_path = os.path.join(self.phoneme_folder, f"{word}.wav")
            if os.path.exists(sample_path):
                _, sample = wavfile.read(sample_path)
                return sample

        elif word_length % 2 == 1:
            # Para palabras de longitud impar
            # Usar dos registros de vocal-consonante y uno de letra individual
            for i in range(0, word_length, 2):
                # Fonemas vocal-consonante
                if i < word_length - 1:
                    phoneme = word[i:i + 2]
                    sample_path = os.path.join(self.phoneme_folder, f"{phoneme}.wav")
                    if os.path.exists(sample_path):
                        _, sample = wavfile.read(sample_path)
                        word_samples.append(sample)

                # Letra individual al final
                if i == word_length - 1:
                    single_letter = word[i]
                    sample_path = os.path.join(self.phoneme_folder, f"{single_letter}.wav")
                    if os.path.exists(sample_path):
                        _, sample = wavfile.read(sample_path)
                        word_samples.append(sample)

        elif word_length % 2 == 0:
            # Para palabras de longitud par, usar registros de vocal-consonante
            for i in range(0, word_length, 2):
                phoneme = word[i:i + 2]
                sample_path = os.path.join(self.phoneme_folder, f"{phoneme}.wav")
                if os.path.exists(sample_path):
                    _, sample = wavfile.read(sample_path)
                    word_samples.append(sample)

        # Concatenar muestras de la palabra
        if word_samples:
            return np.concatenate(word_samples)
        else:
            print(f"No se pudieron sintetizar la palabra: {word}")
            return None

    def learning_phase(self):
        """
        Fase de aprendizaje: grabar muestras de fonemas.
        Omite fonemas ya grabados.
        """
        # Generar todas las combinaciones de fonemas
        phoneme_combinations = self.generate_phoneme_combinations()

        # Obtener fonemas ya grabados
        existing_phonemes = [f.split('.')[0] for f in os.listdir(self.phoneme_folder) if f.endswith('.wav')]

        # Calcular fonemas faltantes
        missing_phonemes = [phoneme for phoneme in phoneme_combinations if phoneme not in existing_phonemes]

        # Mostrar información de progreso
        print(f"Total de fonemas: {len(phoneme_combinations)}")
        print(f"Fonemas ya grabados: {len(existing_phonemes)}")
        print(f"Fonemas pendientes: {len(missing_phonemes)}")

        # Preguntar si desea continuar
        if missing_phonemes:
            continuar = input("¿Desea grabar los fonemas pendientes? (s/n): ").lower()

            if continuar == 's':
                for phoneme in missing_phonemes:
                    self.record_phoneme(phoneme)

                print("Fase de aprendizaje completada.")
            else:
                print("Grabación de fonemas cancelada.")
        else:
            print("Todos los fonemas ya han sido grabados.")


def main():
    """
    Función principal para interactuar con el clonador de voz.
    """
    cloner = VoiceCloner(language='es')

    while True:
        print("\n--- Clonador de Voz por Fonemas ---")
        print("1. Fase de Aprendizaje (Grabar Fonemas)")
        print("2. Sintetizar Audio")
        print("3. Salir")

        choice = input("Elija una opción: ")

        if choice == '1':
            cloner.learning_phase()
        elif choice == '2':
            texto = input("Introduzca el texto a sintetizar: ")
            audio_sintetizado = cloner.synthesize_audio(texto)

            if audio_sintetizado is not None:
                # Reproducir audio sintetizado
                sd.play(audio_sintetizado, 44100)
                sd.wait()
        elif choice == '3':
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    main()