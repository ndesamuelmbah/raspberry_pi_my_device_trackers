from gpiozero import MotionSensor, SmoothedInputDevice
from statistics import median, mean


class SamsMotionSensor(SmoothedInputDevice):
    """
    Extends :class:`SmoothedInputDevice` and represents a passive infra-red
    (PIR) motion sensor like the sort found in the `CamJam #2 EduKit`_.

    .. _CamJam #2 EduKit: http://camjam.me/?page_id=623

    A typical PIR device has a small circuit board with three pins: VCC, OUT,
    and GND. VCC should be connected to a 5V pin, GND to one of the ground
    pins, and finally OUT to the GPIO specified as the value of the *pin*
    parameter in the constructor.
    This class is an built off of MotionSensor from gpiozero.
    The following code will print a line of text when motion is detected::

        from gpiozero import MotionSensor

        pir = SamsMotionSensor(4)
        pir.wait_for_motion()
        print("Motion detected!")

    :type pin: int or str
    :param pin:
        The GPIO pin which the sensor is connected to. See :ref:`pin-numbering`
        for valid pin numbers. If this is :data:`None` a :exc:`GPIODeviceError`
        will be raised.

    :type pull_up: bool or None
    :param pull_up:
        See description under :class:`InputDevice` for more information.

    :type active_state: bool or None
    :param active_state:
        See description under :class:`InputDevice` for more information.

    :param int queue_len:
        The length of the queue used to store values read from the sensor. This
        defaults to 1 which effectively disables the queue. If your motion
        sensor is particularly "twitchy" you may wish to increase this value.

    :param float sample_rate:
        The number of values to read from the device (and append to the
        internal queue) per second. Defaults to 10.

    :param float threshold:
        Defaults to 0.5. When the average of all values in the internal queue
        rises above this value, the sensor will be considered "active" by the
        :attr:`~SmoothedInputDevice.is_active` property, and all appropriate
        events will be fired.

    :param bool partial:
        When :data:`False` (the default), the object will not return a value
        for :attr:`~SmoothedInputDevice.is_active` until the internal queue has
        filled with values.  Only set this to :data:`True` if you require
        values immediately after object construction.

    :type pin_factory: Factory or None
    :param pin_factory:
        See :doc:`api_pins` for more information (this is an advanced feature
        which most users can ignore).

    :type average: an aggregator
    :param average:
        The function used to average the values in the internal queue. This
        defaults to :func:`statistics.median` which is a good selection for
        discarding outliers from jittery sensors. The function specified must
        accept a sequence of numbers and return a single number.

    :type sample_wait: float
    :param float sample_wait:
        The length of time to wait between retrieving the state of the
        underlying device. Defaults to 1/sample_rate. A value of 0.0 indicates that
        values are retrieved as fast as possible.
    """
    def __init__(self, pin=None, *, pull_up=False, active_state=None,
                 queue_len=1, sample_rate=10, threshold=0.2, partial=False,
                 average=None, sample_wait=None,
                 pin_factory=None):
        super().__init__(
            pin, pull_up=pull_up, active_state=active_state,
            threshold=threshold, queue_len=queue_len, sample_wait=sample_wait or 1 /
            sample_rate, partial=partial, pin_factory=pin_factory, average=average or median)
        self._queue.start()

    @property
    def value(self):
        """
        With the default *queue_len* of 1, this is effectively boolean where 0
        means no motion detected and 1 means motion detected. If you specify
        a *queue_len* greater than 1, this will be an averaged value where
        values closer to 1 imply motion detection.
        """
        return super().value

SamsMotionSensor.motion_detected = MotionSensor.is_active
SamsMotionSensor.when_motion = MotionSensor.when_activated
SamsMotionSensor.when_no_motion = MotionSensor.when_deactivated
SamsMotionSensor.wait_for_motion = MotionSensor.wait_for_active
SamsMotionSensor.wait_for_no_motion = MotionSensor.wait_for_inactive
