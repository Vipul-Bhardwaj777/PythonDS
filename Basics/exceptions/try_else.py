def serve_chai(flavor):
    try:
        if flavor == "unknown":
            raise ValueError("We dont know this flavour")

    except ValueError as e:
        print(e)

    else:
        print("Chai served to the cusotmer")

    finally:
        print("Next customer please!")


serve_chai("masala")
