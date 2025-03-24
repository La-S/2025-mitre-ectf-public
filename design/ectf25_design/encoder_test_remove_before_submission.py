from ectf25.utils import Encoder

encoder = Encoder("""extern char channels[3] = {1,3,4};
extern int secret_key_imported[16] = {184,95,127,183,219,185,122,154,18,84,194,192,8,253,223,63};
// {"channels": [1, 3, 4], "aes_key":"B85F7FB7DBB97A9A1254C2C008FDDF3F"}""")
print(encoder)
# encoded = self.encoder.encode(channel.number, frame, timestamp)
# 81 BA CB 32 84 27 E8 C8 B2 CE 39 38 82 D9 AB CD