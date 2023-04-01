from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")

START_FILE_ID = env.str("START_FILE_ID")

ADMINS = [813415126, 5773913054]
