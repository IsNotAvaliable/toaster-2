# Define states
IDLE = 0
SELECTTIME = 1
TOASTING = 2
FINISHED = 3

# Set initial variable values
start_time_ms = control.millis()
button_A_was_pressed = False
button_B_was_pressed = False
button_AB_was_pressed = False
State = IDLE
currentTime = 0.0
strip = neopixel.create(DigitalPin.P2, 8, NeoPixelMode.RGB)

# functions
def toasting_toast():
    pins.digital_write_pin(DigitalPin.P1, 1)
    pass

def untoasting_toast():
    pins.digital_write_pin(DigitalPin.P1, 0)
    strip.show_color(neopixel.rgb(0, 0, 0))
    strip.show()
    pass

def selectingtime():
    strip.show_color(neopixel.rgb(255, 194, 0))
    strip.show()
    pass

# These functions take care of button presses throughout the program. This function makes it so that
# you register a full press and release of the button before anything happens. If you are using two buttons,
# you should do something similar.

def on_button_pressed_a():
    global button_A_was_pressed
    button_A_was_pressed = True
    pass

def on_button_pressed_b():
    global button_B_was_pressed
    button_B_was_pressed = True
    pass

def on_button_pressed_ab():
    global button_AB_was_pressed
    button_AB_was_pressed = True
    pass

input.on_button_pressed(Button.A, on_button_pressed_a)
input.on_button_pressed(Button.B, on_button_pressed_b)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

# This function is used to indicate that the timer has run down to zero.
def playSound():
    music.play_tone(Note.C, music.beat())

def updateSystem():
    # Any Python function needs the global keyword next to any global variable names
    # you plan to use.
    global start_time_ms
    global currentTime
    global button_A_was_pressed
    global button_B_was_pressed
    global button_AB_was_pressed

    #Slide 3 describes the logic below
    if(State == SELECTTIME):  
        # This updates with the current time for cooking. This is needed to 
        start_time_ms = control.millis()
        # If button B is pressed during IDLE, it adds 5 seconds to the currentTime which tracks cooking time.
        if(button_B_was_pressed):
            basic.clear_screen()
            currentTime += 5
            basic.show_number(currentTime,50)
            button_B_was_pressed = False
        if(button_A_was_pressed):
            basic.clear_screen()
            currentTime -= 5
            basic.show_number(currentTime,50)
            button_A_was_pressed = False
            
    if(State == TOASTING):
        if(button_AB_was_pressed):
            currentTime = 0
            button_AB_was_pressed = False
            
            
def evaluateState(state):
    # Changes of state depend only on these three global variables.
    global button_A_was_pressed
    global button_B_was_pressed
    global button_AB_was_pressed
    global currentTime

    # This is the logic presented on slide 4
    if(state==IDLE):
        if(button_B_was_pressed) or (button_A_was_pressed):

            # You will see me use this structure throughout the program - why not use input.button_is_pressed(Button.A)?
            # This is because we want to track a full button press and release before changing state. By using a variable
            # to store a Boolean value indicating that a full button press has occurred, it only registers a change
            # once per press. Otherwise, holding down the button would cause this logic to run continuously.
            # We also set this equal to false after we use it so that we are ready to notice the next press.
            button_B_was_pressed = False
            button_A_was_pressed = False
            return SELECTTIME
    
    # This is the logic presented on slide 5
    elif(state == SELECTTIME):
        if(button_AB_was_pressed):
            button_AB_was_pressed = False
            return TOASTING

    # This is the logic presented on slide 6
    elif(state == TOASTING):
         if(button_A_was_pressed):
            button_A_was_pressed = False
            return SELECTTIME

         elif(button_B_was_pressed):
             button_B_was_pressed = False
             return SELECTTIME

         if(currentTime <= 0):
                    return FINISHED

    # This is the logic presented on slide 7
    elif(state==FINISHED):
        return IDLE
    
    # If the logic somehow fails, or no changes to state are needed based on the variables, we leave the state unchanged.
    return state

def reactToState(state):
    global currentTime
    
    # For the purpose of demonstrating that this works, I've used print statements for everything here except DONE.
    # 
    if(state == SELECTTIME):
        # The convert_to_text function is how you turn a number into a string using the serial port.
        serial.write_line("select time")
        selectingtime()
    elif(state == TOASTING):
        serial.write_line("time left:" + convert_to_text(currentTime))
        toasting_toast()
        pause(1000)
        currentTime -= 1
    elif(state == FINISHED):
        serial.write_line("toast is ready!")
        untoasting_toast()
        playSound()
    elif(state == IDLE):
        serial.write_line("waiting")

def on_forever():
    global State
    
    # Here are the standard functions for a state machine program.
    updateSystem()
    State = evaluateState(State)
    reactToState(State) 
    pass

# This next line seems so basic, but it is what tells the micro:bit to run the entire program. 
basic.forever(on_forever)