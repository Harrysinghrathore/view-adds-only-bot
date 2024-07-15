from FileHandler import FileHandler
from viewAds import VideoBot, run_bot_threads

def get_hardcoded_params():
    """
    Get hardcoded parameters from user input.

    Returns:
    - Tuple of parameters.
    """
    proxies_file_path = 'checked_proxies.xlsx'
    login_credentials_file_path = 'logins.xlsx'
    videos_file_path = 'videos.xlsx'
    watch_duration = int(input("Enter the watch duration in seconds: "))
    num_views = int(input("Enter the total number of views: "))
    num_threads = int(input("Enter the number of threads: "))
    time_to_stay_on_ad = int(input("Enter the time to stay on ad in seconds: "))
    num_of_ads = int(input("Enter the number of ads: "))

    return proxies_file_path, login_credentials_file_path, videos_file_path, watch_duration, num_views, num_threads, time_to_stay_on_ad, num_of_ads

if __name__ == "__main__":
    proxies_file_path, login_credentials_file_path, videos_file_path, watch_duration, num_views, num_threads, time_to_stay_on_ad, num_of_ads = get_hardcoded_params()

    file_handler = FileHandler(proxies_file_path, login_credentials_file_path, videos_file_path)
    video_bot = VideoBot(file_handler)

    login_credentials_list = file_handler.read_login_credentials_from_excel(
        email_col_index=0,
        password_col_index=1,
        recovery_email_col_index=2
    )
    video_list = file_handler.read_channels_from_excel()
    proxies_list = file_handler.read_proxies_from_excel(ip_col_index=0, port_col_index=1)

    run_bot_threads(video_bot, video_list, watch_duration, time_to_stay_on_ad, num_of_ads, num_views, login_credentials_list, num_threads, proxies_list)

# End of runBot.py
