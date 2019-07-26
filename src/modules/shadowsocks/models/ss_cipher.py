class SSCipher(object):
    """
    https://shadowsocks.org/en/spec/Stream-Ciphers.html
    """

    aes_128_ctr = 'aes-128-ctr'
    aes_192_ctr = 'aes-192-ctr'
    aes_256_ctr = 'aes-256-ctr'
    aes_128_cfb = 'aes-128-cfb'
    aes_192_cfb = 'aes-192-cfb'
    aes_256_cfb = 'aes-256-cfb'
    camellia_128_cfb = 'camellia-128-cfb'
    camellia_192_cfb = 'camellia-192-cfb'
    camellia_256_cfb = 'camellia-256-cfb'
    chacha20_ietf = 'chacha20-ietf'
    chacha20_ietf_poly1305 = 'chacha20-ietf-poly1305'

    def __init__(self, cipher: str):
        if cipher not in [
            self.aes_128_ctr,
            self.aes_192_ctr,
            self.aes_256_ctr,
            self.aes_128_cfb,
            self.aes_192_cfb,
            self.aes_256_cfb,
            self.camellia_128_cfb,
            self.camellia_192_cfb,
            self.camellia_256_cfb,
            self.chacha20_ietf,
            self.chacha20_ietf_poly1305
        ]:
            raise ValueError('Unknown cipher: {}'.format(str(cipher)))
        self.cipher = cipher
