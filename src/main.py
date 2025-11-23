from application import build_app_gui, run_gui

def main() -> None:
    app_parts = build_app_gui()
    try:
        run_gui(app_parts)
    except Exception as e:
        pass

if __name__ == "__main__":
    main()