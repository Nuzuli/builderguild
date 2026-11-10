class TmuxError(Exception):
    """Perintah tmux gagal dijalankan."""


class TmuxNotAvailableError(TmuxError):
    """tmux belum terinstall."""


class GraphError(Exception):
    """Operasi pada fact graph gagal."""