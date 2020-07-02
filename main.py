from bs4 import BeautifulSoup
import requests
import json
import sys



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}



def get_video_url(tiktok_url):
    '''Extract video source url from usual TikTok url

    Parameters:
    tiktok_url (str): TikTok url

    Returns:
    str: video source url
    '''

    r = requests.get(tiktok_url, headers=headers, allow_redirects=True)

    if r.status_code != 200:
        print('Bad request to TikTok server. Status code: {}'.format(r.status_code))
        sys.exit(1)

    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.find('script', attrs={'id': '__NEXT_DATA__'})

    if not data:
        print('Can\'t get data from url. Check error.txt')
        
        with open('error.txt', 'w', encoding='utf-8') as f:
            f.write(r.text)
        
        sys.exit(1)

    data = json.loads(data.text)

    try:
        video_url = data['props']['pageProps']['videoData']['itemInfos']['video']['urls'][0]
    
    except Exception as e:
        print('Can\'t get source video url. Check error.txt')
        print(e)

        with open('error.txt', 'w', encoding='utf-8') as f:
            json.dump(data, f)

        sys.exit(1)

    return video_url


def get_video_id(soruce_video_url):
    '''Extract video id from source video url

    Parameters:
    soruce_video_url (str): Source video url

    Returns:
    str: video id
    '''

    r = requests.get(soruce_video_url, headers=headers)

    if r.status_code != 200:
        print('Bad request to source video server. Status code: {}'.format(r.status_code))
        sys.exit(1)

    content = r.content
    position = content.find('vid:'.encode())

    if position == -1:
        print('Can\'t find video id')
        sys.exit(1)

    video_id = content[position+4:position+36].decode('utf-8')

    return video_id


def download_video(video_id):
    '''Downloads video without watermark by video id

    Parameters:
    video_id (str): Video id
    '''

    video_url = 'https://api2-16-h2.musical.ly/aweme/v1/play/?video_id={}&vr_type=0&is_play_url=1&source=PackSourceEnum_PUBLISH&media_type=4'.format(video_id)

    r = requests.get(video_url, headers=headers, allow_redirects=True)

    if r.status_code != 200:
        print('Bad request to no watermark video server. Status code: {}'.format(r.status_code))
        sys.exit(1)

    filename = '{}.mp4'.format(video_id)

    with open(filename, 'wb') as f:
        f.write(r.content)

    print('Video', video_id, 'downloaded')



if __name__ == '__main__':
    
    tiktok_url = input('TikTok video url: ')

    video_url = get_video_url(tiktok_url)
    video_id = get_video_id(video_url)

    download_video(video_id)
