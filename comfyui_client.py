"""
ComfyUI API 客户端
用于与 ComfyUI 服务通信，生成贪吃蛇游戏皮肤
"""

import requests
import uuid
import time
import json
import os
from typing import Optional, Dict, Any, Tuple
from datetime import datetime


class ComfyUIClient:
    """ComfyUI API 客户端"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8188"):
        """
        初始化 ComfyUI 客户端
        
        Args:
            base_url: ComfyUI 服务地址
        """
        self.base_url = base_url
        self.client_id = str(uuid.uuid4())
        self.timeout = 60  # 默认超时时间
        
    def submit_prompt(self, prompt: str,
                     width: int = 512,
                     height: int = 512,
                     steps: int = 20,
                     cfg: float = 7.0,
                     seed: int = -1) -> str:
        """
        提交生成任务到 ComfyUI
        
        Args:
            prompt: 提示词文本
            width: 图片宽度
            height: 图片高度
            steps: 采样步数
            cfg: CFG 值
            seed: 随机种子（-1 表示随机）
            
        Returns:
            prompt_id: 任务ID
            
        Raises:
            requests.RequestException: 请求失败
        """
        # 构建 ComfyUI 工作流
        workflow = self._build_workflow(
            prompt=prompt,
            width=width,
            height=height,
            steps=steps,
            cfg=cfg,
            seed=seed if seed != -1 else int(time.time() * 1000) % 2147483647
        )
        
        # 发送请求
        try:
            response = requests.post(
                f"{self.base_url}/prompt",
                json={
                    "prompt": workflow,
                    "client_id": self.client_id
                },
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data.get("prompt_id")
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] 提交 ComfyUI 任务失败: {e}")
            raise
    
    def get_status(self, prompt_id: str) -> Dict[str, Any]:
        """
        获取生成状态
        
        Args:
            prompt_id: 任务ID
            
        Returns:
            状态信息字典
            
        Raises:
            requests.RequestException: 请求失败
        """
        try:
            response = requests.get(
                f"{self.base_url}/history/{prompt_id}",
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] 获取 ComfyUI 状态失败: {e}")
            raise
    
    def download_image(self, filename: str,
                      subfolder: str = "",
                      image_type: str = "output") -> bytes:
        """
        下载生成的图片
        
        Args:
            filename: 文件名
            subfolder: 子文件夹
            image_type: 图片类型
            
        Returns:
            图片二进制数据
            
        Raises:
            requests.RequestException: 请求失败
        """
        try:
            params = {
                "filename": filename,
                "subfolder": subfolder,
                "type": image_type
            }
            
            response = requests.get(
                f"{self.base_url}/view",
                params=params,
                timeout=30
            )
            
            response.raise_for_status()
            return response.content
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] 下载 ComfyUI 图片失败: {e}")
            raise
    
    def get_queue_info(self) -> Dict[str, Any]:
        """
        获取队列信息
        
        Returns:
            队列信息字典
            
        Raises:
            requests.RequestException: 请求失败
        """
        try:
            response = requests.get(
                f"{self.base_url}/queue",
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] 获取 ComfyUI 队列信息失败: {e}")
            raise
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        获取系统状态
        
        Returns:
            系统状态字典
            
        Raises:
            requests.RequestException: 请求失败
        """
        try:
            response = requests.get(
                f"{self.base_url}/system_stats",
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] 获取 ComfyUI 系统状态失败: {e}")
            raise
    
    def check_health(self) -> bool:
        """
        检查 ComfyUI 服务是否健康
        
        Returns:
            True 表示服务正常，False 表示服务异常
        """
        try:
            self.get_system_stats()
            return True
        except Exception:
            return False
    
    def _build_workflow(self, prompt: str,
                        width: int,
                        height: int,
                        steps: int,
                        cfg: float,
                        seed: int) -> Dict:
        """
        构建 ComfyUI 工作流
        
        Args:
            prompt: 提示词
            width: 图片宽度
            height: 图片高度
            steps: 采样步数
            cfg: CFG 值
            seed: 随机种子
            
        Returns:
            工作流字典
        """
        # 节点ID配置（使用 Stable Diffusion 1.5）
        clip_node = "3"
        clip_model = "4"
        positive = "6"
        negative = "7"
        empty_latent = "5"
        ksampler = "10"
        vae = "8"
        vae_decode = "9"
        save_image = "11"
        
        # 构建工作流
        workflow = {
            clip_node: {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": "v1-5-pruned-emaonly.ckpt"
                }
            },
            clip_model: {
                "class_type": "CLIPLoader",
                "inputs": {
                    "clip_name": "clip-vit-base-patch32"
                }
            },
            positive: {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": prompt,
                    "clip": [clip_model, 0]
                }
            },
            negative: {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": "low quality, blurry, distorted, ugly, bad anatomy, "
                           "bad composition, watermark, text, logo",
                    "clip": [clip_model, 0]
                }
            },
            empty_latent: {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": 1
                }
            },
            ksampler: {
                "class_type": "KSampler",
                "inputs": {
                    "seed": seed,
                    "steps": steps,
                    "cfg": cfg,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1,
                    "model": [clip_node, 0],
                    "positive": [positive, 0],
                    "negative": [negative, 0],
                    "latent_image": [empty_latent, 0]
                }
            },
            vae: {
                "class_type": "VAELoader",
                "inputs": {
                    "vae_name": "vae-ft-mse-840000-ema-pruned.safetensors"
                }
            },
            vae_decode: {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": [ksampler, 0],
                    "vae": [vae, 0]
                }
            },
            save_image: {
                "class_type": "SaveImage",
                "inputs": {
                    "images": [vae_decode, 0],
                    "filename_prefix": f"snake_skin_{int(time.time())}"
                }
            }
        }
        
        return workflow


class SkinGenerator:
    """皮肤生成器（集成 Flask 应用）"""
    
    def __init__(self, comfyui_url: str = None, storage_path: str = "data/skins"):
        """
        初始化皮肤生成器
        
        Args:
            comfyui_url: ComfyUI 服务地址
            storage_path: 皮肤存储路径
        """
        self.comfyui_url = comfyui_url or os.getenv("COMFYUI_URL", "http://127.0.0.1:8188")
        self.client = ComfyUIClient(self.comfyui_url)
        self.storage_path = storage_path
        
        # 创建存储目录
        os.makedirs(self.storage_path, exist_ok=True)
        
        # 任务存储（生产环境应使用 Redis）
        self.tasks: Dict[str, Dict[str, Any]] = {}
    
    def generate_skin(self, prompt: str,
                      player_id: str,
                      style: str = "cartoon",
                      width: int = 512,
                      height: int = 512) -> Tuple[bool, str, str]:
        """
        生成游戏皮肤
        
        Args:
            prompt: 提示词
            player_id: 玩家ID
            style: 风格
            width: 图片宽度
            height: 图片高度
            
        Returns:
            (success, task_id, message)
        """
        # 验证 prompt
        if not prompt or len(prompt.strip()) == 0:
            return False, "", "prompt 不能为空"
        
        if len(prompt) > 500:
            return False, "", "prompt 长度不能超过500字符"
        
        # 生成任务ID
        task_id = f"task_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        try:
            # 检查 ComfyUI 服务
            if not self.client.check_health():
                return False, "", "ComfyUI 服务不可用"
            
            # 提交任务到 ComfyUI
            prompt_id = self.client.submit_prompt(
                prompt=prompt,
                width=width,
                height=height
            )
            
            # 保存任务信息
            self.tasks[task_id] = {
                "task_id": task_id,
                "prompt_id": prompt_id,
                "prompt": prompt,
                "player_id": player_id,
                "style": style,
                "width": width,
                "height": height,
                "status": "pending",
                "created_at": datetime.utcnow().isoformat(),
                "image_url": None
            }
            
            return True, task_id, "皮肤生成任务已提交"
            
        except Exception as e:
            print(f"[ERROR] 生成皮肤失败: {e}")
            return False, "", f"生成失败: {str(e)}"
    
    def get_skin_status(self, task_id: str) -> Dict[str, Any]:
        """
        获取皮肤生成状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            状态信息字典
        """
        if task_id not in self.tasks:
            return {
                "success": False,
                "status": "not_found",
                "message": "任务不存在"
            }
        
        task = self.tasks[task_id]
        
        try:
            # 查询 ComfyUI 状态
            status = self.client.get_status(task["prompt_id"])
            
            # 检查是否完成
            if task["status"] in ["pending", "processing"]:
                outputs = status.get(task["prompt_id"], {}).get("outputs", {})
                
                if outputs:
                    # 生成完成
                    node_id = list(outputs.keys())[0]
                    images = outputs[node_id].get("images", [])
                    
                    if images:
                        image_info = images[0]
                        filename = image_info["filename"]
                        
                        # 下载图片
                        image_data = self.client.download_image(filename)
                        
                        # 保存图片
                        skin_filename = f"{task_id}.png"
                        skin_path = os.path.join(self.storage_path, skin_filename)
                        
                        with open(skin_path, "wb") as f:
                            f.write(image_data)
                        
                        # 更新任务状态
                        task["status"] = "completed"
                        task["image_url"] = f"/api/skin/image/{skin_filename}"
                        task["filename"] = filename
                        task["completed_at"] = datetime.utcnow().isoformat()
                        
                        return {
                            "success": True,
                            "task_id": task_id,
                            "status": "completed",
                            "image_url": task["image_url"],
                            "progress": 100,
                            "message": "生成完成"
                        }
                
                # 仍在处理中
                task["status"] = "processing"
                
                # 估算进度（简单估算）
                progress = min(90, task.get("progress", 0) + 10)
                task["progress"] = progress
                
                return {
                    "success": True,
                    "task_id": task_id,
                    "status": "processing",
                    "progress": progress,
                    "message": "生成中..."
                }
            
            # 已完成
            if task["status"] == "completed":
                return {
                    "success": True,
                    "task_id": task_id,
                    "status": "completed",
                    "image_url": task["image_url"],
                    "progress": 100,
                    "message": "生成完成"
                }
            
            # 失败
            return {
                "success": False,
                "task_id": task_id,
                "status": "failed",
                "message": "生成失败"
            }
            
        except Exception as e:
            print(f"[ERROR] 获取状态失败: {e}")
            task["status"] = "failed"
            return {
                "success": False,
                "task_id": task_id,
                "status": "failed",
                "message": f"获取状态失败: {str(e)}"
            }
    
    def get_skin_history(self, player_id: str, 
                         page: int = 1,
                         limit: int = 10) -> Dict[str, Any]:
        """
        获取玩家的皮肤生成历史
        
        Args:
            player_id: 玩家ID
            page: 页码
            limit: 每页数量
            
        Returns:
            历史记录字典
        """
        # 过滤该玩家的所有任务
        player_tasks = [
            task for task in self.tasks.values()
            if task["player_id"] == player_id and task["status"] == "completed"
        ]
        
        # 按时间倒序排序
        player_tasks.sort(key=lambda x: x["created_at"], reverse=True)
        
        # 分页
        total = len(player_tasks)
        start = (page - 1) * limit
        end = start + limit
        page_tasks = player_tasks[start:end]
        
        return {
            "success": True,
            "total": total,
            "page": page,
            "limit": limit,
            "skins": page_tasks
        }
    
    def get_skin_image(self, filename: str) -> Optional[Tuple[str, bytes]]:
        """
        获取皮肤图片
        
        Args:
            filename: 文件名
            
        Returns:
            (content_type, image_data) 或 None
        """
        filepath = os.path.join(self.storage_path, filename)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, "rb") as f:
                image_data = f.read()
            
            return ("image/png", image_data)
            
        except Exception as e:
            print(f"[ERROR] 读取图片失败: {e}")
            return None


# 模拟模式（用于测试，无需 ComfyUI 服务）
class MockSkinGenerator:
    """模拟皮肤生成器（用于测试）"""

    def __init__(self):
        self.tasks = {}
        self.mock_images = [
            "/api/skin/image/mock_skin_1.png",
            "/api/skin/image/mock_skin_2.png",
            "/api/skin/image/mock_skin_3.png"
        ]
        self.mock_index = 0
    
    def generate_skin(self, prompt: str,
                      player_id: str,
                      style: str = "cartoon",
                      width: int = 512,
                      height: int = 512) -> Tuple[bool, str, str]:
        """模拟生成皮肤"""
        task_id = f"mock_task_{int(time.time())}"
        
        self.tasks[task_id] = {
            "task_id": task_id,
            "prompt": prompt,
            "player_id": player_id,
            "style": style,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        
        return True, task_id, "皮肤生成任务已提交（模拟模式）"
    
    def get_skin_status(self, task_id: str) -> Dict[str, Any]:
        """模拟获取状态"""
        if task_id not in self.tasks:
            return {
                "success": False,
                "status": "not_found",
                "message": "任务不存在"
            }
        
        task = self.tasks[task_id]
        
        if task["status"] == "pending":
            task["status"] = "processing"
            task["progress"] = 50
            return {
                "success": True,
                "task_id": task_id,
                "status": "processing",
                "progress": 50,
                "message": "生成中..."
            }
        
        if task["status"] == "processing":
            # 模拟图片 URL
            mock_url = self.mock_images[self.mock_index % len(self.mock_images)]
            self.mock_index += 1
            
            task["status"] = "completed"
            task["progress"] = 100
            task["image_url"] = mock_url
            
            return {
                "success": True,
                "task_id": task_id,
                "status": "completed",
                "image_url": mock_url,
                "progress": 100,
                "message": "生成完成"
            }
        
        if task["status"] == "completed":
            return {
                "success": True,
                "task_id": task_id,
                "status": "completed",
                "image_url": task["image_url"],
                "progress": 100,
                "message": "生成完成"
            }
        
        return {
            "success": False,
            "task_id": task_id,
            "status": "failed",
            "message": "生成失败"
        }
    
    def get_skin_history(self, player_id: str,
                         page: int = 1,
                         limit: int = 10) -> Dict[str, Any]:
        """模拟获取历史"""
        return {
            "success": True,
            "total": 0,
            "page": page,
            "limit": limit,
            "skins": []
        }
