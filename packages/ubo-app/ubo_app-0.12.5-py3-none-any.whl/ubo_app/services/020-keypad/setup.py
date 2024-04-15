# pyright: reportMissingImports=false, reportMissingModuleSource=false
# ruff: noqa: D100, D101, D102, D103, D104, D107
from __future__ import annotations

import logging
import math
import time
from enum import StrEnum
from typing import TYPE_CHECKING, Literal

import board
from immutable import Immutable

from ubo_app.store.services.keypad import Key, KeypadKeyPressAction
from ubo_app.store.services.sound import SoundDevice, SoundSetMuteStatusAction
from ubo_app.utils import IS_RPI

if TYPE_CHECKING:
    from adafruit_aw9523 import AW9523
    from adafruit_bus_device import i2c_device
    from adafruit_register.i2c_struct import UnaryStruct

INT_EXPANDER = 5  # GPIO PIN index that receives interrupt from AW9523

ButtonStatus = Literal['pressed', 'released']


class KeypadError(Exception): ...


class ButtonName(StrEnum):
    TOP_LEFT = 'top_left'
    MIDDLE_LEFT = 'middle_left'
    BOTTOM_LEFT = 'bottom_left'
    UP = 'up'
    DOWN = 'down'
    BACK = 'back'
    HOME = 'home'
    MIC = 'mic'


class ButtonEvent(Immutable):
    status: ButtonStatus
    timestamp: float


class Event(Immutable):
    inputs: UnaryStruct
    timestamp: float


class KeypadStatus:
    """Class to keep track of button status.

    0: "TOP_LEFT": Top left button
    1: "MIDDLE_LEFT": Middle left button
    2: "BOTTOM_LEFT": Bottom left button
    3: "BACK": Button with back arrow label (under LCD)
    4: "HOME": Button with home label (Under LCD)
    5: "UP": Right top button with upward arrow label
    6: "DOWN": Right bottom button with downward arrow label
    7: "MIC": Microphone mute switch
    """

    buttons: dict[ButtonName, ButtonEvent]

    def __init__(self: KeypadStatus) -> None:
        self.buttons = {
            button_name: ButtonEvent(status='released', timestamp=time.time())
            for button_name in ButtonName
        }

    def update_status(
        self: KeypadStatus,
        button_name: ButtonName,
        new_status: Literal['pressed', 'released'],
    ) -> None:
        if new_status not in {'pressed', 'released'}:
            msg = 'Invalid status'
            raise KeypadError(msg)
        if button_name in self.buttons:
            self.buttons[button_name] = ButtonEvent(
                status=new_status,
                timestamp=time.time(),
            )

    def get_status(
        self: KeypadStatus,
        button_name: ButtonName,
    ) -> Literal['pressed', 'released']:
        if button_name in self.buttons:
            return self.buttons[button_name].status
        msg = 'Invalid button name'
        raise KeypadError(msg)

    def get_timestamp(self: KeypadStatus, button_name: ButtonName) -> float:
        if button_name in self.buttons:
            return self.buttons[button_name].timestamp
        msg = 'Invalid button name'
        raise KeypadError(msg)

    def get_label(self: KeypadStatus, index: int) -> ButtonName:
        if index > len(ButtonName):
            msg = 'Invalid index'
            raise KeypadError(msg)
        return list(ButtonName)[index]


class Keypad:
    """Class to handle keypad events."""

    event_queue: list[Event]
    aw: AW9523
    inputs: UnaryStruct

    def __init__(self: Keypad) -> None:
        """Initialize a Keypad.

        Initializes various parameters including
        loggers and button names.
        """
        self.logger = logging.getLogger('keypad')
        self.logger.setLevel(logging.WARNING)
        self.logger.debug('Initialising keypad...')
        self.event_queue = []
        self.aw = None
        self.inputs = None
        self.bus_address = 0x58
        self.model = 'aw9523'
        self.enabled = True
        self.buttons = KeypadStatus()
        self.index = 0
        self.init_i2c()

    def clear_interrupt_flags(self: Keypad, i2c: i2c_device.I2CDevice) -> None:
        # Write to both registers to reset the interrupt flag
        buffer = bytearray(2)
        buffer[0] = 0x00
        buffer[1] = 0x00
        i2c.write(buffer)
        i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)

        time.sleep(0.1)
        buffer[0] = 0x01
        buffer[1] = 0x00
        i2c.write(buffer)
        i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)
        time.sleep(0.1)

    def disable_interrupt_for_higher_bits(
        self: Keypad,
        i2c: i2c_device.I2CDevice,
    ) -> None:
        # disable interrupt for higher bits
        buffer = bytearray(2)
        buffer[0] = 0x06
        buffer[1] = 0x00
        i2c.write(buffer)
        i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)

        buffer[0] = 0x07
        buffer[1] = 0xFF
        i2c.write(buffer)
        i2c.write_then_readinto(buffer, buffer, out_end=1, in_start=1)

    def init_i2c(self: Keypad) -> None:
        if not IS_RPI:
            return
        # Use GPIO to receive interrupt from the GPIO expander
        from gpiozero import Button

        i2c = board.I2C()
        # Set this to the GPIO of the interrupt:
        btn = Button(INT_EXPANDER)
        try:
            import adafruit_aw9523

            # Search for the GPIO expander address on the I2C bus
            self.aw = adafruit_aw9523.AW9523(i2c, self.bus_address)
            new_i2c = self.aw.i2c_device
        except Exception:
            self.bus_address = False
            self.logger.exception('Failed to initialize I2C Bus on address 0x58')
            raise

        # Perform soft reset of the expander
        self.aw.reset()
        # Set first 8 low significant bits (register 1) to input
        self.aw.directions = 0xFF00
        time.sleep(1)

        # The code below, accessing the GPIO expander registers directly via i2c
        # was created as a workaround of the reset the interrupt flag.
        self.clear_interrupt_flags(new_i2c)
        self.disable_interrupt_for_higher_bits(new_i2c)
        # reset interrupts again
        self.clear_interrupt_flags(new_i2c)

        # read register values
        self.inputs = self.aw.inputs
        self.logger.debug(
            'Initializing inputs',
            extra={'inputs': f'{self.inputs:016b}'},
        )
        self.event_queue = [Event(inputs=self.inputs, timestamp=time.time())]
        time.sleep(0.5)

        # Interrupt callback when any button is pressed
        btn.when_pressed = self.key_press_cb

    def key_press_cb(self: Keypad, _: object) -> None:
        """Handle key press dispatched by GPIO interrupt.

            This is callback function that gets triggers
         if any change is detected on keypad buttons
         states.

         In this callback, we look at the state
         change to see which button was pressed or leased.

        Parameters
        ----------
        _channel: int
            GPIO channel that triggered the callback
            NOT USED currently

        """
        if self.aw is None:
            return
        # read register values
        self.inputs = self.aw.inputs
        event = Event(inputs=self.inputs, timestamp=time.time())
        # append the event to the queue. The queue has a depth of 2 and
        # keeps the current and last event.
        self.event_queue.append(event)
        self.logger.info(self.event_queue)
        self.logger.debug('Current Inputs', extra={'inputs': f'{self.inputs:016b}'})
        previous_event = self.event_queue.pop(0)
        self.logger.debug(
            'Previous Inputs',
            extra={'inputs': f'{previous_event.inputs:016b}'},
        )
        # XOR the last recorded input values with the current input values
        # to see which bits have changed. Technically there can only be one
        # bit change in every callback
        change_mask = previous_event.inputs ^ self.inputs
        self.logger.debug('Change', extra={'change_mask': f'{change_mask:016b}'})
        if change_mask == 0:
            return
        # use the change mask to see if the button was the change was
        # falling (1->0) indicating a pressed action
        # or risign (0->1) indicating a release action
        self.index = (int)(math.log2(change_mask))
        self.logger.info('button index', extra={'button_index': self.index})
        # Check for rising edge or falling edge action (press or release)
        self.button_label = self.buttons.get_label(self.index)
        if (previous_event.inputs & change_mask) == 0:
            self.logger.info(
                'Button pressed',
                extra={'button': str(self.index), 'label': self.button_label},
            )

            # calculate how long the button was held down
            # and print the time
            last_time_stamp = self.buttons.get_timestamp(self.button_label)
            held_down_time = time.time() - last_time_stamp
            self.logger.info(
                'Button was pressed down',
                extra={'held_down_time': held_down_time},
            )

            self.buttons.update_status(self.button_label, 'released')
            self.on_button_event(self.button_label, 'released')

        else:
            self.logger.info(
                'Button released',
                extra={'button': str(self.index), 'label': self.button_label},
            )
            self.buttons.update_status(self.button_label, 'pressed')
            self.on_button_event(self.button_label, 'pressed')

        self.logger.info(self.buttons.buttons)

    def on_button_event(
        self: Keypad,
        button_pressed: ButtonName,
        button_status: ButtonStatus,
    ) -> None:
        from ubo_app.store import dispatch

        if button_status == 'pressed':
            if button_pressed == ButtonName.UP:
                dispatch(
                    KeypadKeyPressAction(
                        key=Key.UP,
                    ),
                )
            elif button_pressed == ButtonName.DOWN:
                dispatch(
                    KeypadKeyPressAction(
                        key=Key.DOWN,
                    ),
                )
            elif button_pressed == ButtonName.TOP_LEFT:
                dispatch(
                    KeypadKeyPressAction(
                        key=Key.L1,
                    ),
                )
            elif button_pressed == ButtonName.MIDDLE_LEFT:
                dispatch(
                    KeypadKeyPressAction(
                        key=Key.L2,
                    ),
                )
            elif button_pressed == ButtonName.BOTTOM_LEFT:
                dispatch(
                    KeypadKeyPressAction(
                        key=Key.L3,
                    ),
                )
            elif button_pressed == ButtonName.BACK:
                dispatch(
                    KeypadKeyPressAction(
                        key=Key.BACK,
                    ),
                )
            elif button_pressed == ButtonName.HOME:
                dispatch(
                    KeypadKeyPressAction(
                        key=Key.HOME,
                    ),
                )
        if button_pressed == ButtonName.MIC:
            from ubo_app.store import dispatch

            dispatch(
                SoundSetMuteStatusAction(
                    device=SoundDevice.INPUT,
                    mute=button_status == 'pressed',
                ),
            )


def init_service() -> None:
    if not IS_RPI:
        return
    Keypad()
