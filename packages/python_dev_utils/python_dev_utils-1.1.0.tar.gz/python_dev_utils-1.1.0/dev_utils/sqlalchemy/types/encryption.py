from sqlalchemy import String, TypeDecorator, func, type_coerce


class PGPString(TypeDecorator[str]):
    impl = String

    cache_ok = True

    def __init__(self, passphrase: str):
        super().__init__()
        self.passphrase = passphrase

    def bind_expression(self, bindvalue):
        # convert the bind's type from PGPString to
        # String, so that it's passed to psycopg2 as is without
        # a dbapi.Binary wrapper
        bindvalue = type_coerce(bindvalue, String)
        return func.pgp_sym_encrypt(bindvalue, self.passphrase)

    def column_expression(self, col):
        return func.pgp_sym_decrypt(col, self.passphrase)
