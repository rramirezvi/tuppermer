from django.shortcuts import render, get_object_or_404

from .models import Producto, Categoria
# Create your views here.
"""VISTAS PARA EL CATALGO DE PRODUCTOS"""


def index(request):
    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()
    context = {'productos': listaProductos, 'categorias': listaCategorias}
    return render(request, 'index.html', context)


def productos_por_categoria(request, categoria_id):
    # Se obtiene la categoria por su id
    objCategoria = Categoria.objects.get(pk=categoria_id)
    # Se obtienen los productos de la categoria
    listaProductos = objCategoria.producto_set.all()

    listaCategorias = Categoria.objects.all()  # Se obtienen todas las categorias

    context = {'productos': listaProductos,
               'categorias': listaCategorias}  # Se crea el contexto

    return render(request, 'index.html', context)


def productosPorNombre(request):
    nombre = request.POST['nombre']

    listaProductos = Producto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()
    context = {'productos': listaProductos, 'categorias': listaCategorias}
    return render(request, 'index.html', context)


def productoDetalle(request, producto_id):

    # objproducto = Producto.objects.get(pk=producto_id)
    objeProducto = get_object_or_404(Producto, pk=producto_id)

    context = {'producto': objeProducto}
    return render(request, 'producto.html', context)


"""VISTAS PARA EL CARRITO DE COMPRAS"""


def carrito(request):
    return render(request, 'carrito.html')
