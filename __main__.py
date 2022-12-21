from utils.loader import client
from utils.configs import configData

if __name__ == '__main__':

    client(configData['prefix'],configData['token']).__start__()