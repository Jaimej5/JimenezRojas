import Ice

import sys
class Downloader():

    def addDownloadTask(self, url):
        print("URL recibida ",url)
        print("descargando")
        return "Descarga" +url+"finalizada"