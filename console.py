#!/usr/bin/python3
"""
The console module
"""
import cmd
from Traitement.Speech2Text import extract_audio_from_youtube, speech_to_text
from Traitement.zephyrChat import check


class TrueD(cmd.Cmd):
    """ contains the entry point of the command interpreter """
    prompt = "TrueDetective:~# "

    def do_EOF(self, line):
        """ end of file """
        return True

    def do_check(self, line):
        """
        Extracting audio from YouTube videos and checking it
        for false information
        :param line[0]: YouTube video url or local video path
        :return: pdf file of checking results
        """
        command = line.split()
        try:
            link = command[0]
            file = {"file": open(extract_audio_from_youtube(link), "rb")}
            text = speech_to_text(file)
            print(check(text))
        except IndexError:
            print('Please enter Youtube URL')

    def do_translate(self, line):
        """
        Extracting audio from YouTube videos and translate it
        :param line[0]: YouTube video url or local video path
        :return: pdf file of translation
        """
        command = line.split()
        try:
            link = command[0]
            lang = input('Language: ')
            file = {"file": open(extract_audio_from_youtube(link), "rb")}
            text = speech_to_text(file, lang, True)
            print(text)
        except IndexError:
            print('Please enter Youtube URL')

    def do_quit(self, line):
        """ exit the cmd """
        return True

    def emptyline(self):
        """ new line if command is empty """
        pass


if __name__ == '__main__':
    TrueD().cmdloop()
