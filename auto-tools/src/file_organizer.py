#!/usr/bin/env python3
"""
File Organizer - 自动整理下载文件夹
展示：文件系统操作、批量处理能力
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class FileOrganizer:
    """文件自动整理工具"""
    
    # 文件类型映射
    EXTENSION_MAP: Dict[str, str] = {
        # 图片
        '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images',
        '.gif': 'Images', '.bmp': 'Images', '.svg': 'Images',
        # 文档
        '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents',
        '.txt': 'Documents', '.md': 'Documents', '.xlsx': 'Documents',
        # 代码
        '.py': 'Code', '.js': 'Code', '.ts': 'Code', '.go': 'Code',
        '.java': 'Code', '.cpp': 'Code', '.html': 'Code', '.css': 'Code',
        # 压缩
        '.zip': 'Archives', '.rar': 'Archives', '.tar': 'Archives',
        '.gz': 'Archives', '.7z': 'Archives',
        # 媒体
        '.mp3': 'Media', '.mp4': 'Media', '.avi': 'Media',
        '.mkv': 'Media', '.wav': 'Media',
        # 其他
        '.exe': 'Executables', '.dmg': 'Executables',
        '.torrent': 'Torrents',
    }
    
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.stats = {'organized': 0, 'errors': 0, 'skipped': 0}
    
    def organize(self, dry_run: bool = False) -> Dict:
        """
        整理文件夹
        
        Args:
            dry_run: 如果为 True，只显示不移动
        
        Returns:
            统计信息
        """
        if not self.target_dir.exists():
            raise FileNotFoundError(f"目录不存在：{self.target_dir}")
        
        print(f"开始整理：{self.target_dir}")
        if dry_run:
            print("⚠️  预览模式（不会实际移动文件）\n")
        
        # 获取所有文件
        files = [f for f in self.target_dir.iterdir() if f.is_file()]
        
        for file_path in files:
            self._organize_file(file_path, dry_run)
        
        return self.stats
    
    def _organize_file(self, file_path: Path, dry_run: bool) -> None:
        """整理单个文件"""
        ext = file_path.suffix.lower()
        category = self.EXTENSION_MAP.get(ext, 'Other')
        
        # 目标目录
        target_folder = self.target_dir / category
        target_path = target_folder / file_path.name
        
        # 如果文件已在正确位置，跳过
        if file_path.parent == target_folder:
            self.stats['skipped'] += 1
            return
        
        if dry_run:
            print(f"  📄 {file_path.name} → {category}/")
        else:
            try:
                target_folder.mkdir(exist_ok=True)
                
                # 处理重名文件
                if target_path.exists():
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    target_path = target_folder / f"{file_path.stem}_{timestamp}{ext}"
                
                shutil.move(str(file_path), str(target_path))
                print(f"  ✓ {file_path.name} → {category}/")
                self.stats['organized'] += 1
                
            except Exception as e:
                print(f"  ✗ {file_path.name}: {e}")
                self.stats['errors'] += 1
    
    def organize_by_date(self, dry_run: bool = False) -> Dict:
        """按日期整理文件（年/月）"""
        print(f"按日期整理：{self.target_dir}")
        
        files = [f for f in self.target_dir.iterdir() if f.is_file()]
        
        for file_path in files:
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                year_month = mtime.strftime('%Y-%m')
                target_folder = self.target_dir / year_month
                
                if dry_run:
                    print(f"  📄 {file_path.name} → {year_month}/")
                else:
                    target_folder.mkdir(exist_ok=True)
                    shutil.move(str(file_path), str(target_folder / file_path.name))
                    print(f"  ✓ {file_path.name} → {year_month}/")
                    self.stats['organized'] += 1
                    
            except Exception as e:
                print(f"  ✗ {file_path.name}: {e}")
                self.stats['errors'] += 1
        
        return self.stats
    
    def cleanup_empty_folders(self) -> int:
        """清理空文件夹"""
        removed = 0
        for folder in self.target_dir.rglob('*'):
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()
                print(f"  删除空文件夹：{folder}")
                removed += 1
        return removed


def main():
    """示例用法"""
    import sys
    
    # 默认整理当前目录
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    organizer = FileOrganizer(target)
    
    print("=" * 50)
    print("文件整理工具")
    print("=" * 50)
    
    # 预览模式
    print("\n【预览】")
    stats = organizer.organize(dry_run=True)
    
    print(f"\n统计：{stats['organized']} 个文件待整理")
    print(f"      {stats['skipped']} 个文件已归类")
    print(f"      {stats['errors']} 个错误")
    
    # 询问是否执行
    response = input("\n是否执行整理？(y/n): ")
    if response.lower() == 'y':
        print("\n【执行】")
        stats = organizer.organize(dry_run=False)
        print(f"\n✓ 整理完成！")
        print(f"  移动：{stats['organized']} 个文件")
        print(f"  跳过：{stats['skipped']} 个文件")
        print(f"  错误：{stats['errors']} 个")


if __name__ == '__main__':
    main()
