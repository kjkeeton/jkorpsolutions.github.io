try:
    import flask
    import stripe
    print("Imports worked!")
except ImportError as e:
    print(f"Import failed: {e}")
