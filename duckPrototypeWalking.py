import maya.cmds as cmds
import math

#TO DO: Rotation of 
#Global variables
pi = math.pi
minValue = 0.1
maxValue = 5
animationStart = 0
animationEnd = 120
fps=24
amplitude = 1.0
rotationAmplitude = 10.0
speed = 1.0
weight = 0.1
direction = 1.0
#Ellipse axes
asq = 3.0
bsq = 1

widgets = {}
controllers = ['R_IK_CTRL', 'L_IK_CTRL', 'R_Toe_CTRL', 'L_Toe_CTRL', 'Spine_CTRL']

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
    angleCut = 2*pi/fps
    for i in range(animationStart, animationEnd, fps):
        for j in range (0, fps, 3):
            if (i + j < animationEnd):
                teta = (i + j) * angleCut
                
           #Feet   
                currentFootTranslationX = weight * math.cos(speed * teta)                        
                currentFootTranslationY = amplitude * math.sin(speed * teta) / asq
                currentFootTranslationZ = -amplitude * math.cos(speed * teta) / bsq
                if (currentFootTranslationY < 0):
                    currentFootTranslationY = 0
             
            #Spine    
                currentSpineTranslationX = currentFootTranslationX 
                currentSpineTranslationY = -amplitude * math.sin(2 * speed * teta) / asq
                currentSpineRotationY = rotationAmplitude * math.cos(speed * teta)
                currentSpineRotationZ = currentSpineRotationY / 3.0
                
            #Frame number
                tLeft = i + j
                tRight = (i + j + halfFPS) % animationEnd        
    
            #Left side
                cmds.setAttr('L_IK_CTRL.translateX', currentFootTranslationX)
                cmds.setKeyframe( 'L_IK_CTRL', attribute='translateX', t=tLeft )           
                cmds.setAttr('L_IK_CTRL.translateY', currentFootTranslationY)
                cmds.setKeyframe( 'L_IK_CTRL', attribute='translateY', t=tLeft )
                cmds.setAttr('L_IK_CTRL.translateZ', currentFootTranslationZ)
                cmds.setKeyframe( 'L_IK_CTRL', attribute='translateZ', t=tLeft )   
                
            #Right side    
                cmds.setAttr('R_IK_CTRL.translateX', -currentFootTranslationX)
                cmds.setKeyframe( 'R_IK_CTRL', attribute='translateX', t=tRight )
                cmds.setAttr('R_IK_CTRL.translateY', currentFootTranslationY)
                cmds.setKeyframe( 'R_IK_CTRL', attribute='translateY', t=tRight )
                cmds.setAttr('R_IK_CTRL.translateZ', currentFootTranslationZ)
                cmds.setKeyframe( 'R_IK_CTRL', attribute='translateZ', t=tRight )   
                
            #Spine
                cmds.setAttr('Spine_CTRL.translateX', currentSpineTranslationX)
                cmds.setKeyframe( 'Spine_CTRL', attribute='translateX', t=tLeft) 
                cmds.setAttr('Spine_CTRL.translateY', currentSpineTranslationY)
                cmds.setKeyframe( 'Spine_CTRL', attribute='translateY', t=tLeft) 
                cmds.setAttr('Spine_CTRL.rotateY',  currentSpineRotationY)
                cmds.setKeyframe( 'Spine_CTRL', attribute='rotateY', t=tLeft) 
                cmds.setAttr('Spine_CTRL.rotateZ',  currentSpineRotationZ)
                cmds.setKeyframe( 'Spine_CTRL', attribute='rotateZ', t=tLeft) 
                
            else:
                break
            
def generateBehaviour():
    #Get values
    tempAnimationStartFrame =  cmds.intFieldGrp(widgets['startFrame'], q = True, v = True)
    tempAnimationEndFrame = cmds.intFieldGrp(widgets['endFrame'], q = True, v = True)
    tempFPS = cmds.intFieldGrp(widgets['FPS'], q = True, v = True)
    tempAmplitude=  cmds.floatFieldGrp(widgets['amplitude'], q = True, v = True)
    tempSpeed = cmds.floatFieldGrp(widgets['speed'], q = True, v = True)
    tempWeight = cmds.floatFieldGrp(widgets['weight'], q = True, v = True)
    tempDirection = cmds.floatFieldGrp(widgets['direction'], q = True, v = True)
    
    #Check values
    if (tempAnimationStartFrame[0] > 0 and tempAnimationStartFrame <= tempAnimationEndFrame[0]):
        global animationStart
        animationStart = tempAnimationStartFrame[0]
    if (tempAnimationEndFrame[0] > animationStart):
        global animationEnd
        animationEnd = tempAnimationEndFrame[0]
    if (tempFPS[0] > 1 and tempFPS[0] <= 60):
        global fps
        fps = tempFPS[0]        
    if (tempAmplitude[0] >= minValue and tempAmplitude[0] <= maxValue):
        global amplitude
        amplitude = tempAmplitude[0]
    if (tempSpeed[0] >= minValue and tempSpeed[0] <= maxValue):
        global speed
        speed = tempSpeed[0]        
    if (tempWeight[0] >= minValue and tempWeight[0] <= maxValue):
        global weight
        weight = tempWeight[0]
    if (tempDirection[0] >= minValue and tempDirection[0] <= maxValue):
        global direction
        direction = tempDirection[0]     
        
    generateWalk()   

def createGUI():
    #Create window
    windowID = 'LeQuackWalker' 
    if (cmds.window(windowID, exists=True)):
        cmds.deleteUI(windowID, window=True)    
   
    widgets['window'] = cmds.window(windowID, title = "Le Quack Walker v1.0", width = 300, height = 400)
    
    #Create layout
    widgets['winLayout'] = cmds.columnLayout(adj=False, rowSpacing = 10)
    
    #Padding
    cmds.separator(height = 20)
    
   #Create general parameters
    widgets['startFrame'] = cmds.intFieldGrp( numberOfFields=1, label='Animation Start Frame ')
    widgets['endFrame'] = cmds.intFieldGrp( numberOfFields=1, label='Animation End Frame ')
    widgets['FPS'] = cmds.intFieldGrp( numberOfFields=1, label='Frames per Seconds ')
    
    cmds.separator(height = 20)
    cmds.text('        Min - Max values are 0.1 - 5')
    
    widgets['amplitude'] = cmds.floatFieldGrp( numberOfFields=1, label='Amplitude ')
    widgets['speed'] = cmds.floatFieldGrp( numberOfFields=1, label='Speed ')
    widgets['weight'] = cmds.floatFieldGrp( numberOfFields=1, label='Weight ')
    widgets['direction'] = cmds.floatFieldGrp( numberOfFields=1, label='Direction ')
    
    cmds.separator(height = 20)
    
    #Create reset and generate button
    widgets['mainButtonsLayout'] = cmds.rowLayout('Main Buttons', parent = widgets['winLayout'], numberOfColumns=2)  
    widgets['resetButton'] = cmds.button( label='Reset', c = 'resetParameters()', h = 50, w = 200, align = 'left')
    widgets['generateButton'] = cmds.button( label='Generate', c = 'generateBehaviour()', h = 50, w = 200, align = 'right')
    
    #Show GUI 
    cmds.showWindow(widgets['window'])
    
createGUI()
    