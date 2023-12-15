from dotenv import load_dotenv
import uuid
import os

def find_dotenv():
    path = os.path.dirname(os.path.abspath(__file__))  # 当前脚本的目录
    root_path = os.path.abspath(os.sep)  # 文件系统的根目录（比如 '/' 或 'C:\\'）

    # 向上遍历直到根目录
    while path != root_path:
        if os.path.exists(os.path.join(path, '.env')):
            env_path = os.path.join(path, '.env')
            return load_dotenv(env_path)
        path = os.path.dirname(path)  # 向上一级目录

    # 如果没有找到 .env 文件，返回 None
    return '.env file is not found'



def generate_uuid():
    return str(uuid.uuid4())

