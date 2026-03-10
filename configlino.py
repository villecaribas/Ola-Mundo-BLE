import json

class Configlino:
    def __init__(self, config_file = "configlino.json"):
        self.config_file = config_file
        self._id_lino = ""
        self._token = ""
        self._proto_com = ""
        self._wifi_modo = None
        self._ssid = None
        self._senha = None
        
        self.PROTO_COM_OPTIONS = ["bluetooth", "wifi", "serial", "mqtt", "esp-now"]
        self.WIFI_MODO_OPTIONS = ["ESTACAO", "PONTO_DE_ACESSO"]
        
    @property
    def id_lino(self):
        return self._id_lino
    
    @id_lino.setter
    def id_lino(self, value):
        if not value:
            raise ValueError("ID Lino não pode estar vazio")
        self._id_lino = value
        
    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, value):
        if not value:
            raise ValueError("Token não pode estar vazio")
        self._token = value
        
    @property
    def proto_com(self):
        return self._proto_com
    
    @proto_com.setter
    def proto_com(self, value):
        if value not in self.PROTO_COM_OPTIONS:
            raise ValueError(f"Protocolo de comunicação deve ser um dos seguintes: {self.PROTO_COM_OPTIONS}")
        self._proto_com = value
        
    @property
    def wifi_modo(self):
        return self._wifi_modo
    
    @wifi_modo.setter
    def wifi_modo(self, value):
        if value is not None and value not in self.WIFI_MODO_OPTIONS:
            raise ValueError(f"Modo WiFi deve ser um dos seguintes: {self.WIFI_MODO_OPTIONS}")
        self._wifi_modo = value
        
    @property
    def ssid(self):
        return self._ssid
    
    @ssid.setter
    def ssid(self, value):
        if self._wifi_modo == "ESTACAO" and not value:
            raise ValueError("SSID é obrigatório no modo Estação")
        self._ssid = value
        
    @property
    def senha(self):
        return self._senha
    
    @senha.setter
    def senha(self, value):
        if self._wifi_modo:
            if not value:
                raise ValueError("Senha é obrigatória para configuração WiFi")
            if len(value) < 8:
                raise ValueError("A senha deve ter pelo menos 8 caracteres")
        self._senha = value
        
    def get_bluetooth_config(self):
        if self.proto_com == "bluetooth":
            return self.id_lino
        return None
        
    def get_wifi_config(self):
        if self.proto_com == "wifi":
            config = {
                "mode": "STA_IF" if self.wifi_modo == "ESTACAO" else "AP_IF"
            }
            
            if self.wifi_modo == "ESTACAO":
                config.update({
                    "ssid": self.ssid,
                    "password": self.senha
                })
            else:
                config.update({
                    "ssid": self.id_lino,
                    "password": self.senha
                })
            return config
        return None
        
    def to_dict(self):
        config = {
            "id_lino": self.id_lino,
            "token": self.token,
            "proto_com": self.proto_com
        }
        
        if self.proto_com == "wifi":
            config["wifi"] = self.get_wifi_config()
        elif self.proto_com == "bluetooth":
            config["bluetooth"] = self.get_bluetooth_config()
            
        return config
        
    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
            
    def load(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        except OSError:
            raise ValueError(f"Arquivo de configuração {self.config_file} não encontrado")
            
        required_fields = ["id_lino", "token", "proto_com"]
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Campo obrigatório {field} não encontrado no arquivo de configuração")
                
        self.id_lino = config["id_lino"]
        self.token = config["token"]
        self.proto_com = config["proto_com"]
        
        if "wifi" in config and isinstance(config["wifi"], dict):
            wifi_config = config["wifi"]
            self.wifi_modo = "ESTACAO" if wifi_config["mode"] == "STA_IF" else "PONTO_DE_ACESSO"
            if self.wifi_modo == "ESTACAO":
                self.ssid = wifi_config.get("ssid")
            self.senha = wifi_config.get("password")