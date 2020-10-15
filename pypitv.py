#!/usr/bin/python3
import sys, os
from datetime import datetime, timedelta
from urllib import request

# Location of local files for settings and channels cache
settings_file = './.pypitv-settings'
channels_file = './.pypitv-channels'
custom_channels_file = './.pypitv-custom-channels'

# pypitv default settings
pypitv_settings = {
    'update_stmp': 0,
    'default_volume': 0,
    'default_display': 5,
    'refresh_hours': 16,
    'ask_before_playing': 'yes',
    'first_match_only': 'no',
    'silent': 'yes',
    'm3u_url': ''
}

def main():
    load_settings()
    
    if pypitv_settings['m3u_url'] == '':
        print("Enter M3U URL:")
        pypitv_settings['m3u_url'] = input()
        pypitv_settings['update_stmp'] = 0
    
    update_m3u()    
    save_settings()
    
    if len(sys.argv) < 2:
        print('USAGE: pypitv.py "channel name"')
        quit()

    search_string = sys.argv[1]
    
    play_custom_channel(search_string)
    play_iptv_channel(search_string)

def load_settings():
    if os.path.isfile(settings_file):
        file = open(settings_file)
        for line in file:
            (key, value) = line.strip().split(';')
            pypitv_settings[key] = value
        file.close()

def update_m3u():
    last_m3u_update = datetime.fromtimestamp(float(pypitv_settings['update_stmp']))
    delta = datetime.now() - timedelta(hours=int(pypitv_settings['refresh_hours']))
    if delta > last_m3u_update:
        if pypitv_settings['silent'] == 'no':
            print("Updating M3U data...")
        raw = request.urlopen(pypitv_settings['m3u_url']).read().decode('utf-8-sig')
        wf = open(channels_file, "w")
        wf.write(raw)
        pypitv_settings['update_stmp'] = datetime.now().timestamp()

def save_settings():
    sf = open(settings_file, "w")
    for key in pypitv_settings:
        sf.write(key + ';' + str(pypitv_settings[key]) + '\n')
    sf.close()

def play(name, url):
    command = "omxplayer --display " + pypitv_settings['default_display'] + ' --vol ' + pypitv_settings['default_volume'] + ' ' + url
    if pypitv_settings['silent'] == 'yes':
        command += ' > /dev/null'
    if pypitv_settings['ask_before_playing'] == 'yes':
        print('Play', name + '?')
        response = input('(S)kip, (Q)uit or (Return) to play: ')
        if response.lower() == 'q':
            quit()
        elif response.lower() == 's':
            return
    os.system(command)
    if pypitv_settings['first_match_only'] == 'yes':
        quit()

def play_all(channels, channel_name):
    for (name, url) in channels:
        if channel_name in name.lower():
            play(name, url)
    
def play_custom_channel(channel_name):
    if os.path.isfile(custom_channels_file):
        file = open(custom_channels_file)
        custom_channels = []
        for line in file:
            data = line.strip().split(';')
            if len(data) == 2:
                custom_channels.append((data[0], data[1]))
        file.close()
        play_all(custom_channels, channel_name)
                
def play_iptv_channel(channel_name):
    if not os.path.isfile(channels_file):
        pypitv_settings['update_stmp'] = 0
        update_m3u()
        save_settings()
    file = open(channels_file)
    iptv_channels = []
    last_channel_name = ''
    for line in file:
        if line.strip() == '#EXTM3U':
            continue
        elif line[:7] == '#EXTINF':
            last_channel_name = line.strip().split(',')[1]
        else:
            iptv_channels.append((last_channel_name, line.strip()))
    file.close()
    play_all(iptv_channels, channel_name)

            
if __name__ == "__main__":
   main()
