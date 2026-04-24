# 通讯录管理系统
# 功能：添加、查看、搜索、删除联系人，支持数据保存到文件

# 导入os模块，用于处理文件路径
import os

# 定义全局变量，用于存储所有联系人（列表中包含字典）
# 每个联系人字典格式：{"name": "姓名", "phone": "电话", "email": "邮箱"}
contacts = []

def add_contact():
    """添加新联系人"""
    # 获取用户输入的联系人信息
    name = input("请输入联系人姓名：").strip()
    # 简单验证：姓名不能为空
    if not name:
        print("姓名不能为空！")
        return  # 提前结束函数
    
    phone = input("请输入联系电话：").strip()
    if not phone:
        print("电话不能为空！")
        return
    
    email = input("请输入电子邮箱（可选）：").strip()  # 邮箱可选，可为空
    
    # 创建联系人字典
    new_contact = {
        "name": name,
        "phone": phone,
        "email": email
    }
    
    # 将新联系人添加到列表
    contacts.append(new_contact)
    print(f"已添加联系人：{name}（电话：{phone}）")
   

def view_contacts():
    """查看所有联系人"""
    # 判断通讯录是否为空
    if not contacts:
        print("当前通讯录为空！")
        return
    
    # 遍历所有联系人并显示（用enumerate获取编号）
    print("\n===== 所有联系人 =====")
    for index, contact in enumerate(contacts):
        # 格式化显示：编号、姓名、电话、邮箱（邮箱为空时显示"无"）
        print(f"{index + 1}. 姓名：{contact['name']}")
        print(f"   电话：{contact['phone']}")
        print(f"   邮箱：{contact['email'] if contact['email'] else '无'}\n")

def search_contact():
    """搜索联系人（按姓名关键词）"""
    if not contacts:
        print("通讯录为空，无法搜索！")
        return
    
    # 获取用户输入的搜索关键词
    keyword = input("请输入要搜索的姓名关键词：").strip().lower()  # 转小写，支持模糊搜索
    if not keyword:
        print("搜索关键词不能为空！")
        return
    
    # 存储搜索结果
    found = []
    # 遍历所有联系人，判断姓名是否包含关键词（忽略大小写）
    for contact in contacts:
        if keyword in contact['name'].lower():
            found.append(contact)
    
    # 显示搜索结果
    if found:
        print(f"\n找到 {len(found)} 个匹配结果：")
        for i, contact in enumerate(found):
            print(f"{i + 1}. 姓名：{contact['name']}，电话：{contact['phone']}")
    else:
        print(f"未找到包含 '{keyword}' 的联系人")

def delete_contact():
    """删除联系人"""
    # 先显示所有联系人，方便用户选择要删除的编号
    view_contacts()
    if not contacts:
        return  # 通讯录为空，直接返回
    
    try:
        # 获取用户输入的编号（转整数后减1，适配列表索引）
        num = int(input("请输入要删除的联系人编号：")) - 1
        # 验证编号是否有效（0 <= num < 列表长度）
        if 0 <= num < len(contacts):
            # 用pop删除并获取被删除的联系人
            deleted = contacts.pop(num)
            print(f"已删除联系人：{deleted['name']}")
        else:
            print("输入的编号无效！")
    except ValueError:
        # 处理用户输入非数字的情况
        print("请输入有效的数字！")

def save_contacts():
    """将通讯录保存到文件（与代码同目录的contacts.txt）"""
    # 获取代码文件所在目录
    code_dir = os.path.dirname(__file__)
    # 拼接保存文件的完整路径
    file_path = os.path.join(code_dir, "contacts.txt")
    
    # 用with语句打开文件（写入模式），自动处理关闭
    with open(file_path, "w", encoding="utf-8") as f:
        # 遍历所有联系人，按固定格式写入文件
        for contact in contacts:
            # 格式：姓名|电话|邮箱（用|分隔，方便读取时拆分）
            f.write(f"{contact['name']}|{contact['phone']}|{contact['email']}\n")
    
    print(f"通讯录已保存到：{file_path}")

def load_contacts():
    """从文件加载通讯录（程序启动时调用）"""
    # 清空现有通讯录（避免重复加载）
    contacts.clear()
    
    # 获取文件路径（与保存时一致）
    code_dir = os.path.dirname(__file__)
    file_path = os.path.join(code_dir, "contacts.txt")
    
    try:
        # 尝试打开文件（读取模式）
        with open(file_path, "r", encoding="utf-8") as f:
            # 逐行读取文件内容
            for line in f:
                line = line.strip()  # 去除换行符和空格
                if line:  # 跳过空行
                    # 按|拆分数据（最多拆分2次，确保正确获取3个字段）
                    parts = line.split("|", 2)
                    # 确保拆分后有3个部分（姓名、电话、邮箱）
                    if len(parts) == 3:
                        name, phone, email = parts
                        # 添加到通讯录列表
                        contacts.append({
                            "name": name,
                            "phone": phone,
                            "email": email
                        })
        print(f"已从文件加载 {len(contacts)} 个联系人")
    except FileNotFoundError:
        # 如果文件不存在，创建一个空文件（避免后续保存出错）
        with open(file_path, "w", encoding="utf-8") as f:
            pass  # 空操作，仅创建文件
        print("首次使用，已创建通讯录文件")
    except Exception as e:
        # 捕获其他可能的错误（如文件格式错误）
        print(f"加载通讯录出错：{e}")

def main():
    """主函数：显示菜单，处理用户选择"""
    # 程序启动时先加载已保存的通讯录
    load_contacts()
    
    # 无限循环，让程序持续运行,直到用户选择退出
    while True:
        # 显示菜单
        print("\n===== 通讯录管理系统 =====")
        print("1. 添加联系人")
        print("2. 查看所有联系人")
        print("3. 搜索联系人")
        print("4. 删除联系人")
        print("5. 保存通讯录")
        print("6. 退出")
        
        # 获取用户选择
        choice = input("请输入操作编号（1-6）：").strip()#.strip()去掉多余空格
        
        # 根据用户选择调用对应函数
        if choice == "1":
            add_contact()
             #  添加后自动保存
            save_contacts()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            save_contacts()
        elif choice == "6":
            # 退出前保存通讯录
            save_contacts()
            print("谢谢使用，再见！")
            break  # 跳出循环，结束程序
        else:
            print("请输入1-6之间的有效编号！")

# 当程序直接运行时，执行主函数
if __name__ == "__main__":
    main()
    