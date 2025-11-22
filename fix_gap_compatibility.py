#!/usr/bin/env python3
"""
CSS gap 属性浏览器兼容性自动修复脚本

用途：自动为使用 gap 的 flexbox/grid 布局添加 margin 补偿，
使其在 IE11、搜狗、360等老浏览器中也能正常显示间距。

使用方法：
    python fix_gap_compatibility.py

配置：
    - 默认扫描目录：assets/vue/controllers/shop
    - 扫描文件类型：*.vue, *.css
    - 备份文件：修改前会自动备份为 *.bak
"""

import os
import re
import sys
import shutil
from pathlib import Path
from typing import List, Tuple, Dict

# 配置
TARGET_DIR = "assets/vue/controllers/shop"
FILE_EXTENSIONS = {".vue", ".css"}
BACKUP_ENABLED = True
DRY_RUN = False  # 设置为 True 只显示修改内容，不实际修改
VERBOSE = True

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log_info(msg):
    """打印信息"""
    if VERBOSE:
        print(f"{Colors.OKCYAN}ℹ {msg}{Colors.ENDC}")


def log_success(msg):
    """打印成功信息"""
    print(f"{Colors.OKGREEN}✓ {msg}{Colors.ENDC}")


def log_warning(msg):
    """打印警告信息"""
    print(f"{Colors.WARNING}⚠ {msg}{Colors.ENDC}")


def log_error(msg):
    """打印错误信息"""
    print(f"{Colors.FAIL}✗ {msg}{Colors.ENDC}")


def extract_gap_value(gap_declaration: str) -> str:
    """
    从 gap 声明中提取值
    
    例如：
        "gap: 8px" -> "8px"
        "gap:8px" -> "8px"
        "gap: 4px 8px" -> "4px 8px"
    """
    match = re.search(r'gap\s*:\s*([^;]+)', gap_declaration)
    if match:
        return match.group(1).strip()
    return None


def parse_gap_in_style_block(css_content: str) -> List[Dict]:
    """
    解析 CSS 代码块中的所有 gap 声明
    
    返回列表：
        [
            {
                'selector': '.flex-items',
                'gap_value': '8px',
                'original_css': '...',
                'start_pos': 100,
                'end_pos': 200,
            },
            ...
        ]
    """
    results = []
    
    # 匹配 CSS 规则块：选择器 + { ... }
    rule_pattern = r'(\.[\w\-]+(?:\s*>\s*\*|\s*[>+~]\s*[\w\-\*]+)?)\s*\{([^}]+)\}'
    
    for match in re.finditer(rule_pattern, css_content):
        selector = match.group(1).strip()
        css_block = match.group(2)
        
        # 检查是否有 gap 声明
        if 'gap:' in css_block:
            gap_value = extract_gap_value(css_block)
            if gap_value:
                # 只处理单一值的 gap（如 gap: 8px）
                # 跳过 gap: 8px 12px 这样的双值
                gap_values = gap_value.split()
                if len(gap_values) == 1:
                    results.append({
                        'selector': selector,
                        'gap_value': gap_value,
                        'css_block': css_block,
                        'full_match': match.group(0),
                        'start_pos': match.start(),
                        'end_pos': match.end(),
                    })
    
    return results


def generate_margin_fix(selector: str, gap_value: str) -> str:
    """
    为 gap 生成 margin 补偿代码
    
    例如，对于:
        selector = '.flex-items'
        gap_value = '8px'
    
    生成:
        .flex-items {
          margin-right: -8px;
        }
        
        .flex-items > * {
          margin-right: 8px;
        }
    """
    # 处理选择器（移除 > * 等后缀）
    base_selector = selector.split('>')[0].strip().split('+')[0].strip().split('~')[0].strip()
    
    margin_fix = f"""
/* 老浏览器（IE11、搜狗、360）兼容性修复：gap -> margin */
{base_selector} {{
  margin-right: -{gap_value};
}}

{base_selector} > * {{
  margin-right: {gap_value};
}}"""
    
    return margin_fix


def fix_gap_in_content(content: str) -> Tuple[str, int]:
    """
    修复单个文件中的所有 gap 声明
    
    返回：(修复后的内容, 修复个数)
    """
    gaps = parse_gap_in_style_block(content)
    
    if not gaps:
        return content, 0
    
    # 倒序处理（从后往前），避免位置偏移
    for gap_info in reversed(gaps):
        selector = gap_info['selector']
        gap_value = gap_info['gap_value']
        css_block = gap_info['css_block']
        start_pos = gap_info['start_pos']
        end_pos = gap_info['end_pos']
        
        # 检查是否已经有 margin-right 补偿
        if 'margin-right:' in css_block and f'margin-right: -{gap_value}' in css_block:
            log_warning(f"  已有补偿：{selector} (跳过)")
            continue
        
        # 在 gap 属性后添加 margin-right
        new_css_block = css_block
        gap_pattern = f'gap\\s*:\\s*{re.escape(gap_value)}'
        
        if not re.search(r'margin-right:\s*-' + re.escape(gap_value), new_css_block):
            # 在 gap 后添加 margin-right 补偿
            new_css_block = re.sub(
                gap_pattern,
                f'gap: {gap_value};\n  margin-right: -{gap_value}',
                new_css_block
            )
        
        # 生成完整的修复后 CSS
        new_rule = f"{selector} {{\n  {new_css_block.strip()}\n}}"
        
        # 替换原有的 CSS 规则
        content = content[:start_pos] + new_rule + content[end_pos:]
        
        # 在规则后添加子元素选择器的 margin
        margin_fix = generate_margin_fix(selector, gap_value)
        
        # 找到规则的结束位置并插入修复代码
        # 重新计算位置（因为已经修改过内容）
        new_rule_end = start_pos + len(new_rule)
        content = content[:new_rule_end] + '\n' + margin_fix + '\n' + content[new_rule_end:]
    
    return content, len(gaps)


def process_file(file_path: str) -> Tuple[bool, str]:
    """
    处理单个文件，修复其中的 gap 问题
    
    返回：(是否修改过, 处理信息)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # 修复内容
        fixed_content, gap_count = fix_gap_in_content(original_content)
        
        # 检查是否有修改
        if fixed_content == original_content:
            return False, f"无修改需求"
        
        if DRY_RUN:
            log_info(f"  [DRY RUN] 将修复 {gap_count} 个 gap 声明")
            return False, "[DRY RUN] 无实际修改"
        
        # 备份原文件
        if BACKUP_ENABLED:
            backup_path = file_path + '.bak'
            shutil.copy2(file_path, backup_path)
            log_info(f"  备份文件：{backup_path}")
        
        # 写入修复后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        return True, f"修复了 {gap_count} 个 gap 声明"
    
    except UnicodeDecodeError:
        return False, "编码错误（跳过）"
    except Exception as e:
        return False, f"错误：{str(e)}"


def find_files_with_gap(root_dir: str) -> List[str]:
    """
    查找目录中所有使用 gap 的文件
    """
    files = []
    
    if not os.path.exists(root_dir):
        log_error(f"目录不存在：{root_dir}")
        return files
    
    for root, dirs, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in FILE_EXTENSIONS):
                file_path = os.path.join(root, filename)
                
                # 读取文件检查是否包含 gap
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'gap:' in content or 'gap :' in content:
                            files.append(file_path)
                except:
                    pass
    
    return sorted(files)


def main():
    """主函数"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}CSS gap 兼容性自动修复工具{Colors.ENDC}\n")
    
    # 验证目录
    if not os.path.isdir(TARGET_DIR):
        log_error(f"目标目录不存在：{TARGET_DIR}")
        sys.exit(1)
    
    log_info(f"扫描目录：{TARGET_DIR}")
    
    # 查找需要修复的文件
    files_to_fix = find_files_with_gap(TARGET_DIR)
    
    if not files_to_fix:
        log_warning("未发现包含 gap 的文件")
        return
    
    log_info(f"发现 {len(files_to_fix)} 个包含 gap 的文件\n")
    
    # 处理文件
    modified_count = 0
    failed_count = 0
    
    for file_path in files_to_fix:
        rel_path = os.path.relpath(file_path)
        print(f"{Colors.BOLD}{rel_path}{Colors.ENDC}")
        
        modified, message = process_file(file_path)
        
        if modified:
            log_success(f"  {message}")
            modified_count += 1
        elif "错误" in message or "无编码" in message:
            log_error(f"  {message}")
            failed_count += 1
        else:
            log_info(f"  {message}")
    
    # 输出总结
    print(f"\n{Colors.BOLD}{Colors.HEADER}修复完成{Colors.ENDC}")
    print(f"  总计：{len(files_to_fix)} 个文件")
    print(f"  修改：{Colors.OKGREEN}{modified_count}{Colors.ENDC} 个文件")
    print(f"  跳过：{len(files_to_fix) - modified_count - failed_count} 个文件")
    
    if failed_count > 0:
        print(f"  失败：{Colors.FAIL}{failed_count}{Colors.ENDC} 个文件")
    
    if BACKUP_ENABLED and modified_count > 0:
        print(f"\n{Colors.OKCYAN}原始文件已备份为 *.bak{Colors.ENDC}")
    
    if modified_count > 0:
        print(f"\n{Colors.OKGREEN}✓ 修复成功！{Colors.ENDC}")
    else:
        print(f"\n{Colors.WARNING}⚠ 无需修改{Colors.ENDC}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}用户中断{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        log_error(f"发生错误：{str(e)}")
        sys.exit(1)
