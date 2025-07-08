    # 找到含 ROE / 股東權益報酬率 的表格
    target_table = None
    for table in tables:
        table_text = table.text
        if ('ROE' in table_text or '股東權益報酬率' in table_text) and '股利發放率' in table_text:
            target_table = table
            break
