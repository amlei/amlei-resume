#!/usr/bin/env python3
"""从 PDF / DOCX 简历抽证件照（嵌图里含人脸的那张），存成 PNG。

用 CNN 人脸检测（YuNet）只保留检测到人脸的候选图，分辨"证件照" vs "图标 / Logo"；模型首次自动下载到本地缓存。PDF / DOCX 都只看第 1 页；多张含人脸取最大；没有就报错退出（让用户提供）。

退出码：0 抽到；1 没找到。
"""

import argparse
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_NAME = "face_detection_yunet_2023mar.onnx"
MODEL_URL = ("https://media.githubusercontent.com/media/opencv/opencv_zoo/"
             "main/models/face_detection_yunet/" + MODEL_NAME)


def _model_path():
    """YuNet 模型缓存路径；不存在或过小（GitHub LFS 指针只有 131B）就自动下载。"""
    cache = os.path.join(os.environ.get("XDG_CACHE_HOME",
                                        os.path.expanduser("~/.cache")),
                         "resume-design")
    os.makedirs(cache, exist_ok=True)
    p = os.path.join(cache, MODEL_NAME)
    if not os.path.isfile(p) or os.path.getsize(p) < 100_000:
        import urllib.request
        print(f"⬇ 首次使用：下载 YuNet 人脸模型 -> {p}")
        urllib.request.urlretrieve(MODEL_URL, p)
        if os.path.getsize(p) < 100_000:
            print(f"✗ 模型下载失败（文件仍过小，可能拿到 LFS 指针）。"
                  f"检查网络，或手动下载 {MODEL_URL} 放到 {p}")
            sys.exit(1)
    return p


def _decode(b):
    """bytes -> BGR ndarray（失败返回 None）。"""
    import cv2
    import numpy as np
    return cv2.imdecode(np.frombuffer(b, np.uint8), cv2.IMREAD_COLOR)


def _has_face(img, model, min_score=0.5):
    """YuNet CNN 检测：返回 (是否有人脸, 最高置信度)。"""
    import cv2
    h, w = img.shape[:2]
    det = cv2.FaceDetectorYN_create(model, "", (w, h),
                                    score_threshold=0.05, nms_threshold=0.3, top_k=5000)
    det.setInputSize((w, h))
    _, faces = det.detect(img)
    if faces is None or len(faces) == 0:
        return False, 0.0
    score = max(float(f[14]) for f in faces)
    return score >= min_score, score


def _candidates_pdf(path):
    """只取第 1 页的嵌图（证件照都在首页）。"""
    import fitz
    d = fitz.open(path)
    if d.page_count == 0:
        return []
    seen, out = set(), []
    for im in d[0].get_images(full=True):
        xref = im[0]
        if xref in seen:
            continue
        seen.add(xref)
        b = d.extract_image(xref)["image"]
        out.append((b, _decode(b)))
    return out


def _candidates_docx(path):
    """只取第 1 页（第一个分页符之前）的嵌图。证件照都在首页。"""
    z = zipfile.ZipFile(path)
    names = set(z.namelist())
    doc = z.read("word/document.xml").decode("utf-8", "ignore") if "word/document.xml" in names else ""
    # 第一页 = 第一个分页符之前（显式 <w:br w:type="page"/> 或 Word 的 <w:lastRenderedPageBreak/>）
    pb = len(doc)
    for pat in (r'<w:br[^>]*w:type="page"', r'<w:lastRenderedPageBreak'):
        m = re.search(pat, doc)
        if m and m.start() < pb:
            pb = m.start()
    page1 = doc[:pb]
    rid2tgt = {}
    if "word/_rels/document.xml.rels" in names:
        rels = z.read("word/_rels/document.xml.rels").decode("utf-8", "ignore")
        rid2tgt = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    out, seen = [], set()
    for rid in re.findall(r'r:embed="(rId\d+)"', page1):
        if rid in seen:
            continue
        seen.add(rid)
        tgt = rid2tgt.get(rid, "")
        if not tgt or tgt.startswith("/"):
            continue
        member = os.path.normpath("word/" + tgt)            # media/image2.png -> word/media/image2.png
        if member in names and member.lower().rsplit(".", 1)[-1] in ("png", "jpg", "jpeg", "bmp"):
            b = z.read(member)
            out.append((b, _decode(b)))
    return out


def main():
    ap = argparse.ArgumentParser(description="从 PDF / DOCX 简历抽出证件照（CNN 人脸检测，只保留含人脸的图）。")
    ap.add_argument("src", help="简历 .pdf / .docx")
    ap.add_argument("out", help="输出 .png 路径")
    args = ap.parse_args()
    src, out = args.src, args.out
    model = _model_path()
    ext = os.path.splitext(src)[1].lower()
    if ext == ".pdf":
        cands = _candidates_pdf(src)
    elif ext == ".docx":
        cands = _candidates_docx(src)
    else:
        print(f"✗ 仅支持 .pdf / .docx，收到 {ext}")
        sys.exit(1)

    # 预过滤：跳过极小图标（<80px），再做 CNN 人脸检测
    import cv2
    faced = []
    for b, img in cands:
        if img is None:
            continue
        h, w = img.shape[:2]
        if min(w, h) < 80:
            continue
        ok, score = _has_face(img, model)
        tag = f"人脸✓({score:.2f})" if ok else "无人脸"
        print(f"  · {w}x{h}  {tag}")
        if ok:
            faced.append((b, img, w * h, score))

    if not faced:
        print(f"✗ {src} 里没有检测到含人脸的证件照"
              f"（只有图标/Logo/装饰图）。请用户单独提供照片放到产物目录。")
        sys.exit(1)

    # 含人脸的里取最大那张
    faced.sort(key=lambda t: t[2], reverse=True)
    b, img, area, score = faced[0]
    h, w = img.shape[:2]
    out_dir = os.path.dirname(os.path.abspath(out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    ok, buf = cv2.imencode(".png", img)
    open(out, "wb").write(buf.tobytes())
    print(f"✓ 抽出证件照 {w}x{h}（人脸置信度 {score:.2f}）-> {out}")


if __name__ == "__main__":
    main()
