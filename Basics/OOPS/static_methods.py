class ChaiUtils:

    @staticmethod
    def clean(raw_data):
        return [item.strip() for item in raw_data.split(",")]


raw = "milk , tea, water,  ginger"
# obj = ChaiUtils()

# res = obj.clean(raw)


res = ChaiUtils.clean(raw)

print(res)
