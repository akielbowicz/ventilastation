def gamma(value,gamma=2.5):
    assert 0 <= value <= 255
    return int(pow(float(value) / 255.0, 2.5) * 255.0)

