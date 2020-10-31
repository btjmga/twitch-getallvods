# Twitch-getallvods

This tool allows to get all VOD URLs of a specified user and/or download them one by one.

Naming convention for downloaded vods is: title + date.

## Installation

```bash
pip install streamlink
```



Use main.py as an import


###### (Optional):
If needed for streamlink install Microsoft C++ Build Tools [https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)

From installation options choose Windows 10 SDK and newest MSVC C++ x64/x86 build tools

## Usage

Provide variables:
```python
clientID = ''
clientSecret = ''
```
These can be retrevied by registering an app here: [https://dev.twitch.tv](https://dev.twitch.tv)
```python
username = ''
```
This specifies the target user (by twitch.tv username)

Run main.py after providing variables


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[UNLICENSE](https://unlicense.org/)
