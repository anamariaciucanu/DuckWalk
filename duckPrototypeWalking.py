import maya.cmds as cmds
import math

#Global variables
pi = math.pi
minValue = 0.0
maxValue = 10.0
speed = 1.0

#Timing
animationStart = 0
animationEnd = 120
fps=24
#Ellipse axes
asq = 3.0
bsq = 0.9
extraAmpFactor = 20

widgets = {}
controllers = ['R_IK_CTRL', 'L_IK_CTRL', 'R_Toe_CTRL', 'L_Toe_CTRL', 'Spine_CTRL', 'Spine1_CTRL', 'Spine2_CTRL', 'Spine7_CTRL', 'Duck_Master_CTRL']

def resetParameters():          
    #Reset transformations
    for ctrl in controllers:
        for axis in 'XYZ':
            cmds.setAttr('%s.translate%s' % (ctrl, axis), 0)
            cmds.cutKey( '%s'%ctrl, time=(animationStart,animationEnd), attribute='translate%s'%axis, option='keys' )
            cmds.setAttr('%s.rotate%s' % (ctrl, axis), 0)
            cmds.cutKey( '%s'%ctrl, time=(animationStart,animationEnd), attribute='rotate%s'%axis, option='keys' )
            cmds.setAttr('%s.scale%s' % (ctrl, axis), 1)
            cmds.cutKey( '%s'%ctrl, time=(animationStart,animationEnd), attribute='scale%s'%axis, option='keys' )
            
def generateWalk():
    halfFPS = fps/2
    angleCut = speed * 2*pi/fps
    weightCosValue = math.cos(weight*pi)
    invWeight = 1.0 - weight
    zWalking = 0

    for i in range(animationStart, animationEnd, fps):
        for j in range (0, fps, 3):
            if (i + j < animationEnd):
                teta = (i + j) * angleCut
                
           #Feet   
                rotationAmplitude = amplitude * extraAmpFactor
                currentLeftFootTranslationX = (amplitude / 3.0) * weight * math.fabs(math.sin(0.5 * teta))
                currentRightFootTranslationX = currentLeftFootTranslationX - amplitude                
                currentFootTranslationY = -amplitude * math.sin(teta) / asq
                currentFootTranslationZ = amplitude * math.cos(teta) / bsq
                currentLeftFootRotationX = -rotationAmplitude * math.sin(teta) / 2.0
                if (currentFootTranslationY < 0):
                    currentFootTranslationY = 0
                if (currentLeftFootRotationX < 0):
                    currentLeftFootRotationX = 0  
                    
                currentLeftToeTranslationY = -currentFootTranslationY / asq
                currentLeftFootTranslationZ = currentLeftToeTranslationY / asq                           
             
            #Spine    
                currentSpineTranslationX = currentLeftFootTranslationX - amplitude / 2.0                
                currentSpineTranslationY = (weightCosValue / 2.0) + invWeight * math.sin(2 * teta) / asq 
                currentSpineRotationY = -weight * rotationAmplitude * math.cos(teta)
                currentSpineRotationZ = currentSpineRotationY / 3.0
                currentTailRotationY = currentSpineRotationY / 2.0
                
            #Neck
                currentNeckTranslationY = -currentSpineTranslationY / 2.0
                currentNeckRotationY = -currentSpineRotationY 
                currentNeckTranslationX = currentNeckRotationY / (extraAmpFactor * 2)
               # currentSpine1RotationZ = currentNeckRotationY / 3.0
                
            #Master control
                zWalking = zWalking + speed * amplitude / asq
                xWalking = amplitude * direction * math.sin(teta)
                yWalkingRotation = rotationAmplitude * xWalking
                
            #Frame number
                tLeft = i + j
                tRight = (i + j + halfFPS) % animationEnd        
    
            #Left side
                cmds.setAttr('L_IK_CTRL.translateX', currentLeftFootTranslationX)
                cmds.setKeyframe( 'L_IK_CTRL', attribute='translateX', t=tLeft )           
                cmds.setAttr('L_IK_CTRL.translateY', currentFootTranslationY)
                cmds.setKeyframe( 'L_IK_CTRL', attribute='translateY', t=tLeft )
                cmds.setAttr('L_IK_CTRL.translateZ', currentFootTranslationZ)
                cmds.setKeyframe( 'L_IK_CTRL', attribute='translateZ', t=tLeft )   
                cmds.setAttr('L_IK_CTRL.rotateX', currentLeftFootRotationX)
                cmds.setKeyframe( 'L_IK_CTRL', attribute='rotateX', t=tLeft ) 
                cmds.setAttr('L_Toe_CTRL.translateY', currentLeftToeTranslationY)
                cmds.setKeyframe( 'L_Toe_CTRL', attribute='translateY', t=tLeft ) 
                cmds.setAttr('L_Toe_CTRL.translateZ', currentLeftFootTranslationZ)
                cmds.setKeyframe( 'L_Toe_CTRL', attribute='translateZ', t=tLeft ) 
                
            #Right side    
                cmds.setAttr('R_IK_CTRL.translateX', currentRightFootTranslationX)
                cmds.setKeyframe( 'R_IK_CTRL', attribute='translateX', t=tLeft )
                cmds.setAttr('R_IK_CTRL.translateY', currentFootTranslationY)
                cmds.setKeyframe( 'R_IK_CTRL', attribute='translateY', t=tRight )
                cmds.setAttr('R_IK_CTRL.translateZ', currentFootTranslationZ)
                cmds.setKeyframe( 'R_IK_CTRL', attribute='translateZ', t=tRight )  
                cmds.setAttr('R_IK_CTRL.rotateX', currentLeftFootRotationX)
                cmds.setKeyframe( 'R_IK_CTRL', attribute='rotateX', t=tRight ) 
                cmds.setAttr('R_Toe_CTRL.translateY', currentLeftToeTranslationY)
                cmds.setKeyframe( 'R_Toe_CTRL', attribute='translateY', t=tRight ) 
                cmds.setAttr('R_Toe_CTRL.translateZ', currentLeftFootTranslationZ)
                cmds.setKeyframe( 'R_Toe_CTRL', attribute='translateZ', t=tRight ) 
                
            #Spine
                cmds.setAttr('Spine_CTRL.translateX', currentSpineTranslationX)
                cmds.setKeyframe( 'Spine_CTRL', attribute='translateX', t=tLeft) 
                cmds.setAttr('Spine_CTRL.translateY', currentSpineTranslationY)
                cmds.setKeyframe( 'Spine_CTRL', attribute='translateY', t=tLeft) 
                cmds.setAttr('Spine_CTRL.rotateY',  currentSpineRotationY)
                cmds.setKeyframe( 'Spine_CTRL', attribute='rotateY', t=tLeft) 
                cmds.setAttr('Spine_CTRL.rotateZ',  currentSpineRotationZ)
                cmds.setKeyframe( 'Spine_CTRL', attribute='rotateZ', t=tLeft)                 
                cmds.setAttr('Spine7_CTRL.rotateY',  currentTailRotationY)
                cmds.setKeyframe( 'Spine7_CTRL', attribute='rotateY', t=tLeft) 
                
            #Neck
                cmds.setAttr('Spine2_CTRL.translateX',  currentNeckTranslationX)
                cmds.setKeyframe( 'Spine2_CTRL', attribute='translateX', t=tLeft) 
                cmds.setAttr('Spine2_CTRL.translateY',  currentNeckTranslationY)
                cmds.setKeyframe( 'Spine2_CTRL', attribute='translateY', t=tLeft) 
                cmds.setAttr('Spine2_CTRL.rotateY',  currentNeckRotationY)
                cmds.setKeyframe( 'Spine2_CTRL', attribute='rotateY', t=tLeft) 
               # cmds.setAttr('Spine1_CTRL.rotateZ',  currentSpine1RotationZ)
               # cmds.setKeyframe( 'Spine1_CTRL', attribute='rotateZ', t=tLeft)
                
            #Forward walking
                cmds.setAttr('Duck_Master_CTRL.translateZ', zWalking)
                cmds.setKeyframe( 'Duck_Master_CTRL', attribute='translateZ', t=tLeft)       
                cmds.setAttr('Duck_Master_CTRL.translateX',  xWalking)
                cmds.setKeyframe( 'Duck_Master_CTRL', attribute='translateX', t=tLeft)      
                cmds.setAttr('Duck_Master_CTRL.rotateY',  yWalkingRotation)
                cmds.setKeyframe( 'Duck_Master_CTRL', attribute='rotateY', t=tLeft)      
                
            else:
                break
 
def getGUIValues():
    #Get values
    #Timing----
    tempAnimationStartFrame =  cmds.intFieldGrp(widgets['startFrame'], q = True, v = True)
    tempAnimationEndFrame = cmds.intFieldGrp(widgets['endFrame'], q = True, v = True)
    tempFPS = cmds.intFieldGrp(widgets['FPS'], q = True, v = True)
    
    #Sliders----
    global amplitude
    amplitude = cmds.floatSliderGrp(widgets['amplitude'], q = True, v = True)
    global speed
    speed = cmds.floatSliderGrp(widgets['speed'], q = True, v = True)
    global weight
    weight = cmds.floatSliderGrp(widgets['weight'], q = True, v = True)
    global direction
    direction = cmds.floatSliderGrp(widgets['direction'], q = True, v = True)
    
    #Check timing values
    if (tempAnimationStartFrame[0] > 0 and tempAnimationStartFrame[0] <= tempAnimationEndFrame[0]):
        global animationStart
        animationStart = tempAnimationStartFrame[0]
    if (tempAnimationEndFrame[0] > animationStart):
        global animationEnd
        animationEnd = tempAnimationEndFrame[0]
    if (tempFPS[0] > 1 and tempFPS[0] <= 60):
        global fps
        fps = tempFPS[0] 
         
    #Normalize values
    normalizeGUIValues()
 
def normalizeGUIValues():
    minMaxDiff1 = maxValue - minValue
    minMaxDiff2 = minMaxDiff1/2.0
    global amplitude
    amplitude = (amplitude - minValue)/minMaxDiff2
    global speed        
    speed = (speed - minValue)/minMaxDiff2

    global asq
    global weight  
    if (weight < maxValue/4):
        asq = 1
    elif (weight < 3*maxValue/4):
        asq=2
    elif (weight < maxValue):
        asq=3        
     
    weight = (weight - minValue)/minMaxDiff1   
    global direction
    direction = (direction - minValue)/minMaxDiff1
     
    
                      
def generateBehaviour():
    getGUIValues()        
    generateWalk()   

def createGUI():
    #Create window
    windowID = 'LeQuackWalker' 
    if (cmds.window(windowID, exists=True)):
        cmds.deleteUI(windowID, window=True)    
   
    widgets['window'] = cmds.window(windowID, title = "Le Quack Walker v1.0", width = 350, height = 400)
    
    #Create layout
    widgets['winLayout'] = cmds.columnLayout(adj=False, rowSpacing = 10)
    
    #Padding
    cmds.separator(height = 20)
    
   #Create general parameters
    widgets['startFrame'] = cmds.intFieldGrp( numberOfFields=1, label='Animation Start Frame ', value1 = animationStart)
    widgets['endFrame'] = cmds.intFieldGrp( numberOfFields=1, label='Animation End Frame ', value1 = animationEnd)
    widgets['FPS'] = cmds.intFieldGrp( numberOfFields=1, label='Frames per Seconds ', value1 = fps)
    
    cmds.separator(height = 20)
    defaultValue = maxValue/2   
    widgets['amplitude'] = cmds.floatSliderGrp( label = 'Amplitude', min = minValue, max = maxValue, value = defaultValue, field=True )
    widgets['speed'] = cmds.floatSliderGrp( label='Speed ', min = minValue, max = maxValue, value = defaultValue, field=True )
    widgets['weight'] = cmds.floatSliderGrp( label='Weight ', min = minValue, max = maxValue, value = defaultValue, field=True )
    widgets['direction'] = cmds.floatSliderGrp( label='Direction ', min = minValue, max = maxValue, value = 0, field=True )
    
    cmds.separator(height = 20)
    
    #Create reset and generate button
    widgets['mainButtonsLayout'] = cmds.rowLayout('Main Buttons', parent = widgets['winLayout'], numberOfColumns=2)  
    widgets['resetButton'] = cmds.button( label='Reset', c = 'resetParameters()', h = 50, w = 200, align = 'left')
    widgets['generateButton'] = cmds.button( label='Generate', c = 'generateBehaviour()', h = 50, w = 200, align = 'right')
    
    #Show GUI 
    cmds.showWindow(widgets['window'])
    
createGUI()    
