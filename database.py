import sqlite3

DB_NAME = 'database/medcontrol.db'

PLANOS = [
    'bradesco', 'banco central', 'saude caixa', 'casf', 'cassi',
    'proasa', 'casembrapa', 'anpa', 'particular', 'petrobras petroleo',
    'aspara', 'trt', 'sepaco', 'unb', 'faama', 'embratel', 'telos',
    'ministerio publico federal', 'iagp',
    'instituicao adventista de educacao -mpa',
    'pame', 'gs garantia de saude (proasa/pa)', 'asfhab', 'padf',
    'vale', 'servico social', 'postal saude', 'gs desconto',
    'ministerio publico militar', 'ministerio publico do trabalho',
    'sesmt', 'sulamerica', 'mpa - missao para amapa', 'aspa',
    'ranpa', 'mopa missao oeste do para',
    'uniao noroeste brasileira unob',
    'entidades unb - projeto 30', 'operadora de planos',
    'omint', 'pro social'
]


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            convenio TEXT,
            paciente TEXT,
            tipo TEXT,
            valor REAL,
            data TEXT,
            status TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            convenio TEXT,
            paciente TEXT,
            valor REAL,
            data TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sobreavisos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hospital TEXT,
            horas INTEGER,
            valor REAL,
            data TEXT,
            status TEXT
        )
    ''')

    conn.commit()
    conn.close()