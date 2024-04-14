import random
from django.db import models
import firebase_admin
from django.db.models.fields.files import FieldFile
from firebase_admin import storage, credentials
import filetype
import os


class CustomFileField(FieldFile):
    @property
    def url(self):
        self._require_file()
        return self.name


def initialize_firebase_app():
    from django.conf import settings
    try:
        app = firebase_admin.get_app()
    except ValueError:
        if verificar_configuracao('FIREBASEKEYPATH'):
            cred = credentials.Certificate(os.path.join(os.path.join(settings.BASE_DIR, settings.FIREBASEKEYPATH), 'Key.json'))
        else:
            cred = credentials.Certificate(os.path.join(settings.BASE_DIR, 'Key.json'))
        firebase_admin.initialize_app(cred, settings.STORAGEBUCKET)


def existe_conteudo(file):
    try:
        if file.size > 0:
            return True
        else:
            return False
    except:
        return False


def verificar_configuracao(nome_variavel):
    from django.conf import settings
    if not isinstance(nome_variavel, str):
        raise TypeError("O nome da variável deve ser uma string.")
    if hasattr(settings, nome_variavel):
        return getattr(settings, nome_variavel)
    else:
        return ''



class FirebaseFileField(models.FileField):

    attr_class = CustomFileField

    def __init__(self, *args, **kwargs):
        self.auto_delete = kwargs.pop('auto_delete', True)
        super().__init__(*args, **kwargs)


    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        models.signals.post_delete.connect(self.delete_file, sender=cls)


    def delete_file(self, instance, **kwargs):
        if self.auto_delete:
            self.blobdelet(self.urlsavedef(getattr(instance, self.attname)))


    def save_to_firebase(self, file, saveurl):
        initialize_firebase_app()
        bucket = storage.bucket()
        bucket.make_public()
        blob = bucket.blob(self.nomeadequado(saveurl))
        x=None
        with file.open('rb') as f:
            if not x:
                file_type = filetype.guess(f)
                blob.content_type = file_type.mime
                x=True
            blob.upload_from_file(f)
        blob.make_public()
        return blob.public_url


    def urladequada(self,nome):
        from django.conf import settings
        saveurl = f"{verificar_configuracao('MEDIA_URL')}{self.upload_to}{nome}"
        if saveurl[0] == '/':
            saveurl = saveurl[1:]
            saveurl = saveurl.replace('//', '/')
        return saveurl


    def urlsavedef(self, file):
        if file:
            if not type(file) == str:
                if 'https://' in file.name:
                    saveurl = file.name.replace('https://','')
                    saveurl = saveurl.split('/')
                    del saveurl[0]
                    del saveurl[0]
                    retsaveurl=''
                    for i in saveurl:
                        retsaveurl+=f"/{i}"
                    return retsaveurl[1:]
                else:
                    return self.urladequada(file.name)
            return self.urladequada(file)
        return None


    def existe(self,path):
        initialize_firebase_app()
        bucket = storage.bucket()
        blob = bucket.blob(path)
        try:
            if blob.exists():
                return True
            else:
                return False
        except Exception as e:
            print(f"Ocorreu um erro ao verificar o arquivo: {e}")
            return False


    def mover_arquivo_firebase(self, origem, destino):
        if self.existe(origem):
            initialize_firebase_app()
            bucket = storage.bucket()
            bucket.make_public()
            blob_origem = bucket.blob(origem)
            blob_destino = bucket.blob(self.nomeadequado(destino))
            data = blob_origem.download_as_string()
            content_type = blob_origem.content_type
            blob_destino.upload_from_string(data, content_type=content_type)
            blob_destino.make_public()
            self.blobdelet(origem)
            return blob_destino.public_url
        return None


    def blobdelet(self, path):
        if path:
            if self.existe(path):
                initialize_firebase_app()
                bucket = storage.bucket()
                bucket.make_public()
                blob = bucket.blob(path)
                blob.delete()
        return None


    def nomeadequado(self, path, ambos=True):
        path = path.split('/')
        path = path[len(path)-1]
        nome, ex = os.path.splitext(path)
        endere=self.urlsavedef(path)
        x=''
        while self.existe(endere):
            x = random.randint(10000, 99999)
            endere = self.urlsavedef(f"{nome}{x}{ex}")
        if ambos:
            return endere
        return f"{nome}{x}"


    def veri_save_to_firebase(self, model_instance, file, saveurl):
        if model_instance.pk:
            self.blobdelet(
                self.urlsavedef(getattr(model_instance.__class__.objects.get(pk=model_instance.pk), self.attname)))
        return self.save_to_firebase(file, saveurl)


    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)
        if file:
            saveurlatua = self.urlsavedef(file)
            if existe_conteudo(file):
                return self.veri_save_to_firebase(model_instance, file, saveurlatua)
            if self.existe(saveurlatua):
                saveurlatuaver = self.urladequada(saveurlatua.split('/')[-1])
                if saveurlatuaver != saveurlatua:
                    return self.mover_arquivo_firebase(saveurlatua,saveurlatuaver)
                return file
            return None
        if model_instance.pk:
            self.blobdelet(self.urlsavedef(getattr(model_instance.__class__.objects.get(pk=model_instance.pk), self.attname)))
        return None