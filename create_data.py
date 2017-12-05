from blog import db, Role, User

db.create_all()
admin_role = Role(name='Admin')
mod_role = Role(name='Moderator')
user_role = Role(name='User')
user_LiPing = User(username='LiPing', role=mod_role)
user_LiuPeng = User(username='LiuPeng', role=admin_role)
user_ZhangShan = User(username='ZhangShan', role=user_role)

db.session.add_all([admin_role, mod_role, user_role, user_LiPing, user_LiuPeng, user_ZhangShan])
db.session.commit()

