import config  # 导入配置项
import exec_runner  # 导入执行器


def main():
    """主程序入口"""
    print("="*80)
    print("🎉 启动 exec 模块注入与代码执行程序（含标准库/第三方包函数示例）")
    print("="*80)

    # 调用执行器，传入配置项（新增 include_stdlib=True）
    exec_runner.run_exec_with_modules(
        code=config.CODE_TO_EXEC,
        include_builtin=True,
        include_stdlib=True,  # 启用标准库模块
        include_third_party=True,
        # include_all_installed=True,
        include_all_installed=False,
        include_custom=config.CUSTOM_PACKAGES,
        print_mod_names=config.PRINT_SOURCES
    )

    print("\n" + "="*80)
    print("🔚 程序结束")
    print("="*80)


if __name__ == "__main__":
    main()