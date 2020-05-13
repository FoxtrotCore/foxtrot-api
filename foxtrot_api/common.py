import os.path
home_dir = os.path.expanduser('/opt/foxtrot-api/')
cache_dir = home_dir + 'cache/'
secrets_dir = home_dir + '.secrets/'
tokens_path = home_dir + 'api_tokens.json'
config_path = home_dir + 'config.json'
db_path = home_dir + 'user_agents.db'
admin_token_path = secrets_dir + 'admin_token.json'
secret_path = secrets_dir + 'secret.json'
