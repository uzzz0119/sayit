"""
用户模型
"""
import json
import os
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import Config


class User(UserMixin):
    """用户类"""
    
    def __init__(self, username, password_hash=None, user_id=None):
        self.username = username
        self.password_hash = password_hash
        self.id = user_id or username
    
    def set_password(self, password):
        """设置密码（加密存储）"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'id': self.id
        }
    
    @staticmethod
    def get_users_file():
        """获取用户数据文件路径"""
        return os.path.join(Config.BASE_DIR, 'users.json')
    
    @staticmethod
    def load_users():
        """从文件加载所有用户"""
        users_file = User.get_users_file()
        if not os.path.exists(users_file):
            return {}
        
        try:
            with open(users_file, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
                return {
                    username: User(
                        username=data['username'],
                        password_hash=data['password_hash'],
                        user_id=data.get('id', username)
                    )
                    for username, data in users_data.items()
                }
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}
    
    @staticmethod
    def save_users(users_dict):
        """保存所有用户到文件"""
        users_file = User.get_users_file()
        try:
            users_data = {
                username: user.to_dict()
                for username, user in users_dict.items()
            }
            with open(users_file, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    @staticmethod
    def get_by_username(username):
        """根据用户名获取用户"""
        users = User.load_users()
        return users.get(username)
    
    @staticmethod
    def get_by_id(user_id):
        """根据用户ID获取用户"""
        users = User.load_users()
        return users.get(user_id)
    
    @staticmethod
    def create_user(username, password):
        """创建新用户"""
        users = User.load_users()
        
        # 检查用户是否已存在
        if username in users:
            return None, "用户名已存在"
        
        # 创建新用户
        new_user = User(username=username)
        new_user.set_password(password)
        
        # 保存到用户字典
        users[username] = new_user
        
        # 持久化到文件
        if User.save_users(users):
            return new_user, None
        else:
            return None, "保存用户失败"
    
    @staticmethod
    def initialize_default_user():
        """初始化默认管理员用户"""
        users = User.load_users()
        
        # 如果没有用户，创建默认管理员
        if not users:
            admin_user = User(username='admin')
            admin_user.set_password('admin123')  # 默认密码
            users['admin'] = admin_user
            User.save_users(users)
            print("✅ Created default admin user (username: admin, password: admin123)")
            print("⚠️  Please change the password after first login!")
        
        return users

