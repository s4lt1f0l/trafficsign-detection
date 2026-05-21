import torch
from torch.utils.data import Dataset
import cv2
import os
import numpy as np

class TrafficSignDataset(Dataset):
    def __init__(self, img_dir, label_dir, model_type='rcnn', transform=None):
        self.img_dir = img_dir
        self.label_dir = label_dir
        self.img_files = sorted([f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.png'))])
        self.transform = transform
        self.model_type = model_type # 'rcnn' hoặc 'detr'

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_files[idx])
        label_path = os.path.join(self.label_dir, self.img_files[idx].rsplit('.', 1)[0] + '.txt')
        
        img = cv2.imread(img_path)
        if img is None: # Kiểm tra ảnh lỗi
            return None
            
        h, w, _ = img.shape
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        boxes = []
        labels = []
        
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                for line in f:
                    data = line.split()
                    if len(data) < 5: continue
                    cls, x_c, y_c, bw, bh = map(float, data)
                    
                    if self.model_type == 'detr':
                        # CHUẨN DETR: Nhãn 0-4, cx,cy,w,h chuẩn hóa 0-1
                        labels.append(int(min(max(cls, 0), 4)))
                        boxes.append([x_c, y_c, bw, bh])
                    else:
                        # CHUẨN R-CNN: Nhãn 1-5, xmin,ymin,xmax,ymax Pixel
                        labels.append(int(min(max(cls, 0), 4)) + 1)
                        xmin = max(0, (x_c - bw/2) * w)
                        ymin = max(0, (y_c - bh/2) * h)
                        xmax = min(w, (x_c + bw/2) * w)
                        ymax = min(h, (y_c + bh/2) * h)
                        if xmax > xmin and ymax > ymin:
                            boxes.append([xmin, ymin, xmax, ymax])

        if len(boxes) == 0:
            boxes = [[0.5, 0.5, 0.05, 0.05]] if self.model_type == 'detr' else [[0, 0, 1, 1]]
            labels = [0]

        target = {
            "boxes": torch.as_tensor(boxes, dtype=torch.float32),
            "labels": torch.as_tensor(labels, dtype=torch.int64)
        }

        if self.transform:
            img = self.transform(img)
        else:
            img = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0

        return img, target

    def __len__(self):
        return len(self.img_files)