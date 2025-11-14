import module_config as config  # 导入配置项
import exec_runner  # 导入执行器


def main():
    """主程序入口"""
    print("="*80)
    print("🎉 启动 exec 模块注入与代码执行程序")
    print("="*80)

    # 调用执行器，传入配置项
    exec_runner.run_exec_with_modules(
        code=config.CODE_TO_EXEC,
        include_builtin=True,
        include_third_party=True,
        include_custom=config.CUSTOM_PACKAGES,
        print_mod_names=config.PRINT_SOURCES
    )

    print("\n" + "="*80)
    print("🔚 程序结束")
    print("="*80)


if __name__ == "__main__":
    main()