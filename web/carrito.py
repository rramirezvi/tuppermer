class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')
        montoTotal = self.session.get('cartMontoTotal')
        if not cart:
            cart = self.session['cart'] = {}
            montoTotal = self.session['cartMontoTotal'] = "0.00"
        self.cart = cart
        self.montoTotal = float(montoTotal)

    def add(self, producto, cantidad):
        if str(producto.id) not in self.cart.keys():
            self.cart[producto.id] = {'producto_id': producto.id, 'nombre': producto.nombre, 'precio': str(
                producto.precio), 'cantidad': cantidad, 'imagen': producto.imagen.url, 'categoria': producto.categoria.nombre, 'subtotal': str(producto.precio * cantidad)}
        else:
            for key, value in self.cart.items():
                if key == str(producto.id):
                    value['cantidad'] = value['cantidad'] + cantidad
                    value['subtotal'] = float(
                        value['precio']) * value['cantidad']
                    break
        self.save()

    def delete(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()

    def save(self):
        """GUARDA EL CARRITO EN LA SESION DEL USUARIO"""

        montoTotal = 0
        for key, value in self.cart.items():
            montoTotal += float(value['subtotal'])

        self.session['cartMontoTotal'] = str(montoTotal)
        self.session['cart'] = self.cart
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.session['cartMontoTotal'] = "0.00"
