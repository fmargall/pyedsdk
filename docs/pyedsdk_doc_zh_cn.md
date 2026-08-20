# pyedsdk — Python 版佳能 EDSDK 封装库

pyedsdk 是佳能 EDSDK（EOS Digital Software Development Kit）的 Python 绑定，让你可以用 Python 直接控制佳能 EOS 系列数码相机。

## 安装

```bash
pip install pyedsdk
```

## 前置要求

### Windows

1. 从佳能官网申请并下载 EDSDK 开发包。
2. 将 `EDSDK.dll`（64位版位于 `EDSDK_64/Dll/` 目录）放到以下任一位置：
   - `C:\Windows\System32`
   - 项目当前工作目录
   - 通过环境变量 `EDSDK_PATH` 指定的路径
3. 库加载时会自动在上述位置搜索 `EDSDK.dll`。

### macOS / Linux

目前 `pyedsdk` **仅支持 Windows**。macOS 和 Linux 的适配尚未完成，欢迎贡献。

## 快速开始

```python
from pyedsdk.camera import EOSCamera

# 初始化第一台相机
camera = EOSCamera(0)

# 查看当前快门速度
print(camera.shutterSpeed)

# 设定快门速度为 1/125 秒
camera.shutterSpeed = 1/125

# 设定光圈 f/8
camera.aperture = 8.0

# 设定 ISO 400
camera.isoSpeed = 400

# 拍摄一张照片（保存为当前工作目录下的 image.RAW）
camera.shot()

# 拍摄并指定文件名
camera.shot("my_photo.RAW")

# 关闭相机会话（也可用 with 语句自动管理）
camera._close()
```

使用 `with` 语句自动管理资源：

```python
with EOSCamera(0) as camera:
    camera.shot("photo.RAW")
```

## 核心 API

### EOSCamera

`EOSCamera(cameraIndex)` — 连接到指定索引的相机。

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `shutterSpeed` | `float` | 快门速度（秒）。可读可写。 |
| `aperture` | `float` | 光圈 f 值。可读可写。 |
| `isoSpeed` | `float` | ISO 感光度。可读可写。 |
| `mirrorLockUp` | `bool` | 反光镜预升状态。可读可写。 |
| `afMode` | `str` | 当前自动对焦模式（只读）。 |
| `filename` | `str` | 下次拍摄时的默认文件名。可读可写。 |

**注意**：设置 `shutterSpeed`、`aperture`、`isoSpeed` 时，库会自动将你的输入值匹配到相机支持的最接近的离散值。

#### 方法

**`shot(filename: str = None) -> None`**

触发快门拍摄。如果指定 `filename`，会覆盖默认文件名。拍摄完成后图片会保存到当前工作目录。

**`liveViewStream(callback=None, errorCallback=None) -> LiveViewStream`**

启动实时取景流。返回 `LiveViewStream` 对象。

#### 可用值查询

```python
camera = EOSCamera(0)

# 获取相机支持的所有光圈值列表
print(camera.getAvailableApertures())

# 直接读取属性时会自动匹配到最接近的可用值
camera.aperture = 2.8  # 自动匹配到最近的可用光圈
```

### LiveViewStream

`EOSCamera.liveViewStream()` 返回的对象，用于处理实时取景画面。

#### 使用方法

**方式一：回调模式**

```python
def on_frame(frame_bytes):
    # frame_bytes 是 JPEG 格式的图片数据
    with open("frame.jpg", "wb") as f:
        f.write(frame_bytes)

def on_error(err):
    print("Live view error:", err)

stream = camera.liveViewStream(callback=on_frame, errorCallback=on_error)

# ... 稍后停止
stream.stop()
```

**方式二：迭代器模式**

```python
stream = camera.liveViewStream()
for frame in stream:
    # 处理每一帧
    process_frame(frame)
    if some_condition:
        break
# 退出循环后流会自动停止
```

**方式三：手动获取单帧**

```python
stream = camera.liveViewStream()
stream.start()  # 手动启动

try:
    frame = stream.getFrame()
    save_frame(frame)
finally:
    stream.stop()
```

### SyncCameraGroup

同步多台相机，适用于阵列拍摄。

```python
from pyedsdk.sync_camera_group import SyncCameraGroup

# 连接索引为 0 和 1 的两台相机
group = SyncCameraGroup([0, 1])

# 同时设置两台相机的相同参数
group.aperture = 5.6
group.shutterSpeed = 1/200

# 分别控制单台相机
group[0].isoSpeed = 100
group[1].isoSpeed = 400

# 同步拍摄
group.fireShot(["cam0.RAW", "cam1.RAW"])
```

## 错误处理

所有 EDSDK 底层错误都会抛出 `CanonError` 异常：

```python
from pyedsdk.core._errors import CanonError

try:
    camera.shot()
except CanonError as e:
    print(f"Error code: {e.code}")
    print(f"Error name: {e.name}")
    print(f"Message: {e.message}")
```

常见错误码：

| 错误码 | 说明 |
|--------|------|
| `ERR_DEVICE_NOT_FOUND` | 未找到相机 |
| `ERR_DEVICE_BUSY` | 相机正忙 |
| `ERR_TAKE_PICTURE_AF_NG` | 自动对焦失败 |
| `ERR_OBJECT_NOTREADY` | 实时取景画面尚未就绪 |

## 注意事项

1. **始终关闭相机会话**：使用 `with` 语句或手动调用 `_close()` 释放资源。
2. **实时取景性能**：单帧下载耗时约 2-3 秒，帧率较低。
3. **镜像锁**：启用 `mirrorLockUp` 后需要额外的快门命令流程，`shot()` 方法已内置支持。
4. **文件格式**：默认保存为 RAW（.RAW），如需其他格式需要自行扩展 `_ImageQuality`。

## 完整示例

```python
from pyedsdk.camera import EOSCamera
from pyedsdk.core._errors import CanonError
import time

def main():
    try:
        with EOSCamera(0) as cam:
            print(f"AF Mode: {cam.afMode}")
            print(f"Initial ISO: {cam.isoSpeed}")

            # 设置参数
            cam.shutterSpeed = 1/60
            cam.aperture = 5.6
            cam.isoSpeed = 800

            # 定义实时取景回调
            frame_count = 0
            def save_frame(data):
                nonlocal frame_count
                with open(f"lv_frame_{frame_count:03d}.jpg", "wb") as f:
                    f.write(data)
                frame_count += 1

            # 启动实时取景，获取 10 帧
            stream = cam.liveViewStream(callback=save_frame)
            time.sleep(3)  # 等待 3 秒，让回调抓取几帧
            stream.stop()

            # 最终拍摄
            cam.shot("final.RAW")
            print("Done!")

    except CanonError as e:
        print(f"Camera error: {e}")

if __name__ == "__main__":
    main()
```

## 后续开发计划

- [ ] macOS 平台支持
- [ ] Linux 平台支持
- [ ] 更多图像格式支持（JPEG、HEIF）
- [ ] 更完善的属性描述
- [ ] 异步 API

## 许可

本项目采用 Apache License 2.0 许可。EDSDK 本身遵循佳能公司的许可协议，请在使用前仔细阅读并遵守。