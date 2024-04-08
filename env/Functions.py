from mido import Message, MidiFile, MidiTrack, note
import io
from typing import BinaryIO
from PIL import Image, ImageDraw

def compose_melody():
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=12))

    melody = [60, 62, 64, 65, 67, 69, 71, 72] # C Major scale

    for note in melody:
        track.append(Message('note_on', note=note, velocity=64, time=32))
        track.append(Message('note_off', note=note, velocity=127, time=32))

    midi_bytes_io = io.BytesIO()
    mid.save(file=midi_bytes_io)
    midi_bytes_io.seek(0)

    return midi_bytes_io

def compose_music_midi() -> BinaryIO:
    """Compose a melody and send it in midi format"""
    # A simple melody
    notes = [
      ('C4', '4'), ('D4', '4'), ('E4', '4'), ('D4', '4'),
      ('C4', '4'), ('D4', '4'), ('E4', '4'), ('C4', '4'),
      ('D4', '4'), ('E4', '4'), ('F4', '8'), ('E4', '8'),
      ('D4', '4'), ('F4', '4'), ('E4', '4'), ('C4', '4'),
      ('C4', '4'), ('D4', '4'), ('E4', '4'), ('D4', '4')
    ]
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    for note, duration in notes:
        track.append(Message('note_on', note=note_to_int(note), velocity=64, time=0))
        track.append(Message('note_off', note=note_to_int(note), velocity=64, time=int(duration)))

    # Convert MIDI file to bytes
    midi_bytes_io = io.BytesIO()
    mid.save(file=midi_bytes_io)
    midi_bytes_io.seek(0)

    return midi_bytes_io

def draw_sun_PNG() -> BinaryIO:
    """Draw a sun """
    size = (100, 100)
    image = Image.new('RGB', size, color = 'skyblue')
    draw = ImageDraw.Draw(image)
    draw.ellipse((25, 25, 75, 75), fill='yellow')
    image_bytes = io.BytesIO()
    image.save(image_bytes, 'PNG')
    image_bytes.seek(0)
    return image_bytes
