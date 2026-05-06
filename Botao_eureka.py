import time

class Botao:
    def __init__(self, pin):
        self.pin = pin
        self.last_state = 1
        self.click_count = 0
        self.last_release_time = 0
        self.long_press_time = 600
        self.double_click_time = 400
        self.pressed_time = 0

    def update(self):
        now = time.ticks_ms()
        state = self.pin.value()

        if self.last_state == 1 and state == 0:
            time.sleep_ms(30)
            if self.pin.value() == 0:
                self.pressed_time = now

        if self.last_state == 0 and state == 1:
            press_duration = time.ticks_diff(now, self.pressed_time)

            if press_duration >= self.long_press_time:
                self.click_count = 0
                self.last_state = state
                return "long"
            else:
                self.click_count += 1
                self.last_release_time = now

        if self.click_count > 0:
            if time.ticks_diff(now, self.last_release_time) > self.double_click_time:
                if self.click_count == 1:
                    self.click_count = 0
                    self.last_state = state
                    return "single"

                elif self.click_count == 2:
                    self.click_count = 0
                    self.last_state = state
                    return "double"

                self.click_count = 0

        self.last_state = state
        return None