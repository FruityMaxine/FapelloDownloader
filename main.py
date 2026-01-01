from fapello.ui import run_interactive

if __name__ == "__main__":
    try:
        run_interactive()
    except KeyboardInterrupt:
        print("\n\n[用户已中断操作]")
    except Exception as e:
        print(f"\n[发生未捕获的错误]: {e}")
