//  Define states
let IDLE = 0
let SELECTTIME = 1
let TOASTING = 2
let FINISHED = 3
//  Set initial variable values
let start_time_ms = control.millis()
let button_A_was_pressed = false
let button_B_was_pressed = false
let button_AB_was_pressed = false
let State = IDLE
let currentTime = 0.0
let strip = neopixel.create(DigitalPin.P2, 8, NeoPixelMode.RGB)
//  functions
function toasting_toast() {
    pins.digitalWritePin(DigitalPin.P1, 1)
    
}

function untoasting_toast() {
    pins.digitalWritePin(DigitalPin.P1, 0)
    strip.showColor(neopixel.rgb(0, 0, 0))
    strip.show()
    
}

function selectingtime() {
    strip.showColor(neopixel.rgb(255, 194, 0))
    strip.show()
    
}

//  These functions take care of button presses throughout the program. This function makes it so that
//  you register a full press and release of the button before anything happens. If you are using two buttons,
//  you should do something similar.
input.onButtonPressed(Button.A, function on_button_pressed_a() {
    
    button_A_was_pressed = true
    
})
input.onButtonPressed(Button.B, function on_button_pressed_b() {
    
    button_B_was_pressed = true
    
})
input.onButtonPressed(Button.AB, function on_button_pressed_ab() {
    
    button_AB_was_pressed = true
    
})
//  This function is used to indicate that the timer has run down to zero.
function playSound() {
    music.playTone(Note.C, music.beat())
}

function updateSystem() {
    //  Any Python function needs the global keyword next to any global variable names
    //  you plan to use.
    
    
    
    
    
    // Slide 3 describes the logic below
    if (State == SELECTTIME) {
        //  This updates with the current time for cooking. This is needed to 
        start_time_ms = control.millis()
        //  If button B is pressed during IDLE, it adds 5 seconds to the currentTime which tracks cooking time.
        if (button_B_was_pressed) {
            basic.clearScreen()
            currentTime += 5
            basic.showNumber(currentTime, 50)
            button_B_was_pressed = false
        }
        
        if (button_A_was_pressed) {
            basic.clearScreen()
            currentTime -= 5
            basic.showNumber(currentTime, 50)
            button_A_was_pressed = false
        }
        
    }
    
    if (State == TOASTING) {
        if (button_AB_was_pressed) {
            currentTime = 0
            button_AB_was_pressed = false
        }
        
    }
    
}

function evaluateState(state: number): number {
    //  Changes of state depend only on these three global variables.
    
    
    
    
    //  This is the logic presented on slide 4
    if (state == IDLE) {
        if (button_B_was_pressed || button_A_was_pressed) {
            //  You will see me use this structure throughout the program - why not use input.button_is_pressed(Button.A)?
            //  This is because we want to track a full button press and release before changing state. By using a variable
            //  to store a Boolean value indicating that a full button press has occurred, it only registers a change
            //  once per press. Otherwise, holding down the button would cause this logic to run continuously.
            //  We also set this equal to false after we use it so that we are ready to notice the next press.
            button_B_was_pressed = false
            button_A_was_pressed = false
            return SELECTTIME
        }
        
    } else if (state == SELECTTIME) {
        //  This is the logic presented on slide 5
        if (button_AB_was_pressed) {
            button_AB_was_pressed = false
            return TOASTING
        }
        
    } else if (state == TOASTING) {
        //  This is the logic presented on slide 6
        if (button_A_was_pressed) {
            button_A_was_pressed = false
            return SELECTTIME
        } else if (button_B_was_pressed) {
            button_B_was_pressed = false
            return SELECTTIME
        }
        
        if (currentTime <= 0) {
            return FINISHED
        }
        
    } else if (state == FINISHED) {
        //  This is the logic presented on slide 7
        return IDLE
    }
    
    //  If the logic somehow fails, or no changes to state are needed based on the variables, we leave the state unchanged.
    return state
}

function reactToState(state: number) {
    
    //  For the purpose of demonstrating that this works, I've used print statements for everything here except DONE.
    //  
    if (state == SELECTTIME) {
        //  The convert_to_text function is how you turn a number into a string using the serial port.
        serial.writeLine("select time")
        selectingtime()
    } else if (state == TOASTING) {
        serial.writeLine("time left:" + convertToText(currentTime))
        toasting_toast()
        pause(1000)
        currentTime -= 1
    } else if (state == FINISHED) {
        serial.writeLine("toast is ready!")
        untoasting_toast()
        playSound()
    } else if (state == IDLE) {
        serial.writeLine("waiting")
    }
    
}

//  This next line seems so basic, but it is what tells the micro:bit to run the entire program. 
basic.forever(function on_forever() {
    
    //  Here are the standard functions for a state machine program.
    updateSystem()
    State = evaluateState(State)
    reactToState(State)
    
})
