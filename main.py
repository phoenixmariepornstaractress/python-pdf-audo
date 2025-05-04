import pyttsx3
import PyPDF2
import os
from io import BytesIO
from pydub import AudioSegment  # Requires pip install pydub
from pydub.playback import play  # Requires simpleaudio

def read_pdf_and_speak(pdf_path='book.pdf', output_filename='story.mp3', rate=150, volume=1.0, voice=None):
    """
    Reads text from a PDF file, prints it to the console, and saves it as an MP3 audio file.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdfreader = PyPDF2.PdfReader(pdf_file)
            speaker = pyttsx3.init()
            all_text = ""
            speaker.setProperty('rate', rate)
            speaker.setProperty('volume', volume)
            if voice:
                try:
                    speaker.setProperty('voice', voice)
                except ValueError:
                    print(f"Warning: Voice ID '{voice}' not found. Using default voice.")
            for page_num in range(len(pdfreader.pages)):
                text = pdfreader.pages[page_num].extract_text()
                clean_text = text.strip().replace('\n', ' ')
                print(clean_text)
                all_text += clean_text + " "
            speaker.save_to_file(all_text, output_filename)
            speaker.runAndWait()
            speaker.stop()
            print(f"\nSuccessfully saved the PDF content as '{output_filename}'")
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found. Please make sure the path is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_available_voices():
    """
    Lists the available voices for text-to-speech.
    """
    speaker = pyttsx3.init()
    voices = speaker.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"[{i}] ID: {voice.id}")
        print(f"    Name: {voice.name}")
        print(f"    Languages: {voice.languages}")
        print(f"    Gender: {voice.gender}")
        print(f"    Age: {voice.age}")
        print("-" * 20)
    speaker.stop()

def split_audio_by_page(pdf_path='book.pdf', output_prefix='page_', rate=150, volume=1.0, voice=None):
    """
    Reads each page of a PDF and saves the audio of each page as a separate MP3 file.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdfreader = PyPDF2.PdfReader(pdf_file)
            speaker = pyttsx3.init()
            speaker.setProperty('rate', rate)
            speaker.setProperty('volume', volume)
            if voice:
                try:
                    speaker.setProperty('voice', voice)
                except ValueError:
                    print(f"Warning: Voice ID '{voice}' not found. Using default voice.")
            for page_num in range(len(pdfreader.pages)):
                text = pdfreader.pages[page_num].extract_text()
                clean_text = text.strip().replace('\n', ' ')
                output_filename = f"{output_prefix}{page_num + 1}.mp3"
                speaker.save_to_file(clean_text, output_filename)
                print(f"Saved page {page_num + 1} as '{output_filename}'")
            speaker.runAndWait()
            speaker.stop()
            print("\nSuccessfully saved audio for each page.")
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found. Please make sure the path is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")

def change_speech_rate(new_rate):
    """
    Changes the speaking rate for the text-to-speech engine.
    """
    speaker = pyttsx3.init()
    speaker.setProperty('rate', new_rate)
    print(f"Speech rate set to {new_rate} words per minute.")
    speaker.stop()

def change_speech_volume(new_volume):
    """
    Changes the speaking volume for the text-to-speech engine.
    """
    speaker = pyttsx3.init()
    if 0.0 <= new_volume <= 1.0:
        speaker.setProperty('volume', new_volume)
        print(f"Speech volume set to {new_volume}.")
    else:
        print("Error: Volume must be between 0.0 and 1.0.")
    speaker.stop()

def set_speech_voice(voice_id):
    """
    Sets a specific voice for the text-to-speech engine.
    Use get_available_voices() to see the available voice IDs.
    """
    speaker = pyttsx3.init()
    try:
        speaker.setProperty('voice', voice_id)
        print(f"Speech voice set to '{voice_id}'.")
    except ValueError:
        print(f"Error: Voice ID '{voice_id}' not found.")
    speaker.stop()

def read_specific_pages(pdf_path='book.pdf', pages_to_read=None, output_filename='selected_pages.mp3', rate=150, volume=1.0, voice=None):
    """
    Reads text from specific pages of a PDF file, prints it, and saves it as an MP3.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdfreader = PyPDF2.PdfReader(pdf_file)
            speaker = pyttsx3.init()
            selected_text = ""
            speaker.setProperty('rate', rate)
            speaker.setProperty('volume', volume)
            if voice:
                try:
                    speaker.setProperty('voice', voice)
                except ValueError:
                    print(f"Warning: Voice ID '{voice}' not found. Using default voice.")
            num_pages = len(pdfreader.pages)
            pages_to_process = []
            if pages_to_read is None:
                pages_to_process = range(num_pages)
            elif isinstance(pages_to_read, str):
                page_ranges = pages_to_read.split(',')
                for page_range in page_ranges:
                    if '-' in page_range:
                        start, end = map(int, page_range.split('-'))
                        pages_to_process.extend(range(start - 1, end))
                    else:
                        pages_to_process.append(int(page_range) - 1)
            elif isinstance(pages_to_read, list):
                pages_to_process = [p - 1 for p in pages_to_read]
            for page_num in sorted(list(set(pages_to_process))):
                if 0 <= page_num < num_pages:
                    text = pdfreader.pages[page_num].extract_text()
                    clean_text = text.strip().replace('\n', ' ')
                    print(f"Page {page_num + 1}: {clean_text[:100]}...")
                    selected_text += clean_text + " "
                else:
                    print(f"Warning: Page number {page_num + 1} is out of range.")
            if selected_text:
                speaker.save_to_file(selected_text, output_filename)
                speaker.runAndWait()
                print(f"\nSuccessfully saved selected pages as '{output_filename}'")
            else:
                print("No text extracted from the specified pages.")
            speaker.stop()
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_pdf_from_memory(pdf_content, output_filename='memory_audio.mp3', rate=150, volume=1.0, voice=None):
    """
    Reads text from PDF content provided in memory (as bytes) and saves it as MP3.
    """
    try:
        pdf_stream = BytesIO(pdf_content)
        pdfreader = PyPDF2.PdfReader(pdf_stream)
        speaker = pyttsx3.init()
        all_text = ""
        speaker.setProperty('rate', rate)
        speaker.setProperty('volume', volume)
        if voice:
            try:
                speaker.setProperty('voice', voice)
            except ValueError:
                print(f"Warning: Voice ID '{voice}' not found. Using default voice.")
        for page_num in range(len(pdfreader.pages)):
            text = pdfreader.pages[page_num].extract_text()
            clean_text = text.strip().replace('\n', ' ')
            print(f"Page {page_num + 1}: {clean_text[:100]}...")
            all_text += clean_text + " "
        speaker.save_to_file(all_text, output_filename)
        speaker.runAndWait()
        speaker.stop()
        print(f"\nSuccessfully saved audio from memory as '{output_filename}'")
    except Exception as e:
        print(f"An error occurred while reading from memory: {e}")

def get_speech_engine_info():
    """
    Prints information about the currently initialized speech engine.
    """
    speaker = pyttsx3.init()
    engine_name = speaker.getProperty('engine')
    print(f"Speech Engine: {engine_name}")
    speaker.stop()

def save_speech_to_file(text_to_speak, output_filename='custom_speech.mp3', rate=150, volume=1.0, voice=None):
    """
    Synthesizes the given text and saves it to an MP3 file without reading from a PDF.
    """
    speaker = pyttsx3.init()
    speaker.setProperty('rate', rate)
    speaker.setProperty('volume', volume)
    if voice:
        try:
            speaker.setProperty('voice', voice)
        except ValueError:
            print(f"Warning: Voice ID '{voice}' not found. Using default voice.")
    speaker.save_to_file(text_to_speak, output_filename)
    speaker.runAndWait()
    speaker.stop()
    print(f"\nSuccessfully saved custom speech to '{output_filename}'")

def play_audio_file(audio_path):
    """
    Plays the specified audio file. Requires the 'pydub' and 'simpleaudio' libraries.
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        play(audio)
        print(f"Playing audio file: '{audio_path}'")
    except FileNotFoundError:
        print(f"Error: Audio file '{audio_path}' not found.")
    except Exception as e:
        print(f"An error occurred while playing audio: {e}")

def convert_pdf_to_text(pdf_path='book.pdf', output_text_file='output.txt'):
    """
    Extracts all text content from a PDF and saves it to a text file.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdfreader = PyPDF2.PdfReader(pdf_file)
            all_text = ""
            for page_num in range(len(pdfreader.pages)):
                text = pdfreader.pages[page_num].extract_text()
                all_text += text + "\n\n"
        with open(output_text_file, 'w', encoding='utf-8') as text_file:
            text_file.write(all_text)
        print(f"Successfully extracted text to '{output_text_file}'")
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred during text extraction: {e}")

def get_pdf_metadata(pdf_path='book.pdf'):
    """
    Retrieves and prints the metadata of the PDF file (author, title, etc.).
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdfreader = PyPDF2.PdfReader(pdf_file)
            metadata = pdfreader.metadata
            if metadata:
                print("PDF Metadata:")
                for key, value in metadata.items():
                    print(f"{key}: {value}")
            else:
                print("No metadata found for this PDF.")
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading metadata: {e}")

def adjust_speech_settings(rate=None, volume=None, voice_id=None):
    """
    Allows dynamic adjustment of speech rate, volume, and voice for the pyttsx3 engine.
    """
    speaker = pyttsx3.init()
    if rate is not None:
        speaker.setProperty('rate', rate)
        print(f"Speech rate set to {rate} words per minute.")
    if volume is not None:
        if 0.0 <= volume <= 1.0:
            speaker.setProperty('volume', volume)
            print(f"Speech volume set to {volume}.")
        else:
            print("Error: Volume must be between 0.0 and 1.0.")
    if voice_id is not None:
        try:
            speaker.setProperty('voice', voice_id)
            print(f"Speech voice set to '{voice_id}'.")
        except ValueError:
            print(f"Error: Voice ID '{voice_id}' not found.")
    speaker.stop()

def stop_speaking():
    """
    Immediately stops any ongoing speech.
    """
    speaker = pyttsx3.init()
    if speaker.isBusy():
        speaker.stop()
        print("Speech stopped.")
    else:
        print("No speech is currently in progress.")

def pause_resume_speaking(action='toggle'):
    """
    Pauses or resumes the speech. Requires further implementation based on the backend.
    Note: This functionality might not be universally supported by all pyttsx3 backends.
    """
    speaker = pyttsx3.init()
    print("Pause/Resume functionality is backend-dependent and might not be fully implemented.")
    speaker.stop() # Ensure the engine is not busy for future actions

def save_speech_to_wav(text_to_speak, output_filename='custom_speech.wav', rate=150, volume=1.0, voice=None):
    """
    Synthesizes the given text and saves it to a WAV audio file.
    """
    speaker = pyttsx3.init()
    speaker.setProperty('rate', rate)
    speaker.setProperty('volume', volume)
    if voice:
        try:
            speaker.setProperty('voice', voice)
        except ValueError:
            print(f"Warning: Voice ID '{voice}' not found. Using default voice.")
    speaker.save_to_file(text_to_speak, output_filename)
    speaker.runAndWait()
    speaker.stop()
    print(f"\nSuccessfully saved custom speech to '{output_filename}' as WAV.")

if __name__ == "__main__":
    print("--- Reading and Speaking Entire PDF ---")
    read_pdf_and_speak()

    print("\n--- Getting Available Voices ---")
    get_available_voices()

    print("\n--- Splitting Audio by Page ---")
    split_audio_by_page()

    print("\n--- Changing Speech Rate ---")
    change_speech_rate(170)
    read_pdf_and_speak(rate=170, output_filename='story_faster.mp3')

    print("\n--- Changing Speech Volume ---")
    change_speech_volume(0.6)
    read_pdf_and_speak(volume=0.6, output_filename='story_quieter.mp3')

    print("\n--- Reading Specific Pages ---")
    read_specific_pages(pages_to_read=[1, 3, 5], output_filename='selected_1_3_5.mp3')
    read_specific_pages(pages_to_read='2-4', output_filename='selected_2_to_4.mp3')

    print("\n--- Reading PDF from Memory ---")
    try:
        with open('book.pdf', 'rb') as f:
            pdf_content = f.read()
            read_pdf_from_memory(pdf_content, output_filename='from_memory.mp3')
    except FileNotFoundError:
        print("Error: 'book.pdf' not found for memory reading example.")

    print("\n--- Getting Speech Engine Info ---")
    get_speech_engine_info()

    print("\n--- Saving Custom Speech ---")
    save_speech_to_file("This is

# Written by TiffinTech and Developed by phoenix marie.
