"""Skill 4: Diet Generator

根據用戶偏好與熱量目標生成個人化每日飲食計畫。
"""

__version__ = "1.0.0"
__all__ = ["generate_diet"]

# 延遲 import 以避免循環依賴問題
def __getattr__(name):
    if name == "generate_diet":
        from .scripts.diet_generator import generate_diet
        return generate_diet
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
