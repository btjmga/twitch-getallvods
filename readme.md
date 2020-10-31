# Twitch-getallvods

This tool allows to get all VOD URLs of a specified user and/or download them one by one.

Naming convention for downloaded vods is: title + date.

## Installation

```bash
pip install streamlink
```



And you can use the source with import.


###### (Optional):
If needed for streamlink install Microsoft C++ Build Tools [https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)

From installation options choose Windows 10 SDK and newest MSVC C++ x64/x86 build tools

## Usage

Provide variables:
```python
MyClientID = '###'
MyClientSecret = '###'
```
These can be retrevied by registering an app here: [https://dev.twitch.tv](https://dev.twitch.tv)
```python
MyUsername = '###'
```
This specifies the target user (by twitch.tv username)
```python
download_videos(videos_desc_list, videos_url_list) 
```
This method is used to initialize 


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[UNLICENSE](https://unlicense.org/)
