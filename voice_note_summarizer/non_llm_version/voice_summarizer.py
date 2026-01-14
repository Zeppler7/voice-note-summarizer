import speech_recognition as sr
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def record_audio(duration=10, test_mode=False, mic_index=None):
    """
    Record audio from microphone for specified duration.
    In test mode, returns None to simulate no audio.
    """
    if test_mode:
        print(f"Test mode: Simulating {duration} seconds of recording...")
        return None

    recognizer = sr.Recognizer()

    try:
        # Try to use specified microphone or default
        if mic_index is not None:
            print(f"Using microphone {mic_index}")
            with sr.Microphone(device_index=mic_index) as source:
                print(f"Recording for {duration} seconds... Speak now!")
                print("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = recognizer.listen(source, timeout=duration)
        else:
            with sr.Microphone() as source:
                print(f"Recording for {duration} seconds... Speak now!")
                print("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = recognizer.listen(source, timeout=duration)

        print("Recording completed.")
        return audio
    except sr.WaitTimeoutError:
        print("No audio detected within timeout period.")
        return None
    except Exception as e:
        print(f"Error accessing microphone: {e}")
        print("Try running with --test flag for testing without microphone.")
        return None

def transcribe_audio(audio):
    """
    Transcribe audio to text using Google Speech Recognition.
    """
    recognizer = sr.Recognizer()

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

def extractive_summarize(text, num_sentences=3):
    """
    Create an extractive summary by selecting the most important sentences.
    """
    if not text or text in ["Could not understand audio", ""]:
        return "No valid text to summarize."

    # Tokenize into sentences
    sentences = sent_tokenize(text)

    if len(sentences) <= num_sentences:
        return text

    # Preprocess text
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())

    # Remove punctuation and stop words
    words = [word for word in words if word not in stop_words and word not in string.punctuation]

    # Calculate word frequencies
    word_freq = Counter(words)

    # Score sentences based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        sentence_words = word_tokenize(sentence.lower())
        sentence_words = [word for word in sentence_words if word not in string.punctuation]
        score = sum(word_freq.get(word, 0) for word in sentence_words)
        sentence_scores[sentence] = score

    # Select top sentences
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    summary = ' '.join([sentence for sentence, score in sorted(top_sentences, key=lambda x: sentences.index(x[0]))])

    return summary

def main(test_mode=False, mic_index=None):
    print("AI Voice Note Summarizer (Non-LLM Version)")
    print("=" * 50)

    # Record audio
    audio = record_audio(duration=10, test_mode=test_mode, mic_index=mic_index)

    # Transcribe
    print("Transcribing...")
    if test_mode or audio is None:
        # Use sample transcription for testing
        transcription = "This is a test voice note. I need to remember to call John about the project deadline. The meeting is scheduled for tomorrow at 2 PM. We discussed the budget allocation and decided to increase the marketing spend by 20 percent. Action items include preparing the presentation slides and sending the agenda to all participants."
        print("Using test transcription (no microphone available)")
    else:
        transcription = transcribe_audio(audio)

    print(f"Transcription: {transcription}")

    # Summarize
    print("Summarizing...")
    summary = extractive_summarize(transcription)
    print(f"Summary: {summary}")

if __name__ == "__main__":
    import sys
    test_mode = "--test" in sys.argv

    # Check for microphone index
    mic_index = None
    if "--mic" in sys.argv:
        try:
            mic_idx = sys.argv.index("--mic")
            if mic_idx + 1 < len(sys.argv):
                mic_index = int(sys.argv[mic_idx + 1])
        except (ValueError, IndexError):
            print("Invalid microphone index. Use --mic <number>")
            sys.exit(1)

    main(test_mode=test_mode, mic_index=mic_index)