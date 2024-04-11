from __future__ import annotations

import re
from contextlib import suppress
from typing import Optional, Union

from playwright.async_api import Error as PlaywrightError
from playwright.async_api import FrameLocator, Page, Request, Route, TimeoutError

from recognizer import Detector


class AsyncChallenger:
    def __init__(self, page: Page, click_timeout: Optional[int] = None, retry_times: int = 15) -> None:
        """
        Initialize a reCognizer AsyncChallenger instance with specified configurations.

        Args:
            page (Page): The Playwright Page to initialize on.
            click_timeout (int, optional): Click Timeouts between captcha-clicks.
            retry_times (int, optional): Maximum amount of retries before raising an Exception. Defaults to 15.
        """
        self.page = page
        self.routed_page = False
        self.detector = Detector()

        self.click_timeout = click_timeout
        self.retry_times = retry_times
        self.retried = 0

        self.dynamic: bool = False
        self.captcha_token: Optional[str] = None

    async def route_handler(self, route: Route, request: Request) -> None:
        response = await route.fetch()
        await route.fulfill(response=response)  # Instant Fulfillment to save Time
        response_text = await response.text()
        assert response_text

        self.dynamic = "dynamic" in response_text

        # Checking if captcha succeeded
        if "userverify" in request.url and "rresp" not in response_text and "bgdata" not in response_text:
            match = re.search(r'"uvresp"\s*,\s*"([^"]+)"', response_text)
            assert match
            self.captcha_token = match.group(1)

    async def check_result(self) -> Union[str, None]:
        if self.captcha_token:
            return self.captcha_token

        with suppress(PlaywrightError):
            captcha_token: str = await self.page.evaluate("grecaptcha.getResponse()")
            return captcha_token

        with suppress(PlaywrightError):
            enterprise_captcha_token: str = await self.page.evaluate("grecaptcha.enterprise.getResponse()")
            return enterprise_captcha_token

        return None

    async def check_captcha_visible(self):
        captcha_frame = self.page.frame_locator("//iframe[contains(@src,'bframe')]")
        label_obj = captcha_frame.locator("//strong")
        try:
            await label_obj.wait_for(state="visible", timeout=10000)
        except TimeoutError:
            return False

        return await label_obj.is_visible()

    async def click_checkbox(self) -> bool:
        # Clicking Captcha Checkbox
        try:
            checkbox = self.page.frame_locator("iframe[title='reCAPTCHA']").first
            await checkbox.locator(".recaptcha-checkbox-border").click()
            return True
        except TimeoutError:
            return False

    async def detect_tiles(self, prompt: str, area_captcha: bool) -> bool:
        image = await self.page.screenshot(full_page=True)
        response, coordinates = self.detector.detect(prompt, image, area_captcha=area_captcha)

        if not any(response):
            return False

        for coord_x, coord_y in coordinates:
            await self.page.mouse.click(coord_x, coord_y)
            if self.click_timeout:
                await self.page.wait_for_timeout(self.click_timeout)

        return True

    async def load_captcha(self, captcha_frame: Optional[FrameLocator] = None, reset: Optional[bool] = False) -> Union[str, bool]:
        # Retrying
        self.retried += 1
        if self.retried >= self.retry_times:
            raise RecursionError(f"Exceeded maximum retry times of {self.retry_times}")

        if not await self.check_captcha_visible():
            if captcha_token := await self.check_result():
                return captcha_token
            elif not await self.click_checkbox():
                raise TimeoutError("Invisible reCaptcha Timed Out.")

        assert await self.check_captcha_visible(), TimeoutError("[ERROR] reCaptcha Challenge is not visible.")

        # Clicking Reload Button
        if reset:
            assert isinstance(captcha_frame, FrameLocator)
            try:
                reload_button = captcha_frame.locator("#recaptcha-reload-button")
                await reload_button.click()
            except TimeoutError:
                return await self.load_captcha()

            # Resetting Values
            self.dynamic = False
            self.captcha_token = ""

        return True

    async def handle_recaptcha(self) -> Union[str, bool]:
        if isinstance(loaded_captcha := await self.load_captcha(), str):
            return loaded_captcha

        # Getting the Captcha Frame
        captcha_frame = self.page.frame_locator("//iframe[contains(@src,'bframe')]")
        label_obj = captcha_frame.locator("//strong")
        if not (prompt := await label_obj.text_content()):
            raise ValueError("reCaptcha Task Text did not load.")

        # Checking if Captcha Loaded Properly
        for _ in range(30):
            # Getting Recaptcha Tiles
            recaptcha_tiles = await captcha_frame.locator("[class='rc-imageselect-tile']").all()
            tiles_visibility = [await tile.is_visible() for tile in recaptcha_tiles]
            if len(recaptcha_tiles) in (9, 16) and len(tiles_visibility) in (9, 16):
                break

            await self.page.wait_for_timeout(1000)
        else:
            await self.load_captcha(captcha_frame, reset=True)
            return await self.handle_recaptcha()

        # Detecting Images and Clicking right Coordinates
        area_captcha = len(recaptcha_tiles) == 16
        result_clicked = await self.detect_tiles(prompt, area_captcha)

        if self.dynamic and not area_captcha:
            while result_clicked:
                await self.page.wait_for_timeout(5000)
                result_clicked = await self.detect_tiles(prompt, area_captcha)
        elif not result_clicked:
            await self.load_captcha(captcha_frame, reset=True)
            return await self.handle_recaptcha()

        # Submit challenge
        try:
            submit_button = captcha_frame.locator("#recaptcha-verify-button")
            await submit_button.click()
        except TimeoutError:
            await self.load_captcha(captcha_frame, reset=True)
            return await self.handle_recaptcha()

        # Waiting for captcha_token for 5 seconds
        for _ in range(5):
            if captcha_token := await self.check_result():
                return captcha_token

            await self.page.wait_for_timeout(1000)

        # Check if error occurred whilst solving
        incorrect = self.page.locator("[class='rc-imageselect-incorrect-response']")
        errors = self.page.locator("[class *= 'rc-imageselect-error']")
        if await incorrect.is_visible() or any([await error.is_visible() for error in await errors.all()]):
            await self.load_captcha(captcha_frame, reset=True)

        # Retrying
        return await self.handle_recaptcha()

    async def solve_recaptcha(self) -> Union[str, bool]:
        """
        Solve a hcaptcha-challenge on the specified Playwright Page

        Returns:
            str/bool: The result of the challenge
        Raises:
            RecursionError: If the challenger doesn´t succeed in the given retry times
        """
        # Resetting Values
        self.dynamic = False
        self.captcha_token = ""

        # Checking if Page needs to be routed
        if not self.routed_page:
            route_captcha_regex = re.compile(r"(\b(?:google\.com.*(?:reload|userverify)|recaptcha\.net.*(?:reload|userverify))\b)")
            await self.page.route(route_captcha_regex, self.route_handler)
            self.routed_page = True

        await self.click_checkbox()
        await self.page.wait_for_timeout(2000)
        return await self.handle_recaptcha()
