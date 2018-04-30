#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This is an adaptation of Nico Broers' experiment "SART_Pilot"
# by Mathanja Verkaik

from psychopy import core, visual, event, logging, gui, data
from pylink import *
import gc  # Garbage collection control
import glob, random, time, codecs, pyglet
import pandas as pd
from my import *
import csv
import os  # Handy system and path functions


## Task parameters -------------------------------------------------------------------

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Define task parameters
expName = 'SARTmathanja'
startBlock = 1  # Start at Block 1
blockDur = 84  # Number of trials per block = 84
pracTrials = 11  # Number of practice trials = 11
answerKey = 'm'


## Text messages and filenames -------------------------------------------------------

# Define the text messages to be displayed
instruction = "You will first be asked to answer 2 questions. Once you've answered these further instructions will follow. \n\nPress any key to continue."
instruction1 = "In this experiment you will be shown words written in uppercase or lowercase as well as digits. Press the m-key when the word is written in lowercase (e.g. mountain) or when the digit is NOT a 3. It is important that you react as fast as possible. Don't press anything when the word is written in uppercase (e.g. BRIDGE) or the digit IS a 3. \n\n Press any key to continue."
instruction2 = "We know that people sometimes get distracted. For this reason you will occassionally be asked what you were thinking about. Please try to respond honestly. You can answer the questions by pressing the applicable key on the keyboard or adjusting the slider where applicable.\n\n Press any key to continue to some examples."
instruction3 = "We will start with a few practice questions. Contact the experimenter if you have any questions. \n\nPress any key to continue."
instruction4 = "The experiment wil start now. There will be several breaks during the experiment when you can rest your eyes. If anything is unclear do not hesitate to ask the experimenter. Good luck!\n\nPress any key to continue."
instruction5 = "Press any key to continue."
instruction6 = "You have finished the experiment. Contact the experimenter."
startQuestion1 = "Are you feeling stressed right now? \n1) Very stressed \n2) Stressed \n3) A little bit stressed \n4) Not stressed at all \n\nPress the number that fits your answer the best to continue. "
startQuestion2 = "Are you feeling happy right now? \n1) Very happy \n2) Happy \n3)A little bit happy \n4) Not happy at all \n\nPress the number that fits your answer the best to continue."
probeQuestion = "What were you thinking about?\n\n1) I was completely concentrated on the task. \n2) I was evaluating aspects of the task.\n(For example, how well you are doing or how long its taking)\n3) I was thinking about personal affairs.\n4) I was distracted by my surroundings.\n(For example, sound, temperature, my physical state) \n5) I was daydreaming / I was thinking about things task-unrelated. \n6) I wasn't paying attention, but wasn't thinking about anything specifically. \n\nPress the number that fits your answer the best to continue."
stickyQuestion = "How hard was it to let this thought go?\n\n1) Very difficult \n2) Difficult \n3) Not difficult nor easy \n4) Easy \n5) Very easy\n\nPress the number that fits your answer the best to continue."
temporalQuestion = "What were you thinking about? \n \n 1) Past \n 2) Present  \n 3) Future \n\nPress the number that fits your answer the best to continue."
valenceQuestion = "Were your thoughts positive, neutral or negative? \n \nUse the slider to indicate where your answer falls on the scale."
suggestBreak = "You may take a short break.\n\nPress any key when you are ready to continue."

# Prompt and store info about the experimental session
expInfo = {'Experiment':expName, 'Participant ID':'', 'Participant number':''}
infoDlg = gui.DlgFromDict(dictionary=expInfo, title='Experiment info', 
    fixed=['Experiment'])
if infoDlg.OK == False: core.quit()  # User pressed cancel

# Data file name stem = absolute path + subject number + experiment name
filename = _thisDir + os.sep + 'data/%03d_%s_' %(int(expInfo['Participant number']), expName)
EDFfilename = 'SART%03d.EDF' %(int(expInfo['Participant number']))

# Check whether data files for this participant already exist
if os.path.exists(filename + '_1out.csv'):
    idDlg = gui.Dlg(title='ID bestaat al')
    idDlg.addText('Er zijn al data voor deze participant opgeslagen. Wil je de oude bestanden overschrijven? ')
    idDlg.show()
    if idDlg.OK == False: core.quit()  # User pressed cancel
    

## Run experiment ----------------------------------------------------


# Initiaise clock and escape flag
clock = core.Clock()
endExpNow = False

# Load experiment window
win = visual.Window(size=[1600, 1200], fullscr=True, winType='pyglet', 
    monitor='testMonitor', units='cm')
win.mouseVisible = False

# Make instruction and thought probe stimuli

instructionStim = visual.TextStim(win, text=instruction, 
    height=0.8, color='black', font='Helvetica', wrapWidth=20)
startQuestionStim1 = visual.TextStim(win, text=startQuestion1, 
    height=0.8, color='black', font='Arial', wrapWidth=20)
startQuestionStim2 = visual.TextStim(win, text=startQuestion2, 
    height=0.8, color='black', font='Arial', wrapWidth=20)
instructionStim1 = visual.TextStim(win, text=instruction1, 
    height=0.8, color='black', font='Helvetica', wrapWidth=20)
instructionStim2 = visual.TextStim(win, text=instruction2, 
    height=0.8, color='black', font='Helvetica', wrapWidth=20)
instructionStim3 = visual.TextStim(win, text=instruction3, 
    height=0.8, color='black', font='Helvetica', wrapWidth=20)
instructionStim4 = visual.TextStim(win, text=instruction4, 
    height=0.8, color='black', font='Helvetica', wrapWidth=20)
instructionStim5 = visual.TextStim(win, text=instruction5, 
    height = 0.8, color='black', font='Helvetica', wrapWidth=20)
instructionStim6 = visual.TextStim(win, text=instruction6, 
    height = 0.8, color='black', font='Helvetica', wrapWidth=20)
thoughtProbeStim = visual.TextStim(win, text=probeQuestion, 
    height=0.8, color='black', font='Arial', wrapWidth=20)
stickyStim = visual.TextStim(win, text=stickyQuestion,
    height=0.8, color='black', font='Arial', wrapWidth=20)
temporalStim = visual.TextStim(win, text=temporalQuestion,
    height=0.8, color='black', font='Arial', wrapWidth=20)
valenceStim = visual.TextStim(win, text=valenceQuestion,
    height=0.8, color='black', font='Arial', wrapWidth=20)
breakStim = visual.TextStim(win, text=suggestBreak, 
    height=0.8, color='black', font='Helvetica')

# Initialise eye tracker and do calibration (manually)
#eyeTracker = EyeLink()
#startEyetracker(EDFfilename, win)

instructionStim.draw()
win.flip()
event.waitKeys()

#run initial questions
runStartQuestions(win, filename, startQuestionStim1, startQuestionStim2, EDFfilename, expInfo)


# Present instructions 1-3
instructionStim1.draw()
win.flip()
event.waitKeys()
instructionStim2.draw()
win.flip()
event.waitKeys()
thoughtProbeStim.draw()
win.flip()
event.waitKeys()
stickyStim.draw()
win.flip()
event.waitKeys()
instructionStim3.draw()
win.flip()
event.waitKeys()

# Run practice trials
runPractice(win, pracTrials, clock, answerKey, thoughtProbeStim, 
    stickyStim, temporalStim, valenceStim, instructionStim5, EDFfilename)

# Warn the participant that the experiment is about to start
instructionStim4.draw()
win.flip()
event.waitKeys()
    
# Perform additional calibration and start recording.
#startEyeTrackRec(win, EDFfilename, instructionStim5)

# Run experimental blocks (including breaks)
runBlocks(win, filename, startBlock, blockDur, clock, answerKey, 
    EDFfilename, expInfo, thoughtProbeStim, stickyStim, temporalStim, valenceStim,
    instructionStim5, breakStim)
    
# Tell participant the experiment has finished
instructionStim6.draw()
win.flip()

# End tracking and save data
#closeEyetracker(EDFfilename)

# Wait for keypress and close window
event.waitKeys()
win.close()
