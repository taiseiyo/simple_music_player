#!/usr/bin/env python3
from pyfzf.pyfzf import FzfPrompt
from mutagen.mp3 import MP3
import argparse
import pygame
import time
import glob
import os

pygame.mixer.init()
fzf = FzfPrompt()
os.chdir(os.getenv("HOME") + "/Downloads/music/")


def option_parser():
    parser = argparse.ArgumentParser(
        description="Select play mode. If there is no argument, select one song at a time")

    parser.add_argument(
        '-r', '--repeat', action="store_true", help='repeat music')
    parser.add_argument(
        '-c', '--continuous', action="store_true", help='play music continuously')
    option = parser.parse_args()
    return option


def get_file(repeat=False, continuous=False):
    # filename is list object
    if(repeat):
        filename = fzf.prompt(
            glob.glob("*mp3"))
        audio = MP3(filename[0])
        return filename[0], audio

    elif(continuous):
        filename = glob.glob("*mp3")
        return filename

    filename = fzf.prompt(
        glob.glob("*mp3"))
    audio = MP3(filename[0])
    return filename[0], audio


def play_music(filename, audio):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(1)
    time.sleep(audio.info.length+0.5)
    pygame.mixer.music.stop()


def main():
    option = option_parser()
    if(option.repeat):
        filename, audio = get_file(option.repeat)
        while True:
            play_music(filename, audio)

    elif(option.continuous):
        filename = get_file(False, option.continuous)
        for name in filename:
            audio = MP3(name)
            play_music(name, audio)

    while True:
        filename, audio = get_file()
        play_music(filename, audio)
        if(input() == "q"):
            break


main()
