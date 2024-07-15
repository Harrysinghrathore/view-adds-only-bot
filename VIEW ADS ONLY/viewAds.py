import threading
import logging
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from FileHandler import FileHandler
import time

logging.basicConfig(level=logging.INFO)


class VideoBot:
    def __init__(self, file_handler):
        self.file_handler = file_handler

    def open_chrome(self, proxy):
        """
        Open Chrome browser with specified proxy.

        Parameters:
        - proxy (str): Proxy URL.

        Returns:
        - driver: Selenium WebDriver instance.
        """
        try:
            driver = Driver(uc=True, incognito=True, proxy=proxy, undetectable=True)
            return driver
        except Exception as e:
            logging.error(f"Error opening Chrome: {e}")
            if driver:
                driver.quit()
            raise

    def watch_video(self, driver, video_url, watch_duration, thread_number, time_to_stay_on_ad, num_of_ads):
        """
        Watch a video and interact with ads.

        Parameters:
        - driver: Selenium WebDriver instance.
        - video_url (str): Link to the video.
        - watch_duration (int): Duration to watch the video.
        - thread_number (int): Thread number for logging.
        - time_to_stay_on_ad (int): Time to stay on each ad.
        - num_of_ads (int): Number of ads to interact with.
        """
        try:
            driver.uc_open(video_url)
            logging.info(f"Thread number:{thread_number} Watching video at {video_url} for {watch_duration} seconds")
            original_window = driver.current_window_handle
            start_time = time.time()
            for _ in range(num_of_ads):
                try:
                    print("Windows before:")
                    print(driver.window_handles)
                    # Click ad button
                    driver.uc_click('.ytp-ad-button.ytp-flyout-cta-action-button.ytp-flyout-cta-action-button-rounded', by=By.CSS_SELECTOR, timeout=(watch_duration))
                    logging.info(f"Thread number:{thread_number} ad button clicked!")
                    print("Windows after:")
                    print(driver.window_handles)
                    new_window = [window for window in driver.window_handles if window != original_window][0]
                    driver.switch_to.window(new_window)
                    driver.maximize_window()
                    logging.info(f"Ad window opened!")
                    time.sleep(time_to_stay_on_ad)
                    # Close the new window
                    driver.close()
                    # Switch back to the original window
                    driver.switch_to.window(original_window)
                    logging.info(f"Back to original window")
                    try:
                        driver.uc_click('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > button', by=By.CSS_SELECTOR, timeout=(10))
                        print("Play button clicked!")
                    except:
                        pass
                    time.sleep(30)
                    try:
                        WebDriverWait(driver, 230).until(
                            EC.invisibility_of_element_located((By.CSS_SELECTOR, '.ytp-ad-skip-button-container.ytp-ad-skip-button-container-detached .ytp-ad-skip-button-modern.ytp-button'))
                        )
                    except:
                        pass
                except Exception as e:
                    logging.error(f"Thread number:{thread_number} ad button not clicked! {e}")
                    pass
                end_time = time.time()
                elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time} seconds")
            if watch_duration > elapsed_time:
                time.sleep(watch_duration-elapsed_time)
            else:
                time.sleep(5)
        except Exception as e:
            logging.error(f"Thread number:{thread_number} Error watching video: {e}")
            raise

    def login_gmail(self, driver, email, password, recovery_email, thread_number):
        """
        Log in to Gmail.

        Parameters:
        - driver: Selenium WebDriver instance.
        - email (str): Gmail email address.
        - password (str): Gmail password.
        - recovery_email (str): Recovery email address.
        - thread_number (int): Thread number for logging.
        """
        try:
            driver.maximize_window()
            driver.uc_open("https://accounts.google.com/signin")
            driver.sleep(2)
            driver.type('input[id="identifierId"]', email, timeout=20)
            driver.uc_click('div[id="identifierNext"]', by=By.CSS_SELECTOR, timeout=20)
            logging.info(f"Thread number:{thread_number} Email next clicked")
            driver.type('input[name="Passwd"]', password, timeout=20)
            driver.uc_click('div[id="passwordNext"]', by=By.CSS_SELECTOR, timeout=20)
            logging.info(f"Thread number:{thread_number} Password next clicked")
            driver.sleep(2)
            try:
                driver.uc_click('#yDmH0d > c-wiz > div > div.eKnrVb > div > div.j663ec > div > form > span > section:nth-child(2) > div > div > section > div > div > div > ul > li:nth-child(3) > div > div.vxx8jf', by=By.CSS_SELECTOR, timeout=2)
                logging.info(f"Thread number:{thread_number} Recovery button clicked")
                driver.type('#knowledge-preregistered-email-response', recovery_email, timeout=2)
                driver.uc_click('#view_container > div > div > div.pwWryf.bxPAYd > div > div.zQJV3 > div > div.qhFLie > div > div > button', by=By.CSS_SELECTOR, timeout=2)
                logging.info(f"Thread number:{thread_number} Recovery Next button clicked")
            except Exception as e:
                logging.error(f"Thread number:{thread_number} An error occurred during recovery")

            logging.info(f"Thread number:{thread_number} Log in successful!!!!!!!!")
        except Exception as e:
            logging.error(f"Thread number:{thread_number} An error occurred during login: {e}")


    def bot_task(self, thread_number, video_url, watch_duration,  time_to_stay_on_ad, num_of_ads, email=None, password=None, recovery_email=None,
                 proxy=None):
        """
        Perform bot tasks: login, fetch video, watch video.

        Parameters:
        - thread_number (int): Thread number for logging.
        - video_url (str): Link to the video.
        - watch_duration (int): Duration to watch the video.
        - time_to_stay_on_ad (int): Time to stay on each ad.
        - num_of_ads (int): Number of ads to interact with.
        - email (str): Gmail email address.
        - password (str): Gmail password.
        - recovery_email (str): Recovery email address.
        - proxy (str): Proxy URL.
        """
        driver = None
        try:
            driver = self.open_chrome(proxy)
            if email and password:
                self.login_gmail(driver, email, password, recovery_email, thread_number)

            self.watch_video(driver, video_url, watch_duration, thread_number, time_to_stay_on_ad, num_of_ads)
        except Exception as e:
            logging.error(f"Thread number:{thread_number} Bot task failed: {e}")
            driver.quit()
        finally:
            if driver:
                logging.info(f"Closing thread number:{thread_number}. Bot task Successfull!")
                driver.quit()


# Function to run bot threads (moved from the main script)
def run_bot_threads(video_bot, videos_list, watch_duration, time_to_stay_on_ad, num_of_ads, num_views, login_credentials_list, num_threads=1,
                    proxies_list=None):
    """
    Run multiple bot threads.

    Parameters:
    - video_bot: VideoBot instance.
    - video_url (str): Link to the video.
    - watch_duration (int): Duration to watch the video.
    - time_to_stay_on_ad (int): Time to stay on each ad.
    - num_of_ads (int): Number of ads to interact with.
    - num_views (int): Total number of views.
    - login_credentials_list (list): List of login credentials.
    - num_threads (int): Number of threads.
    - proxies_list (list): List of proxy URLs.
    """
    threads = []
    try:
        for i in range(num_views // num_threads):
            for j in range(num_threads):
                email, password, recovery_email = video_bot.file_handler.select_random_login_credentials(
                    login_credentials_list)
                proxy_url = video_bot.file_handler.select_random_proxy(proxies_list)
                thread_number = i * num_threads + j
                video_url = str(videos_list[thread_number][0])
                url = str(video_url)
                print(url)
                time.sleep(5)
                time.sleep(5)
                thread = threading.Thread(target=video_bot.bot_task,
                                          args=(thread_number, url, watch_duration, time_to_stay_on_ad, num_of_ads, email, password,
                                                recovery_email, proxy_url))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
    except Exception as e:
        logging.error(f"Error creating threads: {e}")
