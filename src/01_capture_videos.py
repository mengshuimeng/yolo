"""
1. 摄像头录像程序，用于录制视频并保存到本地。
"""
import cv2
import time
from datetime import datetime
import os
from pathlib import Path


def resolve_output_path(filename: str) -> str:
    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "videos"
    output_dir.mkdir(parents=True, exist_ok=True)
    return str(output_dir / filename)


def select_fourcc(output_filename: str) -> int:
    suffix = Path(output_filename).suffix.lower()
    if suffix in {".mp4", ".m4v", ".mov"}:
        return cv2.VideoWriter_fourcc(*"mp4v")
    if suffix == ".avi":
        return cv2.VideoWriter_fourcc(*"XVID")
    return cv2.VideoWriter_fourcc(*"mp4v")


def record_video(output_filename="recorded_video.mp4", camera_index=3, target_fps=12, max_read_failures=30):
    """
    摄像头录像程序 - 无 OSD 显示版本

    Args:
        output_filename: 输出视频文件名
        camera_index: 摄像头索引，默认为 3
        target_fps: 目标帧率，默认 12
    """
    # 初始化摄像头
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print(f"错误：无法打开摄像头 {camera_index}")
        return False

    # 设置摄像头属性
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, target_fps)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    # 获取实际参数
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    camera_fps = int(cap.get(cv2.CAP_PROP_FPS)) or target_fps

    print(f"摄像头分辨率：{frame_width}x{frame_height}")
    print(f"摄像头 FPS: {camera_fps}")
    print(f"目标录制 FPS: {target_fps}")
    print(f"输出文件：{output_filename}")
    print("开始录制... 按 'q' 键停止并保存")

    fourcc = select_fourcc(output_filename)
    out = cv2.VideoWriter(output_filename, fourcc, target_fps, (frame_width, frame_height))

    if out is None or not out.isOpened():
        print("错误：无法创建视频写入器")
        cap.release()
        return False

    # 统计变量
    start_time = time.time()
    frame_count = 0
    dropped_frames = 0
    consecutive_failures = 0

    # 创建显示窗口
    cv2.namedWindow('Camera Recording', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Camera Recording', 1280, 720)

    try:
        while True:
            loop_start = time.time()

            ret, frame = cap.read()

            if not ret:
                dropped_frames += 1
                consecutive_failures += 1
                if consecutive_failures >= max_read_failures:
                    print(f"\n连续读取失败 {max_read_failures} 次，停止录制...")
                    break
                continue
            consecutive_failures = 0

            # 写入视频（不添加任何文字覆盖）
            out.write(frame)
            frame_count += 1

            # 计算时间信息
            current_time = time.time()
            elapsed_time = current_time - start_time

            # 显示帧（纯净画面，无 OSD）
            cv2.imshow('Camera Recording', frame)

            # 精确控制帧间隔
            frame_time = time.time() - loop_start
            target_interval = 1.0 / target_fps

            if frame_time < target_interval:
                sleep_ms = int((target_interval - frame_time) * 1000)
                key = cv2.waitKey(sleep_ms) & 0xFF
            else:
                key = cv2.waitKey(1) & 0xFF

            if key == ord('q') or key == ord('Q'):
                print("\n用户请求停止录制...")
                break

    except KeyboardInterrupt:
        print("\n录制被中断...")
    finally:
        end_time = time.time()
        # 清理资源
        cap.release()
        if out is not None:
            out.release()
        cv2.destroyAllWindows()

    # 输出详细统计信息
    recording_duration = end_time - start_time
    video_duration = frame_count / target_fps
    recorded_fps = frame_count / recording_duration if recording_duration > 0 else 0
    duration_diff = abs(recording_duration - video_duration)
    duration_diff_percent = (duration_diff / recording_duration * 100) if recording_duration > 0 else 0

    print(f"\n{'=' * 50}")
    print(f"=== 录制统计 ===")
    print(f"{'=' * 50}")
    print(f"总帧数：{frame_count}")
    print(f"录制时长：{recording_duration:.3f} 秒")
    print(f"视频时长：{video_duration:.3f} 秒")
    print(f"时长差异：{duration_diff:.3f} 秒 ({duration_diff_percent:.1f}%)")
    print(f"设定帧率：{target_fps} FPS")
    print(f"平均帧率：{recorded_fps:.2f} FPS")
    print(f"丢帧数：{dropped_frames}")
    print(f"文件大小：{os.path.getsize(output_filename) / (1024 * 1024):.2f} MB")
    print(f"视频已保存至：{output_filename}")

    if duration_diff_percent > 5:
        print(f"\n⚠️  警告：时长差异超过 5%，可能原因:")
        print(f"   - 实际帧率 ({recorded_fps:.1f} FPS) 低于设定帧率 ({target_fps} FPS)")
        print(f"   - 系统性能不足或 USB 带宽限制")
        print(f"   - 建议降低分辨率或帧率")

    return True


def main():
    """主函数"""
    # 摄像头参数
    target_fps = 30
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = resolve_output_path(f"video_{timestamp}.mp4")


    print("摄像头录像程序启动")
    print("=" * 50)

    # 尝试不同摄像头索引
    for cam_idx in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        print(f"尝试摄像头索引 {cam_idx}...")
        if record_video(filename, cam_idx, target_fps):
            print("录制成功完成！")
            break
        else:
            print(f"摄像头 {cam_idx} 无法使用，尝试下一个...")
    else:
        print("所有摄像头都无法使用！")


if __name__ == "__main__":
    main()
