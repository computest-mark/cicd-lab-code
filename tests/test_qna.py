def test_catpic(client):
    response = client.get('/catpic')
    assert response.data == b'Werkt niet meer, klachten bij Bart Steensma'

def test_pincode(client):
    response = client.get('/pincode')
    assert response.data == b'1234'
