from visual import *
import numpy as np
import wx
import scipy as sp
from scipy.integrate import odeint
#import matplotlib.pyplot as plt

#For defining the axis rotation on the inner ring from the point frame.
def perpendicular_vector(v):
    if (v.x == 0) and (v.y == 0):
        if (v.z == 0):
            raise ValueError('zero vector')
        return (0, 1, 0)
    return (-v.y, v.x, 0)


def solvr(z, t):
    #little_sphere.pos = coordsToSphere(float(np.random.sample()), float(np.random.sample()))
    alpha, alphadot = z
    return [alphadot, (I1*omega*(phidot - omega*sin(float(lat.GetValue()) * pi / 180 + pi/2)*cos(alpha))*sin((float(lat.GetValue()) * pi / 180 + pi/2))*sin(alpha) +
	1/2 * I2 *omega*omega * (sin((float(lat.GetValue()) * pi / 180 + pi/2)))*(sin((float(lat.GetValue()) * pi / 180) + pi/2))*sin(2*alpha))/I2 - alphadot*dampeningConstant]



def coordsToSphere(latitude,longitude):
    r = EARTH_RADIUS
    phi = latitude*pi/180
    theta = longitude*pi/180
    x = r *np.cos(phi) *np.sin(theta);
    y = r *np.sin(phi);
    z = r * np.cos(phi) * np.cos(theta)
    spherical = (x,y,z)
    return spherical

def OnEnterPressed(event):
    should_break = true
    little_sphere.pos = coordsToSphere(float(lat.GetValue()),float(lon.GetValue()))
    v1 = vector(0,1,0)
    v2 = little_sphere.pos
    v3 = cross(v2,v1)
    v4 = rotate(v2, angle = pi/2, axis = v3)
    little_sphere.axis = v4
    OGvector[0] = v4[0]; 
    OGvector[1] = v4[1]; 
    OGvector[2] = v4[2] 

    little_sphere.length = 0.12
    sol[:] = (RunSimulation())
    return

def RunSimulation():

    # Initial conditions on y, y' at x=0
    init = pi/2, 0.0
    # First integrate from 0 to 2
    x = np.linspace(0,5,20000)
    # Then integrate from 0 to -2
    x = np.linspace(0,5,20000)
    return odeint(solvr, init, x)


def SetRate(evt): # called on slider events
    value = s1.GetValue()
    global Loops_per_second
    Loops_per_second = value
    OnEnterPressed(evt)

def SetPhidot(evt): # called on slider events
    value = s2.GetValue()
    global phidot
    phidot = -1*value
    OnEnterPressed(evt)

def SetOmega(evt): # called on slider events
    value = s3.GetValue()
    global omega
    omega = value
    OnEnterPressed(evt)

def SetDamper(evt): # called on slider events
    value = s4.GetValue()
    global dampeningConstant
    dampeningConstant = value
    OnEnterPressed(evt)
 

##constants
LEFTMARGIN = 20
EARTH_RADIUS = 1.0
BASE_POSITION = (0,-12.1 - 1.5,0)
BASE_AXIS = (0,1,0)
BASE_SIZE = (1.5, 1.5, 1.5)
BASE_COLOUR = (255,223,0)

INDICATOR_POSITION = (12.5, 0, 0)
INDICATOR_AXIS = (3, 0, 0)
INDICATOR_WIDTH = 0.2
INDICATOR_COLOR = (255,223,0)
INDICATOR_OPACITY = 0.3

ROD_POSITION = (-11,0,0)
ROD_AXIS = (22,0,0)
ROD_RADIUS = 0.3
ROD_COLOUR = (255,223,0)

GYRO_POSITION = (0,0,0)
GYRO_AXIS = (0.3,0,0)
GYRO_RADIUS = 10
GYRO_COLOUR = (255,223,0)

IRING_POSITION = (0,0,0)
IRING_AXIS = (0,1,0)
IRING_RADIUS = 11.1
IRING_THICKNESS = 0.1
IRING_COLOUR =(255,223,0)

ORING_POSITION = (0,0,0)
ORING_AXIS = (0,0,1)
ORING_RADIUS = 12
ORING_THICKNESS = 0.1
ORING_COLOUR =(255,223,0)

WINDOW_POSX = 0
WINDOW_POSY = 0
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000

TEXTBOX_HEIGHT = 20
TEXTBOX_WIDTH = 150
TEXTBOX1_POSX = LEFTMARGIN
TEXTBOX1_POSY = WINDOW_HEIGHT / 2 + 20
TEXTBOX2_POSX = TEXTBOX1_POSX + LEFTMARGIN + TEXTBOX_WIDTH
TEXTBOX2_POSY = TEXTBOX1_POSY

RATE_SLIDER_POSX = TEXTBOX1_POSX
RATE_SLIDER_POSY = TEXTBOX1_POSY + TEXTBOX_HEIGHT + 25
MIN_RATE = 1
MAX_RATE = 1000

PHIDOT_SLIDER_POSX = TEXTBOX1_POSX
PHIDOT_SLIDER_POSY = RATE_SLIDER_POSY + 50
MIN_PHIDOT = 0
MAX_PHIDOT = 100

OMEGA_SLIDER_POSX = TEXTBOX1_POSX
OMEGA_SLIDER_POSY = PHIDOT_SLIDER_POSY + 50
MIN_OMEGA = 0
MAX_OMEGA = 15

DAMPER_SLIDER_POSX = TEXTBOX1_POSX + 500
DAMPER_SLIDER_POSY = PHIDOT_SLIDER_POSY + 50
MIN_DAMPER = 0
MAX_DAMPER = 15 

Loops_per_second = 50
should_break = false 
dampeningConstant = 1.5
sol = np.zeros((20000,2))
omega =5
#omega = 0.00007295
I1 = .125 * 0.30 * 3 / 2
I2 = I1 / 2
delta = pi/3;
phidot = -50;
OGvector = vector(1,0,0)
##setup window and displays
w = window(title = 'Gyrocompass',x=WINDOW_POSX,y=WINDOW_POSY,width=WINDOW_WIDTH,height=WINDOW_HEIGHT,
           menus = True, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

L = 500
d = LEFTMARGIN
scene1 = display(window=w, x=d, y=d, width=L-2*d, height=L-2*d, forward=-vector(0,1,2),background = (1,1,1))
scene2 = display(window=w, x=d+scene1.width, y=d, width=L-2*d, height=L-2*d, forward=-vector(0,1,2))

##populate scene1
scene1.select()
gyro = frame()
indicator = arrow(frame = gyro, pos= INDICATOR_POSITION, axis= INDICATOR_AXIS , shaftwidth= INDICATOR_WIDTH, color = INDICATOR_COLOR, opacity = INDICATOR_OPACITY) #North Indicator
base = pyramid(pos = BASE_POSITION, axis = BASE_AXIS, size = BASE_SIZE, color = BASE_COLOUR) ## create the suppport for the outer ring 
rod = cylinder(frame = gyro, pos= ROD_POSITION, axis= ROD_AXIS , radius= ROD_RADIUS, color = ROD_COLOUR) #Inner Rotating Circle
spinner = cylinder(frame = gyro, pos= GYRO_POSITION, axis= GYRO_AXIS, radius= GYRO_RADIUS, material = materials.wood) #Circle Supports
IRING = ring(pos = IRING_POSITION , axis = IRING_AXIS, radius = IRING_RADIUS, thickness = IRING_THICKNESS, color = IRING_COLOUR) #XZ Plane Ring
ORING = ring(pos = ORING_POSITION, axis = ORING_AXIS, radius = ORING_RADIUS, thickness = ORING_THICKNESS, color = ORING_COLOUR ) ## this is the outer ring, might be part of a frame later? (Y- Plane ring)


##populate scene 2
scene2.select()
earth = sphere(pos = GYRO_POSITION,material = materials.earth, radius = EARTH_RADIUS)
little_sphere = arrow(pos = earth.pos + (0,0,earth.radius) + (0,0,earth.radius/32), material = materials.emissive, color = (1,0,1),shaftwidth=0.02, length = 0.12)

p = w.panel # Refers to the full region of the window in which to place widgets

wx.StaticText(p, pos=(d,4), size=(L-2*d,d), label='Gyroscope',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
wx.StaticText(p, pos=(d+scene1.width,4), size=(L-2*d,d), label='Earth',
              style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

##setup textbox 1
lat = wx.TextCtrl(p, pos=(TEXTBOX1_POSX,TEXTBOX1_POSY), size=(TEXTBOX_WIDTH,TEXTBOX_HEIGHT), style=wx.TE_PROCESS_ENTER) 
lat.SetValue('0')
lat.SetInsertionPoint(len(lat.GetValue())+1) # position cursor at end of text

##setup textbox 2
lon = wx.TextCtrl(p, pos=(TEXTBOX2_POSX,TEXTBOX2_POSY),size=(TEXTBOX_WIDTH,TEXTBOX_HEIGHT), style=wx.TE_PROCESS_ENTER)
lon.SetInsertionPoint(len(lon.GetValue())+1) # position cursor at end of text
lon.SetValue('0')

wx.StaticText(p, pos=(TEXTBOX1_POSX,TEXTBOX1_POSY - d), size=(L-2*d,d), label='Latitude')
              #style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
wx.StaticText(p, pos=(TEXTBOX2_POSX,TEXTBOX2_POSY - d), size=(L-2*d,d), label='Longitude')
              #style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

#Initializing slider for modifying the rate of program execution.
s1 = wx.Slider(p, pos=(RATE_SLIDER_POSX,RATE_SLIDER_POSY), size=(0.9*L,20), minValue=MIN_RATE, maxValue=MAX_RATE)
s1.Bind(wx.EVT_SCROLL, SetRate)
s1.SetValue(Loops_per_second) # update the slider
wx.StaticText(p, pos=(RATE_SLIDER_POSX,RATE_SLIDER_POSY - 20), label='Set oscillation rate')

#Initializing slider for modifying angular velocity of gyroscope
s2 = wx.Slider(p, pos=(PHIDOT_SLIDER_POSX,PHIDOT_SLIDER_POSY), size=(0.9*L,20), minValue=MIN_PHIDOT, maxValue=MAX_PHIDOT)
s2.Bind(wx.EVT_SCROLL, SetPhidot)
s2.SetValue(phidot) # update the slider
wx.StaticText(p, pos=(PHIDOT_SLIDER_POSX,PHIDOT_SLIDER_POSY - 20), label='Set Gyroscope Angular Velocity')

#Initializing slider for modifying planetary angular velocity
s3 = wx.Slider(p, pos=(OMEGA_SLIDER_POSX,OMEGA_SLIDER_POSY), size=(0.9*L,20), minValue=MIN_OMEGA, maxValue=MAX_OMEGA)
s3.Bind(wx.EVT_SCROLL, SetOmega)
s3.SetValue(omega) # update the slider
wx.StaticText(p, pos=(OMEGA_SLIDER_POSX,OMEGA_SLIDER_POSY - 20), label='Set Planetary Angular Velocity')

#Initializing slider for modifying dampening constant for ode
s4 = wx.Slider(p, pos=(DAMPER_SLIDER_POSX,DAMPER_SLIDER_POSY), size=(0.9*L,20), minValue=MIN_DAMPER, maxValue=MAX_DAMPER)
s4.Bind(wx.EVT_SCROLL, SetDamper)
s4.SetValue(dampeningConstant) # update the slider
wx.StaticText(p, pos=(DAMPER_SLIDER_POSX,DAMPER_SLIDER_POSY - 20), label='Set Dampening Constant')


##if you want to see the little sphere respond to changes in lat and lon use line below
little_sphere.pos = coordsToSphere(float(lat.GetValue()),float(lon.GetValue()))
lat.Bind(wx.EVT_TEXT_ENTER, OnEnterPressed)
lon.Bind(wx.EVT_TEXT_ENTER, OnEnterPressed)

little_sphere.pos = coordsToSphere(float(lat.GetValue()),float(lon.GetValue()))
v1 = vector(0,1,0)
v2 = little_sphere.pos
v3 = cross(v2,v1)
v4 = rotate(v2, angle = pi/2, axis = v3)
OGvector[0] = v4[0]; 
OGvector[1] = v4[1]; 
OGvector[2] = v4[2] 
little_sphere.axis = v4
little_sphere.length = 0.12
sol = RunSimulation()


# The analytical answer in red dots
#exactp;x = np.linspace(-2,2,10)
#exact_y = 2*np.exp(2*exact_x)-exact_x*np.exp(-exact_x)

#start = wx.Button(p, label='Start', pos=(900,15))
#start.Bind(wx.EVT_BUTTON, setright)
while(true):
    for i in range(0,5000):
        wx.Yield()
        if should_break == true:
            should_break = false
            print('lol')
        v1 = little_sphere.pos 
        v2 = rotate(OGvector, angle = sol[i,0], axis = v1)
        little_sphere.axis = v2
        little_sphere.length = 0.12
        rate(100)
        gyro.rotate(angle=0.5)
        gyro.axis = vector(sin(sol[i,0]), 0, cos(sol[i,0]))
        IRING.axis = perpendicular_vector(gyro.axis)



    
