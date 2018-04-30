
from psychopy import core, visual, event, logging, gui, data
from pylink import *
import gc  # Garbage collection control
import glob, random, time, codecs, pyglet
import pandas as pd
import csv
import os  # Handy system and path functions



### Experiment functions -------------------------------------------------------


def presentBlank (win):
    ## Presents the intertrial interval.
    ## Fixation cross can be removed by setting the lineColor to 'grey'.
    
    blank = visual.ShapeStim(win, 
        vertices=((0, -0.3), (0, 0.3), (0, 0), (-0.3, 0), (0.3, 0)),
        lineWidth=2,
        closeShape=False,
        lineColor='black')
    #win.callOnFlip(getEYELINK().sendMessage, "ITI_ON")
    blank.draw()
    win.flip()
    waitTime = 0.001*random.randint(1500, 2100)
    core.wait(waitTime)
    

def presentStimuli(win, aStimulus, clock, answerKey, EDFfilename):
    ## Presents a SART word stimulus and returns the response. 
    ## Does not present thought probes.
    
    word = visual.TextStim(win, 
        text=str(aStimulus), 
        color='Black', 
        font='Arial', height=1.0)
    mask = visual.TextStim(win, 
        text="XXXXXXXXXXXXXXXXXXXX", 
        color='Black', 
        font='Arial', 
        height=0.8)
    blank = visual.ShapeStim(win, 
        vertices=((0, -0.3), (0, 0.3), (0, 0), (-0.3, 0), (0.3, 0)),
        lineWidth=2,
        closeShape=False,
        lineColor='black')
    
    # Present the stimulus for 300 ms and register responses
    stimTime = 0
    c = []
    
    #win.callOnFlip(getEYELINK().sendMessage, "STIM_ON")
    win.callOnFlip(clock.reset)
    word.draw()
    event.clearEvents()
    win.flip()
    
    core.wait(secs=0.3, hogCPUperiod=0.3)
    c = event.getKeys(keyList=answerKey, timeStamped=clock)
    
    if event.getKeys(keyList=["escape"]):
        #closeEyetracker(EDFfilename)
        core.quit()
    
    if c:
        #getEYELINK().sendMessage("SART_RESPONSE")
        return c[0]
    
    # Present the mask for 300 ms or until response
    #win.callOnFlip(getEYELINK().sendMessage, "MASK_ON")
    mask.draw()
    win.flip()
    
    while stimTime < 0.6:
        c = event.getKeys(keyList=answerKey, timeStamped=clock)
        
        if event.getKeys(keyList=["escape"]):
            #closeEyetracker(EDFfilename)
            core.quit()
        
        if c:
            #getEYELINK().sendMessage("SART_RESPONSE")
            return c[0]
        
        stimTime = clock.getTime()
    
    mask.setText("")
    win.flip()
    
    # Present the response window for 3000 ms or until response
    #win.callOnFlip(getEYELINK().sendMessage, "RESPONSE_INTERVAL_ON")
    blank.draw()
    win.flip()
    
    while stimTime < 3.6:
        c = event.getKeys(keyList=answerKey, timeStamped=clock)
        
        if event.getKeys(keyList=["escape"]):
            #closeEyetracker(EDFfilename)
            core.quit()
        
        if c:
            #getEYELINK().sendMessage("SART_RESPONSE")
            return c[0]
        
        stimTime = clock.getTime()
    
    #getEYELINK().sendMessage("NO_SART_RESPONSE")
    return ['0','NA']
  
def presentStartQuestion1(win, startQuestionStim1, EDFfilename):
    ## Presents a first start question 
    
    questionScale1 = visual.RatingScale(win, choices=['1', '2', '3', '4'])
    item = startQuestionStim1
    while questionScale1.noResponse:
        item.draw()
        questionScale1.draw()
        win.flip()
        if event.getKeys(['escape']):
                core.quit()
    rating1 = questionScale1.getRating()
    decisionTime = questionScale1.getRT()
    choiceHistory = questionScale1.getHistory()
    
    if event.getKeys(keyList=["escape"]):
        #closeEyetracker(EDFfilename)
        core.quit()
    
    if rating1:
        return rating1[0]
    else:
        #getEYELINK().sendMessage("NO_TP_RESPONSE")
        return ''
        
def presentStartQuestion2(win, startQuestionStim2, EDFfilename):
    ## Presents a second start question.
    
    questionScale2 = visual.RatingScale(win, choices=['1', '2', '3', '4'])
    item = startQuestionStim2
    while questionScale2.noResponse:
        item.draw()
        questionScale2.draw()
        win.flip()
        if event.getKeys(['escape']):
                core.quit()
    rating2 = questionScale2.getRating()
    decisionTime = questionScale2.getRT()
    choiceHistory = questionScale2.getHistory()
    
    if event.getKeys(keyList=["escape"]):
        #closeEyetracker(EDFfilename)
        core.quit()
    
    if rating2:
        return rating2[0]
    else:
        #getEYELINK().sendMessage("NO_TP_RESPONSE")
        return ''


def presentProbe(win, thoughtProbeStim, EDFfilename):
    ## Presents a regular thought probe.
    
    #win.callOnFlip(getEYELINK().sendMessage, "TP_ON")
    thoughtProbeStim.draw()
    win.flip()
    event.getKeys()
    probeResponse = event.waitKeys(keyList=["1","2","3","4","5","6"])
    #getEYELINK().sendMessage("TP_RESPONSE %s" %(probeResponse[0]))
    
    if event.getKeys(keyList=["escape"]):
        #closeEyetracker(EDFfilename)
        core.quit()
    
    if probeResponse:
        return probeResponse[0]
    else:
        #getEYELINK().sendMessage("NO_TP_RESPONSE")
        return ''
    

def presentStickyProbe(win, stickyStim, EDFfilename):
    ## Presents the stickiness question.
    
    #win.callOnFlip(getEYELINK().sendMessage, "STICKY_ON")
    stickyStim.draw()
    win.flip()
    event.getKeys()
    stickyResponse = event.waitKeys(keyList=["1","2","3","4","5"])
    #getEYELINK().sendMessage("STICKY_RESPONSE %s" %(stickyResponse[0]))
    
    if event.getKeys(keyList=["escape"]):
        #closeEyetracker(EDFfilename)
        core.quit()
        
    if stickyResponse:
        return stickyResponse[0]
    else:
        #getEYELINK().sendMessage("NO_STICKY_RESPONSE")
        return ''
    
def presentTemporalProbe(win, temporalStim, EDFfilename):
    ## Presents the temporal question.
    
    #win.callOnFlip(getEYELINK().sendMessage, "STICKY_ON")
    temporalStim.draw()
    win.flip()
    event.getKeys()
    temporalResponse = event.waitKeys(keyList=["1","2","3"])
    #getEYELINK().sendMessage("STICKY_RESPONSE %s" %(stickyResponse[0]))
    
    if event.getKeys(keyList=["escape"]):
        #closeEyetracker(EDFfilename)
        core.quit()
        
    if temporalResponse:
        return temporalResponse[0]
    else:
        #getEYELINK().sendMessage("NO_STICKY_RESPONSE")
        return ''

def presentValenceProbe(win, valenceStim, EDFfilename):
    ## Presents the valence question.
    
    #win.callOnFlip(getEYELINK().sendMessage, "STICKY_ON")
    valenceStim.draw()
    win.flip()
    event.getKeys()
    
    valenceScale = visual.RatingScale(win, low = 1, high = 100, tickMarks= [1, 25, 50, 75, 100], labels = ['--', '-', 'neutral', '+', '++'], showValue = False, acceptPreText ='click line', acceptText = 'Continue')
    valenceRating = []
    item = valenceStim
    while valenceScale.noResponse:
        item.draw()
        valenceScale.draw()
        win.flip()
        if event.getKeys(['escape']):
                core.quit()
    valenceRating.append(valenceScale.getRating())
    valenceRT = valenceScale.getRT()
    vlaenceChoiceHistory = valenceScale.getHistory()
    
    #getEYELINK().sendMessage("STICKY_RESPONSE %s" %(stickyResponse[0]))
    
    if event.getKeys(keyList=["escape"]):
        #closeEyetracker(EDFfilename)
        core.quit()
        
    if valenceRating:
        return valenceRating[0]
    else:
        #getEYELINK().sendMessage("NO_STICKY_RESPONSE")
        return ''
        
        
       


def presentBreak(win, EDFfilename, breakStim, instructionStim5):
    ## Presents the 'suggestBreak' text until response and starts manual calibration 
    ## to correct for the participant leaving the chinrest.
    
    #win.callOnFlip(getEYELINK().sendMessage, "BREAK_START")
    breakStim.draw()
    win.flip()
    
    #stopEyeTrackRec()
    
    # Wait for button press to continue
    event.waitKeys()
    #getEYELINK().sendMessage("BREAK_END")
    
    #startEyeTrackRec(win, EDFfilename, instructionStim5)
    

def runStartQuestions(win, filename, startQuestionStim1, startQuestionStim2, EDFfilename, expInfo):
    
    rating1 = presentStartQuestion1(win, startQuestionStim1, EDFfilename)
    win.flip()
    rating2 = presentStartQuestion2(win, startQuestionStim2, EDFfilename)
    win.flip()
   
    outputFile = open(filename + '_' + 'out' + 'initquestions' + '.csv', 'w')
    outputFile.write("expName, 'EDFfile', date, subjID, subjNum, rating1, rating2")
    outputFile.write("\n")
    outputFile.write("{},{},{},{},{},{},{}\n".format(
        expInfo['Experiment'], 
        EDFfilename,
        data.getDateStr(), 
        expInfo['Participant ID'],
        expInfo['Participant number'],
        rating1[0],
        rating2[0]))
            
    
def runStartQuestion2(win, startQuestion2, startQuestionStim2, EDFfilename):
    presentStartQuestion1(win, startQuestion2, startQuestionStim2, EDFfilename)
    win.flip()

def runPractice(win, pracTrials, clock, answerKey, thoughtProbeStim, stickyStim, temporalStim, valenceStim, instructionStim5, EDFfilename):
    ## Runs 'pracTrials' practice trials,  including a thought probe. 
    ## Does not record any behavioural or eye-tracking data.
    
    # Load practice file
    pracFile = pd.read_csv('Prac.csv', delimiter = ';')
    pracStimuli = pracFile['stimuli']
    pracTrial = pracFile['trialType']
    
    # Run pactice trials
    for i in range (pracTrials):
        if pracTrial[i]== 1:
            toPresent = pracStimuli[i]
            presentBlank(win)
            presentStimuli(win, toPresent, clock, answerKey, EDFfilename)
        else:
            presentProbe(win, thoughtProbeStim, EDFfilename)
            presentStickyProbe(win, stickyStim, EDFfilename)
            presentTemporalProbe(win, temporalStim, EDFfilename)
            presentValenceProbe(win, valenceStim, EDFfilename)
            instructionStim5.draw()
            win.flip()
            event.waitKeys()
    

def runBlocks(win, filename, startBlock, blockDur, clock, answerKey, EDFfilename, expInfo, thoughtProbeStim, stickyStim, temporalStim, valenceStim, instructionStim5, breakStim):
    ## Runs 'blockDur' number of trials of each block, including thought probes,  
    ## starting at 'startBlock'. Breaks are presented every other block.
    
    trialNo = 0
    for i in range (startBlock, 9):
        expFile = pd.read_csv('Block_' + str(i) + '_Ned.csv', delimiter = ';')
        stimuli = expFile['stimuli']
        trialType = expFile['trialType']  # 0 = Practice, 1 = Go, 2 = NoGo, 3 = OwnConcern, 
        blockNum = expFile['blockNum']    # 4 = OtherConcern, 5 = ThoughtProbe
        outputFile = open(filename + '_' + str(i) + 'out' + '.csv', 'w')
        outputFile.write("expName, 'EDFfile', date, subjID, subjNum, blockNum, trialNo, trialType, goResp, RT, tpResp, tpRT, stickyResp, stickyRT, temporalResp, temporalRT, valenceResp, valenceRT")
        outputFile.write("\n")
        
        # Suggest a break after 2, 4 and 6 blocks:
        if blockNum[i] in [3, 5, 7]:
            presentBreak(win, EDFfilename, breakStim, instructionStim5)
        
        # Run trials
        for m in range (blockDur):
            trialNo = trialNo + 1
            
            # Send trial info to tracker
            #getEYELINK().sendCommand("record_status_message 'Trial %d %s'"%(trialNo, trialType[m]))
            #getEYELINK().sendMessage("TRIAL_ID %d %s"%(trialNo, trialType[m]))
            
            # Normal trial
            if  trialType[m]!= 5:
                presentBlank(win)
                trialResp = presentStimuli(win, stimuli[m], clock, answerKey, EDFfilename)
                
                
                # Write results to data file
                outputFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{}, {}, {}, {}, {}\n".format(
                    expInfo['Experiment'], 
                    EDFfilename,
                    data.getDateStr(), 
                    expInfo['Participant ID'],
                    expInfo['Participant number'],
                    blockNum[m], 
                    trialNo, 
                    trialType[m], 
                    trialResp[0], 
                    trialResp[1],
                    "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA"))
            
            # Thought probe
            else:
                presTime = time.time()
                probeResp = presentProbe(win, thoughtProbeStim, EDFfilename)
                respTime = time.time()
                probeRT = float(respTime - presTime) 
                stickyResp = presentStickyProbe(win, stickyStim, EDFfilename)
                respTimeSticky = time.time()
                stickyRT = float(respTimeSticky - presTime)
                temporalResp = presentTemporalProbe(win, temporalStim, EDFfilename)
                respTimeTemporal = time.time()
                temporalRT = float(respTimeTemporal - presTime)
                valenceResp = presentValenceProbe(win, valenceStim, EDFfilename)
                respTimeValence = time.time()
                valenceRT = float(respTimeValence - presTime)
                
                # Write results to data file
                outputFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{}, {}, {}, {}, {}\n".format(
                    expInfo['Experiment'], 
                    EDFfilename,
                    data.getDateStr(), 
                    expInfo['Participant ID'], 
                    expInfo['Participant number'],
                    blockNum[m], 
                    trialNo, 
                    trialType[m], 
                    "NA", "NA", 
                    probeResp, 
                    probeRT, 
                    stickyResp, 
                    stickyRT,
                    temporalResp,
                    temporalRT,
                    valenceResp,
                    valenceRT))
                # After a thought probe, press any key to continue.
                #win.callOnFlip(getEYELINK().sendMessage, "INSTRUCTION5_ON")
                instructionStim5.draw()
                win.flip()
                c = event.waitKeys()
                #getEYELINK().sendMessage("INSTRUCTION5_RESPONSE")
                
            # Mark end of trial
            #getEYELINK().sendMessage("TRIAL_OK")
            
        outputFile.close()
    


### Eye tracker functions ----------------------------------------------------------------


#def calibrate(win):
#    ## Opens the 'Camera Setup' menu on the eye tracker for manual calibration
#    ## Continues when 'Exit Setup' is clicked or escape is pressed on the eye tracker.
#    
#    getEYELINK().sendMessage("START_CALIBRATION")
#    
#    # Minimise window
#    win.winHandle.minimize()
#    win.fullscr = False
#    win.flip() # redraw the (minimised) window
#    
#    # Do the calibration 
#    openGraphics((1600,1200), 32)
#    setCalibrationColors((int(0), int(0), int(0)), (int(127.5), int(127.5), int(127.5)))
#    setTargetSize(int(1600/70), int(1200/300))
#    getEYELINK().doTrackerSetup()
#    closeGraphics()
#    
#    # Maximise window
#    win.winHandle.maximize()
#    win.fullscr = True 
#    win.winHandle.activate()
#    win.flip()
#    win.mouseVisible = False
#    
#    getEYELINK().sendMessage("END_CALIBRATION")
#    
#
#def startEyetracker(EDFfilename, win):
#    ## Opens EDF file and configures eye tracker
#    
#    # Create EDF filename (max 8 characters) and open it
#    getEYELINK().openDataFile(EDFfilename)
#    pylink.flushGetkeyQueue()
#    getEYELINK().setOfflineMode()
#    
#    # Eyetracker configurations
#    getEYELINK().sendCommand("screen_pixel_coords =  0 1200 1600 0")
#    getEYELINK().sendMessage("DISPLAY_COORDS  0 1200 1600 0")
#    getEYELINK().sendCommand("recording_parse_type = GAZE")  # Gaze direction recorded as screen coordinates
#    getEYELINK().sendCommand("pupil_size_diameter = YES")  # Pupil size recorded as diameter
#    getEYELINK().sendCommand("saccade_velocity_threshold = 30")
#    getEYELINK().sendCommand("saccade_acceleration_threshold = 8000")
#    getEYELINK().sendCommand("saccade_motion_threshold = 0.1")
#    getEYELINK().sendCommand("saccade_pursuit_fixup = 60")
#    getEYELINK().sendCommand("fixation_update_interval = 0")
#    
#    # Do the calibration (manually)
#    calibrate(win)
#    
#
#def startEyeTrackRec(win, EDFfilename, instructionStim5):
#    ## Performs calibration and starts the recording.
#    
#    # Start recording or throw error
#    error = getEYELINK().startRecording(1, 1, 1, 1)  # 0 if succesfull, takes 10-30 ms to begin
#    if error:
#        print ("ERROR: Could not start recording")
#        closeEyetracker(EDFfilename)
#        core.quit()
#    getEYELINK().sendMessage("REC_START")
#    
#    # Start realtime
#    gc.disable()
#    pylink.beginRealTimeMode(200)
#    getEYELINK().sendMessage("REALTIME_START")
#    
#    # After calibration, press any button to continue
#    instructionStim5.draw()
#    win.flip()
#    event.waitKeys()
#    
#
#def stopEyeTrackRec():
#    
#    # End real time
#    getEYELINK().sendMessage("REALTIME_END")
#    pylink.endRealTimeMode()
#    gc.enable()
#    
#    # Stop recording
#    getEYELINK().sendMessage("REC_STOP")
#    pylink.pumpDelay(100)
#    getEYELINK().stopRecording()
#    
#
#def closeEyetracker(EDFfilename):
#    ## Stops the recording and closes eye tracker properly.
#    
#    # End real time
#    getEYELINK().sendMessage("REALTIME_END")
#    pylink.endRealTimeMode()
#    gc.enable()
#    
#    # Stop recording
#    getEYELINK().sendMessage("REC_STOP")
#    pylink.pumpDelay(100)
#    getEYELINK().stopRecording()
#    
#    # Set eye tracker to idle
#    getEYELINK().setOfflineMode()
#    msecDelay(600)  # Delay of 600 ms for eye tracker to finish its job
#    
#    # Close EDF file and copy it to experiment folder
#    getEYELINK().closeDataFile()
#    getEYELINK().receiveDataFile(EDFfilename, EDFfilename)
#    
#    # Close link with eye tracker
#    getEYELINK().close()
