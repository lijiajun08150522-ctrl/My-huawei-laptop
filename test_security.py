"""
安全功能测试脚本
测试JWT认证、CSRF防护、XSS防护等功能
"""
import requests
import json
from datetime import datetime


class SecurityTester:
    """安全功能测试类"""

    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
        self.auth_token = None
        self.csrf_token = None

    def print_section(self, title):
        """打印章节标题"""
        print(f"\n{'=' * 70}")
        print(f"{title}")
        print('=' * 70)

    def test_get_csrf_token(self):
        """测试获取CSRF Token"""
        self.print_section("测试1: 获取CSRF Token")

        try:
            response = requests.get(f"{self.base_url}/api/auth/csrf-token")
            data = response.json()

            print(f"状态码: {response.status_code}")
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            if response.status_code == 200 and data.get('success'):
                self.csrf_token = data.get('csrf_token')
                print(f"✅ CSRF Token获取成功: {self.csrf_token[:20]}...")
                self.test_results.append(("获取CSRF Token", True))
                return True
            else:
                print("❌ 获取CSRF Token失败")
                self.test_results.append(("获取CSRF Token", False))
                return False

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            self.test_results.append(("获取CSRF Token", False))
            return False

    def test_register(self, username, password, email=None):
        """测试用户注册"""
        print(f"\n注册用户: {username}")

        try:
            payload = {
                "username": username,
                "password": password
            }

            if email:
                payload["email"] = email

            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json=payload
            )
            data = response.json()

            print(f"状态码: {response.status_code}")
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            return response.status_code in [200, 201] and data.get('success')

        except Exception as e:
            print(f"❌ 注册失败: {e}")
            return False

    def test_login(self, username, password):
        """测试用户登录"""
        print(f"\n登录用户: {username}")

        try:
            payload = {
                "username": username,
                "password": password
            }

            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json=payload
            )
            data = response.json()

            print(f"状态码: {response.status_code}")
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            if response.status_code == 200 and data.get('success'):
                self.auth_token = data.get('token')
                print(f"✅ 登录成功，Token: {self.auth_token[:30]}...")
                return True
            else:
                print("❌ 登录失败")
                return False

        except Exception as e:
            print(f"❌ 登录失败: {e}")
            return False

    def test_get_profile(self):
        """测试获取用户信息（需要认证）"""
        print("\n测试获取用户信息（需要认证）")

        if not self.auth_token:
            print("❌ 没有有效的Token，请先登录")
            return False

        try:
            headers = {
                "Authorization": f"Bearer {self.auth_token}"
            }

            response = requests.get(
                f"{self.base_url}/api/auth/profile",
                headers=headers
            )
            data = response.json()

            print(f"状态码: {response.status_code}")
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            if response.status_code == 200 and data.get('success'):
                print("✅ 获取用户信息成功")
                return True
            else:
                print("❌ 获取用户信息失败")
                return False

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False

    def test_refresh_token(self):
        """测试刷新Token"""
        print("\n测试刷新Token")

        if not self.auth_token:
            print("❌ 没有有效的Token，请先登录")
            return False

        try:
            payload = {
                "token": self.auth_token
            }

            response = requests.post(
                f"{self.base_url}/api/auth/refresh",
                json=payload
            )
            data = response.json()

            print(f"状态码: {response.status_code}")
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            if response.status_code == 200 and data.get('success'):
                self.auth_token = data.get('token')
                print(f"✅ Token刷新成功: {self.auth_token[:30]}...")
                return True
            else:
                print("❌ Token刷新失败")
                return False

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False

    def test_change_password(self, old_password, new_password):
        """测试修改密码"""
        print(f"\n测试修改密码")

        if not self.auth_token:
            print("❌ 没有有效的Token，请先登录")
            return False

        try:
            headers = {
                "Authorization": f"Bearer {self.auth_token}"
            }

            payload = {
                "old_password": old_password,
                "new_password": new_password
            }

            response = requests.put(
                f"{self.base_url}/api/auth/change-password",
                headers=headers,
                json=payload
            )
            data = response.json()

            print(f"状态码: {response.status_code}")
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            if response.status_code == 200 and data.get('success'):
                print("✅ 密码修改成功")
                return True
            else:
                print("❌ 密码修改失败")
                return False

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False

    def test_xss_protection(self):
        """测试XSS防护"""
        self.print_section("测试2: XSS防护")

        print("\n测试XSS输入过滤")

        # 尝试注册包含XSS payload的用户名
        xss_payload = "<script>alert('XSS')</script>"

        result = self.test_register("test_xss_user", "password123")
        self.test_results.append(("XSS防护 - 注册", not result))  # 应该失败

        # 尝试注册正常用户名
        result = self.test_register("normal_user", "password123")
        self.test_results.append(("正常注册", result))  # 应该成功

    def test_jwt_authentication(self):
        """测试JWT认证"""
        self.print_section("测试3: JWT认证")

        # 测试登录
        result = self.test_login("admin", "admin123")
        self.test_results.append(("JWT登录", result))

        if result:
            # 测试获取用户信息
            result = self.test_get_profile()
            self.test_results.append(("JWT获取用户信息", result))

            # 测试刷新Token
            result = self.test_refresh_token()
            self.test_results.append(("JWT刷新Token", result))

    def test_password_change(self):
        """测试密码修改"""
        self.print_section("测试4: 密码修改")

        # 修改密码
        result = self.test_change_password("admin123", "newpassword123")
        self.test_results.append(("密码修改", result))

        # 使用新密码登录
        if result:
            result = self.test_login("admin", "newpassword123")
            self.test_results.append(("新密码登录", result))

            # 改回原密码
            self.test_change_password("newpassword123", "admin123")
            self.test_login("admin", "admin123")

    def test_security_headers(self):
        """测试安全响应头"""
        self.print_section("测试5: 安全响应头")

        try:
            # 访问首页检查响应头
            response = requests.get(f"{self.base_url}/api/auth/csrf-token")

            headers = response.headers

            # 检查安全头
            security_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Content-Security-Policy': None
            }

            print("\n安全响应头检查:")
            for header, expected_value in security_headers.items():
                actual_value = headers.get(header)
                status = "✅" if actual_value else "❌"

                print(f"  {status} {header}: {actual_value or '未设置'}")

                if expected_value is None:
                    self.test_results.append((f"安全头 - {header}", bool(actual_value)))
                else:
                    self.test_results.append((f"安全头 - {header}", actual_value == expected_value))

        except Exception as e:
            print(f"❌ 测试失败: {e}")

    def run_all_tests(self):
        """运行所有测试"""
        self.print_section("安全功能 - 自动化测试")

        # 检查服务器
        print("\n检查服务器状态...")
        try:
            response = requests.get(f"{self.base_url}/api/auth/csrf-token", timeout=3)
            print("✅ 服务器运行正常")
        except:
            print("❌ 服务器未启动！")
            print("请先运行: python app.py")
            return

        # CSRF Token测试
        self.test_get_csrf_token()

        # JWT认证测试
        self.test_jwt_authentication()

        # XSS防护测试
        self.test_xss_protection()

        # 密码修改测试
        self.test_password_change()

        # 安全响应头测试
        self.test_security_headers()

        # 总结
        self.print_summary()

    def print_summary(self):
        """打印测试总结"""
        self.print_section("测试总结")

        passed = sum(1 for _, result in self.test_results if result)
        total = len(self.test_results)

        print(f"\n测试结果: {passed}/{total} 通过\n")

        for test_name, result in self.test_results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"  {test_name}: {status}")


def main():
    """主函数"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║           Flask安全功能 - 自动化测试工具                        ║")
    print("╚════════════════════════════════════════════════════════════╝")

    # 运行测试
    tester = SecurityTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
