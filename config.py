import configparser

def ini_read():
    config = configparser.ConfigParser()
    config.read('settings.ini') #path of your .ini file
    web_driver = config.get("Settings","path") 
    return web_driver